#!/usr/bin/env python3
"""
Reusable PRD automation orchestrator.

Primary responsibilities:
- Load repo-specific config.
- Build deterministic PRD chunks and persist state.
- Drive CLI commands (init/status/run/enhance/retry/reset).
- Coordinate with Cursor via AppleScript driver to process each chunk.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


ROOT_DIR = Path(__file__).resolve().parents[2]
TOOLS_DIR = ROOT_DIR / "tools" / "automation"
CONFIG_PATH = TOOLS_DIR / "prd_auto_config.json"
STATE_PATH = ROOT_DIR / ".prd_auto_state.json"
ENHANCE_STATE_PATH = ROOT_DIR / ".prd_enhance_state.json"
LOG_PATH = TOOLS_DIR / "prd_auto.log"
DEFAULT_PRD_PATH = ROOT_DIR / "prd.md"


class AutomationError(Exception):
    """Custom exception for orchestration issues."""


def log(message: str, command: str = "", chunk_id: Optional[int] = None, phase: str = "") -> None:
    """Enhanced logging with phase tracking and context."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    parts = [f"[{timestamp}]"]
    if command:
        parts.append(f"[{command}]")
    if chunk_id is not None:
        parts.append(f"[chunk={chunk_id}]")
    if phase:
        parts.append(f"[phase={phase}]")
    parts.append(message)
    line = " ".join(parts)
    print(line)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def load_json(path: Path) -> Dict:
    """Load JSON file, raise AutomationError if missing."""
    if not path.exists():
        raise AutomationError(f"Missing required file: {path}")
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as e:
        raise AutomationError(f"Invalid JSON in {path}: {e}")


def save_json(path: Path, data: Dict) -> None:
    """Save JSON file, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")


def detect_project_name() -> str:
    """Detect project name from repo root directory."""
    return ROOT_DIR.name


def ensure_default_config() -> Dict:
    """Ensure config file exists, create with defaults if missing."""
    if CONFIG_PATH.exists():
        return load_json(CONFIG_PATH)

    default_config = {
        "project_name": detect_project_name(),
        "prd_path": "prd.md",
        "chunk_strategy": "fixed_lines",
        "chunk_size_lines": 100,
        "chat_strategy": "single_chat",
        "worker_prompt_template_path": "tools/automation/worker_prompt.md",
        "cursor_driver_path": "tools/automation/cursor_driver.scpt",
        "output_dir": "tools/automation",
        "default_wait_seconds": 60,
        "worker_prompt_enhance_path": "tools/automation/worker_prompt_enhance.md",
        "enhanced_output_path": "prd_enhanced.md",
        "enhanced_notes_output_path": "prd_enhanced_notes.md",
    }
    save_json(CONFIG_PATH, default_config)
    log(f"Created default config at {CONFIG_PATH}", command="init")
    return default_config


def resolve_path(path_str: str) -> Path:
    """Resolve relative path to absolute path relative to repo root."""
    path = Path(path_str)
    if not path.is_absolute():
        path = ROOT_DIR / path
    return path


def read_prd_lines(prd_path: Path) -> List[str]:
    """Read PRD file and return lines."""
    if not prd_path.exists():
        raise AutomationError(f"PRD file not found: {prd_path}")
    try:
        with prd_path.open("r", encoding="utf-8") as fh:
            return fh.readlines()
    except Exception as e:
        raise AutomationError(f"Failed to read PRD file {prd_path}: {e}")


def compute_checksum(lines: List[str]) -> str:
    """Compute SHA256 checksum of PRD lines."""
    import hashlib

    sha = hashlib.sha256()
    for line in lines:
        sha.update(line.encode("utf-8"))
    return sha.hexdigest()


def extract_overview(lines: List[str]) -> str:
    """Extract project overview from PRD (looks for 'Project Overview' section)."""
    overview_heading_indices = []
    for idx, line in enumerate(lines):
        stripped = line.strip().lower()
        if stripped.startswith("#") and "project overview" in stripped:
            overview_heading_indices.append(idx)

    if overview_heading_indices:
        start = overview_heading_indices[0] + 1
        collected = []
        for line in lines[start:]:
            if line.strip().startswith("#"):
                break
            collected.append(line)
        overview = "".join(collected).strip()
        if overview:
            return overview

    # Fallback: first ~200 words
    text = "".join(lines)
    words = text.split()
    return " ".join(words[:200])


@dataclass
class Chunk:
    """Represents a PRD chunk with metadata."""

    id: int
    section: str
    start_line: int
    end_line: int
    status: str = "pending"
    attempts: int = 0
    last_output_path: Optional[str] = None
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    chat_reference: Optional[str] = None
    last_result: Optional[str] = None  # ok, cursor_error, parse_error, etc.

    def to_dict(self) -> Dict:
        """Convert chunk to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "section": self.section,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "status": self.status,
            "attempts": self.attempts,
            "last_output_path": self.last_output_path,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "chat_reference": self.chat_reference,
            "last_result": self.last_result,
        }


def determine_section(line: str) -> Optional[str]:
    """Detect section heading from markdown line."""
    stripped = line.strip()
    if stripped.startswith("#"):
        return stripped.lstrip("#").strip()
    return None


def build_chunks(lines: List[str], chunk_size: int) -> List[Chunk]:
    """Build deterministic chunks from PRD lines."""
    if chunk_size <= 0:
        raise AutomationError("chunk_size_lines must be > 0")

    chunks: List[Chunk] = []
    line_count = len(lines)
    chunk_id = 1
    line_index = 0
    current_section = "Global"
    while line_index < line_count:
        start = line_index + 1
        end = min(line_index + chunk_size, line_count)
        chunk_lines = lines[start - 1 : end]
        for l in chunk_lines:
            detected = determine_section(l)
            if detected:
                current_section = detected
                break
        chunk = Chunk(
            id=chunk_id,
            section=current_section,
            start_line=start,
            end_line=end,
        )
        chunks.append(chunk)
        chunk_id += 1
        line_index = end
    return chunks


def build_state(config: Dict, lines: List[str]) -> Dict:
    """Build initial state from PRD."""
    chunk_size = config.get("chunk_size_lines", 100)
    chunks = build_chunks(lines, chunk_size)
    state = {
        "project_name": config.get("project_name", detect_project_name()),
        "config_path": str(CONFIG_PATH.relative_to(ROOT_DIR)),
        "prd_path": config.get("prd_path", "prd.md"),
        "chunk_strategy": config.get("chunk_strategy", "fixed_lines"),
        "chat_strategy": config.get("chat_strategy", "single_chat"),
        "overview_text": extract_overview(lines),
        "prd_checksum": compute_checksum(lines),
        "created_at": datetime.utcnow().isoformat() + "Z",
        "chunks": [chunk.to_dict() for chunk in chunks],
    }
    return state


def chunk_text(lines: List[str], chunk: Chunk) -> str:
    """Extract text for a specific chunk."""
    start = chunk.start_line - 1
    end = chunk.end_line
    subset = lines[start:end]
    return "".join(subset)


def load_state() -> Dict:
    """Load state file, raise error if missing."""
    if not STATE_PATH.exists():
        raise AutomationError("State file missing. Run `init` first.")
    return load_json(STATE_PATH)


def save_state(state: Dict) -> None:
    """Save state file."""
    save_json(STATE_PATH, state)


def prompt_for_prd_creation(prd_path: Path) -> None:
    """Prompt user to create PRD template if missing."""
    template = """# Project Name – Product Requirements Document

## Project Overview
- What problem are we solving?
- Why now?

## Goals & Non-Goals
### Goals
- ...
### Non-Goals
- ...

## Target Users
- Primary personas and their needs.

## Features / Use Cases
- Key workflows and capabilities.

## Constraints & Tech Stack
- Platforms, devices, integrations, technical boundaries.

## Automation Hints
- Any special notes to help automated prompt engineers when processing PRD chunks.
"""
    answer = input(f"No PRD found at {prd_path}. Create template? [y/N]: ").strip().lower()
    if answer == "y":
        prd_path.write_text(template, encoding="utf-8")
        log(f"Created PRD template at {prd_path}", command="init")
    else:
        raise AutomationError("PRD file is required. Supply one and rerun.")


def ensure_state(config: Dict) -> Dict:
    """Ensure state exists, create from PRD if missing."""
    prd_path = resolve_path(config.get("prd_path", "prd.md"))
    if not prd_path.exists():
        prompt_for_prd_creation(prd_path)
    lines = read_prd_lines(prd_path)
    state = build_state(config, lines)
    save_state(state)
    log(f"Initialized state with {len(state['chunks'])} chunks.", command="init")
    
    # Check for existing enhanced PRD
    enhanced_path = resolve_path(config.get("enhanced_output_path", "prd_enhanced.md"))
    if enhanced_path.exists():
        log(f"Found existing enhanced PRD at {enhanced_path}", command="init")
    
    return state


def ensure_enhance_state(base_state: Dict) -> Dict:
    """Ensure enhancement state exists, create from base state if missing."""
    if ENHANCE_STATE_PATH.exists():
        return load_json(ENHANCE_STATE_PATH)
    chunks = []
    for chunk in base_state["chunks"]:
        chunks.append(
            {
                "id": chunk["id"],
                "section": chunk["section"],
                "start_line": chunk["start_line"],
                "end_line": chunk["end_line"],
                "status": "pending",
                "attempts": 0,
                "last_output_path": None,
                "improved_chunk_path": None,
                "notes_path": None,
                "started_at": None,
                "finished_at": None,
                "last_result": None,
            }
        )
    enhance_state = {
        "project_name": base_state.get("project_name"),
        "created_at": datetime.utcnow().isoformat() + "Z",
        "chunks": chunks,
    }
    save_json(ENHANCE_STATE_PATH, enhance_state)
    log(f"Initialized enhancement state with {len(chunks)} chunks.", command="enhance")
    return enhance_state


def load_enhance_state() -> Dict:
    """Load enhancement state, raise error if missing."""
    if not ENHANCE_STATE_PATH.exists():
        raise AutomationError("Enhancement state missing. Run `init` first to build base state.")
    return load_json(ENHANCE_STATE_PATH)


def summarize_status(state: Dict) -> str:
    """Generate status summary string."""
    counts = {"pending": 0, "running": 0, "done": 0, "failed": 0, "skipped_dry_run": 0}
    for chunk in state["chunks"]:
        status = chunk.get("status", "pending")
        counts[status] = counts.get(status, 0) + 1
    summary_parts = []
    for status in ["pending", "running", "done", "failed", "skipped_dry_run"]:
        if counts.get(status, 0) > 0:
            summary_parts.append(f"{status}: {counts[status]}")
    return ", ".join(summary_parts)


def print_status(state: Dict, verbose: bool = False, mode: str = "run") -> None:
    """Print status summary, optionally verbose table."""
    total = len(state["chunks"])
    log(f"Chunk status summary ({mode} mode):", command="status")
    log(f"Total chunks: {total}", command="status")
    log(summarize_status(state), command="status")
    
    if not verbose:
        log("Chunks:", command="status")
        for chunk in state["chunks"][:10]:  # Show first 10
            log(
                f"#{chunk['id']:03d} [{chunk.get('status', 'pending')}] {chunk['section']} "
                f"(lines {chunk['start_line']}-{chunk['end_line']}) attempts={chunk.get('attempts', 0)}",
                command="status"
            )
        if total > 10:
            log(f"... and {total - 10} more chunks. Use --verbose to see all.", command="status")
    else:
        # Verbose table
        log("", command="status")
        log(f"{'ID':<5} {'Section':<40} {'Lines':<15} {'Status':<12} {'Attempts':<9} {'Result':<15} {'Updated':<20}", command="status")
        log("-" * 120, command="status")
        for chunk in state["chunks"]:
            section = chunk.get("section", "Unknown")[:38]
            line_range = f"{chunk['start_line']}-{chunk['end_line']}"
            status = chunk.get("status", "pending")
            attempts = chunk.get("attempts", 0)
            result = chunk.get("last_result", "-") or "-"
            updated = chunk.get("finished_at") or chunk.get("started_at") or "-"
            if updated != "-":
                try:
                    dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                    updated = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    pass
            log(f"{chunk['id']:<5} {section:<40} {line_range:<15} {status:<12} {attempts:<9} {result:<15} {updated:<20}", command="status")


def load_worker_template(config: Dict) -> str:
    """Load worker prompt template."""
    template_path = resolve_path(config.get("worker_prompt_template_path", "tools/automation/worker_prompt.md"))
    if not template_path.exists():
        raise AutomationError(f"Worker prompt template missing: {template_path}")
    return template_path.read_text(encoding="utf-8").strip()


def load_enhance_template(config: Dict) -> str:
    """Load enhancement worker prompt template."""
    template_path = resolve_path(config.get("worker_prompt_enhance_path", "tools/automation/worker_prompt_enhance.md"))
    if not template_path.exists():
        raise AutomationError(f"Enhancement worker prompt template missing: {template_path}")
    return template_path.read_text(encoding="utf-8").strip()


def compose_prompt(overview: str, template: str, chunk: Chunk, chunk_body: str) -> str:
    """Compose full prompt for normal run."""
    return (
        f"Project Overview:\n{overview.strip()}\n\n"
        f"{template}\n\n"
        f"---\n"
        f"PRD Chunk #{chunk.id} (lines {chunk.start_line}-{chunk.end_line}, section: {chunk.section}):\n"
        f"{chunk_body.strip()}\n"
        f"---\n"
    )


def compose_enhance_prompt(overview: str, template: str, chunk: Chunk, chunk_body: str) -> str:
    """Compose full prompt for enhancement."""
    return (
        f"Project Overview:\n{overview.strip()}\n\n"
        f"{template}\n\n"
        f"---\n"
        f"PRD Chunk #{chunk.id} (lines {chunk.start_line}-{chunk.end_line}, section: {chunk.section}):\n"
        f"{chunk_body.strip()}\n"
        f"---\n"
    )


def extract_improved_chunk(transcript_text: str) -> Tuple[str, str]:
    """Extract improved chunk and notes from transcript."""
    start_marker = "<<<IMPROVED_CHUNK_START>>>"
    end_marker = "<<<IMPROVED_CHUNK_END>>>"
    start_idx = transcript_text.find(start_marker)
    end_idx = transcript_text.find(end_marker)
    if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
        raise AutomationError("Could not find improved chunk markers in transcript.")
    improved = transcript_text[start_idx + len(start_marker) : end_idx].strip()
    notes = transcript_text[end_idx + len(end_marker) :].strip()
    return improved, notes


def run_cursor_driver(
    prompt_text: str, chunk_id: int, config: Dict, wait_seconds: int, output_prefix: str = "output_chunk", dry_run: bool = False
) -> Optional[Path]:
    """Run Cursor driver via AppleScript, or simulate in dry-run mode."""
    driver_path = resolve_path(config.get("cursor_driver_path", "tools/automation/cursor_driver.scpt"))
    
    if dry_run:
        log(f"DRY-RUN: Would invoke Cursor driver for chunk {chunk_id}", command="run", chunk_id=chunk_id, phase="send_prompt")
        log(f"DRY-RUN: Prompt length: {len(prompt_text)} chars", command="run", chunk_id=chunk_id, phase="send_prompt")
        log(f"DRY-RUN: Would wait {wait_seconds} seconds", command="run", chunk_id=chunk_id, phase="wait")
        output_dir = resolve_path(config.get("output_dir", "tools/automation"))
        output_dir.mkdir(parents=True, exist_ok=True)
        transcript_path = output_dir / f"{output_prefix}_{chunk_id}.txt"
        # Write a mock transcript for dry-run
        transcript_path.write_text(f"[DRY-RUN] Mock transcript for chunk {chunk_id}\n\n{prompt_text[:200]}...", encoding="utf-8")
        log(f"DRY-RUN: Would save transcript to {transcript_path}", command="run", chunk_id=chunk_id, phase="save_transcript")
        return transcript_path
    
    if not driver_path.exists():
        raise AutomationError(
            f"Cursor driver script missing: {driver_path}\n"
            "Please ensure cursor_driver.scpt exists in tools/automation/.\n"
            "If you don't have Cursor set up, use --dry-run mode."
        )

    output_dir = resolve_path(config.get("output_dir", "tools/automation"))
    output_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = output_dir / f"{output_prefix}_{chunk_id}.txt"

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
        tmp.write(prompt_text)
        tmp_path = Path(tmp.name)

    try:
        cmd = [
            "osascript",
            str(driver_path),
            str(tmp_path),
            str(transcript_path),
            config.get("chat_strategy", "single_chat"),
            str(wait_seconds),
        ]
        log(f"Invoking Cursor driver for chunk {chunk_id}", command="run", chunk_id=chunk_id, phase="send_prompt")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=wait_seconds + 30)
        if result.returncode != 0:
            error_msg = result.stderr.strip() or result.stdout.strip() or "Unknown error"
            raise AutomationError(
                f"Cursor driver failed for chunk {chunk_id}: {error_msg}\n"
                "This might be due to:\n"
                "- Cursor not being installed or accessible\n"
                "- Missing macOS Automation permissions (System Settings → Privacy & Security → Accessibility)\n"
                "- Cursor not responding. Try increasing --wait time."
            )
    except subprocess.TimeoutExpired:
        raise AutomationError(
            f"Cursor driver timed out for chunk {chunk_id}.\n"
            "The AppleScript may be waiting too long. Try increasing --wait time or check Cursor."
        )
    finally:
        try:
            tmp_path.unlink(missing_ok=True)
        except Exception:
            pass

    if not transcript_path.exists():
        raise AutomationError(
            f"Cursor driver did not produce transcript for chunk {chunk_id}.\n"
            "Check that Cursor is running and the AppleScript completed successfully."
        )

    return transcript_path


def process_chunk(
    state: Dict, chunk_dict: Dict, lines: List[str], config: Dict, wait_seconds: int, dry_run: bool = False
) -> None:
    """Process a single chunk (normal run mode)."""
    chunk = Chunk(**{k: v for k, v in chunk_dict.items() if k in ["id", "section", "start_line", "end_line", "status", "attempts"]})
    
    log(f"Processing chunk {chunk.id} (lines {chunk.start_line}-{chunk.end_line}, section=\"{chunk.section}\")", 
        command="run", chunk_id=chunk.id, phase="prepare_prompt")
    
    template_text = load_worker_template(config)
    overview = state.get("overview_text", "")
    body = chunk_text(lines, chunk)
    prompt = compose_prompt(overview, template_text, chunk, body)

    chunk.attempts += 1
    chunk.status = "running"
    chunk.started_at = datetime.utcnow().isoformat() + "Z"
    chunk_dict.update(chunk.to_dict())
    save_state(state)

    try:
        log(f"Sending chunk {chunk.id} to Cursor", command="run", chunk_id=chunk.id, phase="send_prompt")
        transcript_path = run_cursor_driver(prompt, chunk.id, config, wait_seconds, dry_run=dry_run)
        
        if dry_run:
            chunk.status = "skipped_dry_run"
            chunk.last_result = "dry_run"
            log(f"DRY-RUN: Chunk {chunk.id} marked as skipped_dry_run", command="run", chunk_id=chunk.id, phase="update_state")
        else:
            log(f"Waiting {wait_seconds} seconds for Cursor to respond", command="run", chunk_id=chunk.id, phase="wait")
            # Wait already happened in run_cursor_driver, but log it
            chunk.last_output_path = str(transcript_path.relative_to(ROOT_DIR))
            chunk.status = "done"
            chunk.last_result = "ok"
            log(f"Saved transcript to {chunk.last_output_path}", command="run", chunk_id=chunk.id, phase="save_transcript")
        
        chunk.finished_at = datetime.utcnow().isoformat() + "Z"
        log(f"Chunk {chunk.id} completed", command="run", chunk_id=chunk.id, phase="update_state")
    except AutomationError as exc:
        chunk.status = "failed"
        chunk.last_result = "cursor_error"
        chunk.finished_at = datetime.utcnow().isoformat() + "Z"
        log(f"Chunk {chunk.id} failed: {exc}", command="run", chunk_id=chunk.id, phase="error")
        log(f"Next: Chunk marked as failed. Use 'retry {chunk.id}' to retry.", command="run", chunk_id=chunk.id, phase="error")
    except Exception as exc:  # pylint: disable=broad-except
        chunk.status = "failed"
        chunk.last_result = "unknown_error"
        chunk.finished_at = datetime.utcnow().isoformat() + "Z"
        log(f"Chunk {chunk.id} failed with unexpected error: {exc}", command="run", chunk_id=chunk.id, phase="error")
        log(f"Next: Chunk marked as failed. Use 'retry {chunk.id}' to retry.", command="run", chunk_id=chunk.id, phase="error")
    finally:
        chunk_dict.update(chunk.to_dict())
        save_state(state)


def process_chunk_enhance(
    base_state: Dict,
    enhance_state: Dict,
    chunk_dict: Dict,
    lines: List[str],
    config: Dict,
    wait_seconds: int,
    dry_run: bool = False,
) -> None:
    """Process a single chunk in enhancement mode."""
    chunk = Chunk(
        id=chunk_dict["id"],
        section=chunk_dict["section"],
        start_line=chunk_dict["start_line"],
        end_line=chunk_dict["end_line"],
        status=chunk_dict.get("status", "pending"),
        attempts=chunk_dict.get("attempts", 0),
    )
    
    log(f"Enhancing chunk {chunk.id} (lines {chunk.start_line}-{chunk.end_line}, section=\"{chunk.section}\")",
        command="enhance", chunk_id=chunk.id, phase="prepare_prompt")
    
    template_text = load_enhance_template(config)
    overview = base_state.get("overview_text", "")
    body = chunk_text(lines, chunk)
    prompt = compose_enhance_prompt(overview, template_text, chunk, body)

    chunk_dict["attempts"] = chunk_dict.get("attempts", 0) + 1
    chunk_dict["status"] = "running"
    chunk_dict["started_at"] = datetime.utcnow().isoformat() + "Z"
    save_json(ENHANCE_STATE_PATH, enhance_state)

    try:
        log(f"Sending enhancement prompt for chunk {chunk.id} to Cursor", command="enhance", chunk_id=chunk.id, phase="send_prompt")
        transcript_path = run_cursor_driver(prompt, chunk.id, config, wait_seconds, output_prefix="enhanced_chunk", dry_run=dry_run)
        
        if dry_run:
            chunk_dict["status"] = "skipped_dry_run"
            chunk_dict["last_result"] = "dry_run"
            log(f"DRY-RUN: Chunk {chunk.id} marked as skipped_dry_run", command="enhance", chunk_id=chunk.id, phase="update_state")
        else:
            log(f"Waiting {wait_seconds} seconds for Cursor to respond", command="enhance", chunk_id=chunk.id, phase="wait")
            transcript_text = transcript_path.read_text(encoding="utf-8")
            log(f"Parsing improved chunk from transcript", command="enhance", chunk_id=chunk.id, phase="parse_improved_chunk")
            improved_text, notes_text = extract_improved_chunk(transcript_text)

            output_dir = resolve_path(config.get("output_dir", "tools/automation"))
            improved_path = output_dir / f"improved_chunk_{chunk.id}.md"
            improved_path.write_text(improved_text + "\n", encoding="utf-8")
            chunk_dict["improved_chunk_path"] = str(improved_path.relative_to(ROOT_DIR))

            notes_path = None
            if notes_text:
                notes_path_obj = output_dir / f"improved_chunk_{chunk.id}_notes.md"
                notes_path_obj.write_text(notes_text + "\n", encoding="utf-8")
                notes_path = str(notes_path_obj.relative_to(ROOT_DIR))

            chunk_dict["notes_path"] = notes_path
            chunk_dict["status"] = "done"
            chunk_dict["last_result"] = "ok"
            chunk_dict["last_output_path"] = str(transcript_path.relative_to(ROOT_DIR))
            log(f"Enhanced chunk {chunk.id} written to {chunk_dict['improved_chunk_path']}", 
                command="enhance", chunk_id=chunk.id, phase="save_transcript")
        
        chunk_dict["finished_at"] = datetime.utcnow().isoformat() + "Z"
        log(f"Chunk {chunk.id} enhancement completed", command="enhance", chunk_id=chunk.id, phase="update_state")
    except AutomationError as exc:
        chunk_dict["status"] = "failed"
        chunk_dict["last_result"] = "parse_error" if "markers" in str(exc) else "cursor_error"
        chunk_dict["finished_at"] = datetime.utcnow().isoformat() + "Z"
        log(f"Enhancement for chunk {chunk.id} failed: {exc}", command="enhance", chunk_id=chunk.id, phase="error")
        log(f"Next: Chunk marked as failed. Use 'retry --mode=enhance {chunk.id}' to retry.", 
            command="enhance", chunk_id=chunk.id, phase="error")
    except Exception as exc:  # pylint: disable=broad-except
        chunk_dict["status"] = "failed"
        chunk_dict["last_result"] = "unknown_error"
        chunk_dict["finished_at"] = datetime.utcnow().isoformat() + "Z"
        log(f"Enhancement for chunk {chunk.id} failed with unexpected error: {exc}", 
            command="enhance", chunk_id=chunk.id, phase="error")
        log(f"Next: Chunk marked as failed. Use 'retry --mode=enhance {chunk.id}' to retry.", 
            command="enhance", chunk_id=chunk.id, phase="error")
    finally:
        save_json(ENHANCE_STATE_PATH, enhance_state)


def build_enhanced_outputs(enhance_state: Dict, config: Dict) -> None:
    """Build final enhanced PRD and notes files from all improved chunks."""
    if not all(chunk["status"] == "done" for chunk in enhance_state["chunks"]):
        log("Not all chunks are done. Skipping final output assembly.", command="enhance")
        return
    
    log("All chunks enhanced. Building final outputs...", command="enhance")
    output_path = resolve_path(config.get("enhanced_output_path", "prd_enhanced.md"))
    notes_path = resolve_path(config.get("enhanced_notes_output_path", "prd_enhanced_notes.md"))
    chunks_sorted = sorted(enhance_state["chunks"], key=lambda c: c["id"])

    combined = []
    for chunk in chunks_sorted:
        improved_path = chunk.get("improved_chunk_path")
        if not improved_path:
            raise AutomationError(f"Missing improved chunk file for chunk {chunk['id']}.")
        combined.append((ROOT_DIR / improved_path).read_text(encoding="utf-8").rstrip() + "\n\n")
    output_path.write_text("".join(combined), encoding="utf-8")
    log(f"Wrote concatenated enhanced PRD to {output_path}", command="enhance")

    notes_sections = []
    for chunk in chunks_sorted:
        notes_file = chunk.get("notes_path")
        if not notes_file:
            continue
        content = (ROOT_DIR / notes_file).read_text(encoding="utf-8").strip()
        if content:
            notes_sections.append(f"## Chunk {chunk['id']} ({chunk['section']})\n{content}\n")
    if notes_sections:
        notes_path.write_text("\n\n".join(notes_sections), encoding="utf-8")
        log(f"Wrote enhancement notes to {notes_path}", command="enhance")
    elif notes_path.exists():
        notes_path.unlink()


def cmd_init(args: argparse.Namespace) -> None:
    """Initialize config and state."""
    config = ensure_default_config()
    ensure_state(config)


def cmd_status(args: argparse.Namespace) -> None:
    """Show status summary."""
    _ = ensure_default_config()
    mode = args.mode or "run"
    
    if mode == "enhance":
        state = load_enhance_state()
    else:
        state = load_state()
    
    print_status(state, verbose=args.verbose, mode=mode)


def cmd_run(args: argparse.Namespace) -> None:
    """Process pending chunks in normal mode."""
    config = ensure_default_config()
    state = load_state()
    prd_path = resolve_path(config.get("prd_path", "prd.md"))
    lines = read_prd_lines(prd_path)
    wait_seconds = args.wait or config.get("default_wait_seconds", 60)
    from_id = args.from_id or 1
    limit = args.limit or float("inf")
    dry_run = args.dry_run

    if dry_run:
        log("DRY-RUN mode: No actual Cursor calls will be made", command="run")

    template_text = load_worker_template(config)  # Validate availability early.
    _ = template_text

    processed_count = 0
    for chunk_dict in state["chunks"]:
        if chunk_dict["id"] < from_id:
            continue
        if chunk_dict["status"] != "pending":
            continue
        if processed_count >= limit:
            log(f"Reached limit of {limit} chunks. Stopping.", command="run")
            break
        process_chunk(state, chunk_dict, lines, config, wait_seconds, dry_run=dry_run)
        processed_count += 1

    if processed_count == 0:
        log("No pending chunks matched the criteria.", command="run")


def cmd_enhance(args: argparse.Namespace) -> None:
    """Process pending chunks in enhancement mode."""
    config = ensure_default_config()
    base_state = load_state()
    enhance_state = ensure_enhance_state(base_state)
    prd_path = resolve_path(config.get("prd_path", "prd.md"))
    lines = read_prd_lines(prd_path)
    wait_seconds = args.wait or config.get("default_wait_seconds", 60)
    from_id = args.from_id or 1
    limit = args.limit or float("inf")
    dry_run = args.dry_run

    if dry_run:
        log("DRY-RUN mode: No actual Cursor calls will be made", command="enhance")

    # Validate template availability early
    _ = load_enhance_template(config)

    processed_count = 0
    for chunk_dict in enhance_state["chunks"]:
        if chunk_dict["id"] < from_id:
            continue
        if chunk_dict["status"] != "pending":
            continue
        if processed_count >= limit:
            log(f"Reached limit of {limit} chunks. Stopping.", command="enhance")
            break
        process_chunk_enhance(base_state, enhance_state, chunk_dict, lines, config, wait_seconds, dry_run=dry_run)
        processed_count += 1

    if processed_count == 0:
        log("No enhancement chunks processed.", command="enhance")
    else:
        build_enhanced_outputs(enhance_state, config)


def cmd_retry(args: argparse.Namespace) -> None:
    """Reset specific chunks to pending."""
    _ = ensure_default_config()
    mode = args.mode or "run"
    ids = set(args.chunk_ids)

    if mode == "enhance":
        state = load_enhance_state()
        state_path = ENHANCE_STATE_PATH
    else:
        state = load_state()
        state_path = STATE_PATH

    for chunk in state["chunks"]:
        if chunk["id"] in ids:
            chunk["status"] = "pending"
            chunk["attempts"] = 0
            chunk["started_at"] = None
            chunk["finished_at"] = None
            chunk["last_result"] = None
            log(f"Reset chunk {chunk['id']} to pending ({mode} mode).", command="retry")

    save_json(state_path, state)


def cmd_reset(args: argparse.Namespace) -> None:
    """Rebuild state from PRD."""
    config = ensure_default_config()
    if STATE_PATH.exists():
        STATE_PATH.unlink()
        log("Deleted existing state file.", command="reset")
    if ENHANCE_STATE_PATH.exists():
        ENHANCE_STATE_PATH.unlink()
        log("Deleted existing enhancement state file.", command="reset")
    ensure_state(config)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="PRD automation orchestrator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Initialize config/state")

    status_parser = subparsers.add_parser("status", help="Show chunk status summary")
    status_parser.add_argument("--verbose", action="store_true", help="Show detailed table of all chunks")
    status_parser.add_argument("--mode", choices=["run", "enhance"], help="Show status for run or enhance mode")

    run_parser = subparsers.add_parser("run", help="Process pending chunks")
    run_parser.add_argument("--from", dest="from_id", type=int, help="Start from chunk id")
    run_parser.add_argument("--wait", dest="wait", type=int, help="Seconds to wait for chat response after sending")
    run_parser.add_argument("--limit", type=int, help="Process only N chunks then stop (useful for testing)")
    run_parser.add_argument("--dry-run", action="store_true", help="Simulate processing without calling Cursor")

    enhance_parser = subparsers.add_parser("enhance", help="Enhance PRD chunks and build prd_enhanced.md")
    enhance_parser.add_argument("--from", dest="from_id", type=int, help="Start enhancement from chunk id")
    enhance_parser.add_argument("--wait", dest="wait", type=int, help="Seconds to wait for chat response after sending")
    enhance_parser.add_argument("--limit", type=int, help="Process only N chunks then stop (useful for testing)")
    enhance_parser.add_argument("--dry-run", action="store_true", help="Simulate processing without calling Cursor")

    retry_parser = subparsers.add_parser("retry", help="Reset specific chunks to pending")
    retry_parser.add_argument("chunk_ids", type=int, nargs="+", help="Chunk ids to retry")
    retry_parser.add_argument("--mode", choices=["run", "enhance"], help="Retry in run or enhance mode")

    subparsers.add_parser("reset", help="Rebuild chunk state from PRD")

    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    """Main entry point."""
    args = parse_args(argv)
    try:
        if args.command == "init":
            cmd_init(args)
        elif args.command == "status":
            cmd_status(args)
        elif args.command == "run":
            cmd_run(args)
        elif args.command == "enhance":
            cmd_enhance(args)
        elif args.command == "retry":
            cmd_retry(args)
        elif args.command == "reset":
            cmd_reset(args)
        else:
            raise AutomationError(f"Unknown command: {args.command}")
    except AutomationError as exc:
        log(f"Error: {exc}", command=args.command if hasattr(args, "command") else "")
        sys.exit(1)
    except KeyboardInterrupt:
        log("Interrupted by user. State has been saved.", command=args.command if hasattr(args, "command") else "")
        sys.exit(130)
    except Exception as exc:
        log(f"Unexpected error: {exc}", command=args.command if hasattr(args, "command") else "")
        log("Please report this issue with the full error message.", command=args.command if hasattr(args, "command") else "")
        sys.exit(1)


if __name__ == "__main__":
    main()
