#!/usr/bin/env python3
"""
PRD Automation Orchestrator

Splits PRD into chunks, sends to Cursor via AppleScript, tracks state.
"""

import json
import os
import re
import subprocess
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class PRDAutomation:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.config = self.load_config()
        self.log_file = repo_root / self.config["output_dir"] / "prd_auto.log"
        self.state_file = repo_root / ".prd_auto_state.json"
        self.enhance_state_file = repo_root / ".prd_enhance_state.json"
        self.output_dir = repo_root / self.config["output_dir"]
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def load_config(self) -> Dict:
        """Load config file, create default if missing."""
        config_path = self.repo_root / "tools" / "automation" / "prd_auto_config.json"
        if not config_path.exists():
            default_config = {
                "project_name": "PRD Automation Template",
                "prd_path": "prd.md",
                "chunk_strategy": "fixed_lines",
                "chunk_size_lines": 100,
                "chat_strategy": "single_chat",
                "worker_prompt_template_path": "tools/automation/worker_prompt.md",
                "worker_prompt_enhance_path": "tools/automation/worker_prompt_enhance.md",
                "cursor_driver_path": "tools/automation/cursor_driver.scpt",
                "output_dir": "tools/automation",
                "default_wait_seconds": 60,
                "enhanced_output_path": "prd_enhanced.md",
                "enhanced_notes_output_path": "prd_enhanced_notes.md"
            }
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, "w") as f:
                json.dump(default_config, f, indent=2)
            self.log(f"Created default config at {config_path}")
            return default_config
        
        with open(config_path, "r") as f:
            return json.load(f)

    def log(self, message: str, command: str = "general", chunk_id: Optional[int] = None, phase: str = ""):
        """Log message to both stdout and log file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        chunk_str = f"[chunk={chunk_id}]" if chunk_id is not None else ""
        phase_str = f"[phase={phase}]" if phase else ""
        log_line = f"[{timestamp}][{command}]{chunk_str}{phase_str} {message}"
        
        print(log_line)
        with open(self.log_file, "a") as f:
            f.write(log_line + "\n")

    def extract_project_overview(self, prd_lines: List[str]) -> str:
        """Extract project overview from PRD (typically first section)."""
        overview_lines = []
        in_overview = False
        overview_depth = None
        
        for i, line in enumerate(prd_lines[:200]):  # Check first 200 lines
            if re.match(r"^##\s+1\.\s+Project Overview", line, re.IGNORECASE):
                in_overview = True
                overview_depth = 2
                overview_lines.append(line)
                continue
            
            if in_overview:
                # Stop at next top-level section (##)
                if re.match(r"^##\s+[2-9]", line):
                    break
                overview_lines.append(line)
        
        if not overview_lines:
            # Fallback: use first 50 lines
            overview_lines = prd_lines[:50]
        
        return "\n".join(overview_lines).strip()

    def chunk_prd(self, prd_lines: List[str]) -> List[Dict]:
        """Split PRD into deterministic chunks."""
        chunks = []
        chunk_size = self.config["chunk_size_lines"]
        current_chunk_lines = []
        current_start = 1
        current_section = "Unknown"
        chunk_id = 1
        
        for i, line in enumerate(prd_lines, start=1):
            # Detect section headers
            match = re.match(r"^(#{1,3})\s+(.+)$", line)
            if match:
                level = len(match.group(1))
                if level <= 2:  # Top-level or second-level heading
                    current_section = match.group(2).strip()
            
            current_chunk_lines.append(line)
            
            # Create chunk when size reached
            if len(current_chunk_lines) >= chunk_size:
                chunks.append({
                    "id": chunk_id,
                    "section": current_section,
                    "start_line": current_start,
                    "end_line": i,
                    "status": "pending",
                    "attempts": 0,
                    "last_result": None,
                    "last_updated_at": None,
                    "last_output_path": None
                })
                chunk_id += 1
                current_start = i + 1
                current_chunk_lines = []
        
        # Add final chunk if there are remaining lines
        if current_chunk_lines:
            chunks.append({
                "id": chunk_id,
                "section": current_section,
                "start_line": current_start,
                "end_line": len(prd_lines),
                "status": "pending",
                "attempts": 0,
                "last_result": None,
                "last_updated_at": None,
                "last_output_path": None
            })
        
        return chunks

    def load_state(self, mode: str = "run") -> Dict:
        """Load state file."""
        state_file = self.state_file if mode == "run" else self.enhance_state_file
        if state_file.exists():
            with open(state_file, "r") as f:
                return json.load(f)
        return {"chunks": [], "created_at": datetime.now().isoformat()}

    def save_state(self, state: Dict, mode: str = "run"):
        """Save state file."""
        state_file = self.state_file if mode == "run" else self.enhance_state_file
        state["updated_at"] = datetime.now().isoformat()
        with open(state_file, "w") as f:
            json.dump(state, f, indent=2)

    def init(self):
        """Initialize system: read PRD, create chunks, save state."""
        self.log("Initializing PRD automation system", "init")
        
        prd_path = self.repo_root / self.config["prd_path"]
        if not prd_path.exists():
            self.log(f"ERROR: PRD file not found at {prd_path}", "init", phase="error")
            sys.exit(1)
        
        with open(prd_path, "r", encoding="utf-8") as f:
            prd_lines = f.readlines()
        
        self.log(f"Read PRD: {len(prd_lines)} lines", "init", phase="read_prd")
        
        chunks = self.chunk_prd(prd_lines)
        self.log(f"Created {len(chunks)} chunks", "init", phase="chunking")
        
        state = {
            "chunks": chunks,
            "created_at": datetime.now().isoformat(),
            "prd_path": str(prd_path),
            "prd_line_count": len(prd_lines)
        }
        
        self.save_state(state, "run")
        self.log(f"Saved state to {self.state_file}", "init", phase="save_state")
        
        # Also initialize enhance state
        enhance_state = {
            "chunks": [chunk.copy() for chunk in chunks],
            "created_at": datetime.now().isoformat(),
            "prd_path": str(prd_path),
            "prd_line_count": len(prd_lines)
        }
        self.save_state(enhance_state, "enhance")
        self.log(f"Saved enhance state to {self.enhance_state_file}", "init", phase="save_state")

    def status(self, verbose: bool = False, mode: str = "run"):
        """Show status of chunks."""
        state = self.load_state(mode)
        chunks = state.get("chunks", [])
        
        if not chunks:
            self.log("No chunks found. Run 'init' first.", "status")
            return
        
        # Count by status
        counts = {"pending": 0, "running": 0, "done": 0, "failed": 0, "skipped_dry_run": 0}
        for chunk in chunks:
            status = chunk.get("status", "pending")
            counts[status] = counts.get(status, 0) + 1
        
        self.log(f"Chunk status summary ({mode} mode):", "status")
        self.log(f"Total chunks: {len(chunks)}", "status")
        self.log(f"pending: {counts['pending']}, done: {counts['done']}, failed: {counts['failed']}, running: {counts['running']}, skipped_dry_run: {counts['skipped_dry_run']}", "status")
        
        if verbose:
            print("\nID    Section                                  Lines          Status       Attempts  Result          Updated")
            print("-" * 100)
            for chunk in chunks:
                section = (chunk.get("section", "Unknown") or "Unknown")[:40]
                lines = f"{chunk['start_line']}-{chunk['end_line']}"
                status = chunk.get("status", "pending")
                attempts = chunk.get("attempts", 0)
                last_result = chunk.get("last_result")
                result = (last_result[:15] if last_result else "") or "N/A"
                updated = chunk.get("last_updated_at", "")[:19] if chunk.get("last_updated_at") else "N/A"
                print(f"{chunk['id']:<5} {section:<40} {lines:<14} {status:<12} {attempts:<9} {result:<15} {updated}")

    def build_prompt(self, chunk: Dict, prd_lines: List[str], mode: str = "run") -> str:
        """Build prompt from template and chunk."""
        # Load template
        template_path = self.repo_root / (
            self.config["worker_prompt_template_path"] if mode == "run" 
            else self.config["worker_prompt_enhance_path"]
        )
        
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
        
        # Extract project overview
        overview = self.extract_project_overview(prd_lines)
        
        # Extract chunk text
        chunk_text_lines = prd_lines[chunk["start_line"]-1:chunk["end_line"]]
        chunk_text = "".join(chunk_text_lines)
        
        # Replace placeholders
        prompt = template.replace("{{PROJECT_NAME}}", self.config["project_name"])
        prompt = prompt.replace("{{PROJECT_OVERVIEW}}", overview)
        prompt = prompt.replace("{{CHUNK_TEXT}}", chunk_text)
        
        return prompt

    def call_cursor_driver(self, prompt: str, wait_seconds: int, dry_run: bool = False) -> str:
        """Call AppleScript driver to interact with Cursor."""
        if dry_run:
            return f"[DRY-RUN] Would send prompt ({len(prompt)} chars) and wait {wait_seconds} seconds"
        
        driver_path = self.repo_root / self.config["cursor_driver_path"]
        if not driver_path.exists():
            raise FileNotFoundError(f"Cursor driver not found at {driver_path}")
        
        try:
            result = subprocess.run(
                ["osascript", str(driver_path), prompt, str(wait_seconds)],
                capture_output=True,
                text=True,
                timeout=wait_seconds + 30
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"AppleScript error: {result.stderr}")
            
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Timeout waiting for Cursor response after {wait_seconds + 30} seconds")
        except Exception as e:
            raise RuntimeError(f"Error calling Cursor driver: {str(e)}")

    def extract_improved_chunk(self, transcript: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract improved chunk and notes from transcript."""
        start_marker = "<<<IMPROVED_CHUNK_START>>>"
        end_marker = "<<<IMPROVED_CHUNK_END>>>"
        
        start_idx = transcript.find(start_marker)
        end_idx = transcript.find(end_marker)
        
        if start_idx == -1 or end_idx == -1:
            return None, None
        
        improved_chunk = transcript[start_idx + len(start_marker):end_idx].strip()
        
        # Try to extract notes section
        notes_section = transcript[end_idx + len(end_marker):]
        notes_match = re.search(r"###\s+Notes for This Chunk\s+(.+?)(?=\n###|\Z)", notes_section, re.DOTALL)
        notes = notes_match.group(1).strip() if notes_match else None
        
        return improved_chunk, notes

    def process_chunk(self, chunk: Dict, prd_lines: List[str], wait_seconds: int, 
                     dry_run: bool, mode: str = "run", state: Optional[Dict] = None) -> Tuple[bool, Dict]:
        """Process a single chunk. Returns (success, updated_chunk)."""
        chunk_id = chunk["id"]
        updated_chunk = chunk.copy()
        
        try:
            # Update status to running
            updated_chunk["status"] = "running"
            updated_chunk["attempts"] = updated_chunk.get("attempts", 0) + 1
            updated_chunk["last_updated_at"] = datetime.now().isoformat()
            
            # Update state temporarily
            if state:
                for i, c in enumerate(state["chunks"]):
                    if c["id"] == chunk_id:
                        state["chunks"][i] = updated_chunk
                        break
                self.save_state(state, mode)
            
            # Build prompt
            self.log(f"Processing chunk {chunk_id} (lines {updated_chunk['start_line']}-{updated_chunk['end_line']}, section=\"{updated_chunk['section']}\")", 
                    mode, chunk_id, "prepare_prompt")
            prompt = self.build_prompt(updated_chunk, prd_lines, mode)
            
            # Send to Cursor
            self.log(f"Sending chunk {chunk_id} to Cursor", mode, chunk_id, "send_prompt")
            transcript = self.call_cursor_driver(prompt, wait_seconds, dry_run)
            
            if dry_run:
                self.log(f"Dry-run: would wait {wait_seconds} seconds", mode, chunk_id, "wait")
            else:
                self.log(f"Waiting {wait_seconds} seconds for Cursor to respond", mode, chunk_id, "wait")
            
            # Save transcript
            if mode == "run":
                output_path = self.output_dir / f"output_chunk_{chunk_id}.txt"
            else:
                output_path = self.output_dir / f"enhanced_chunk_{chunk_id}.txt"
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(transcript)
            
            self.log(f"Saved transcript to {output_path}", mode, chunk_id, "save_transcript")
            
            # For enhance mode, extract improved chunk
            if mode == "enhance" and not dry_run:
                improved_chunk, notes = self.extract_improved_chunk(transcript)
                if improved_chunk:
                    improved_path = self.output_dir / f"improved_chunk_{chunk_id}.md"
                    with open(improved_path, "w", encoding="utf-8") as f:
                        f.write(improved_chunk)
                    self.log(f"Extracted improved chunk to {improved_path}", mode, chunk_id, "parse_improved_chunk")
                    
                    if notes:
                        notes_path = self.output_dir / f"improved_chunk_{chunk_id}_notes.md"
                        with open(notes_path, "w", encoding="utf-8") as f:
                            f.write(notes)
                else:
                    updated_chunk["status"] = "failed"
                    updated_chunk["last_result"] = "parse_error"
                    self.log(f"ERROR: Could not find improved chunk markers in transcript", mode, chunk_id, "error")
                    return False, updated_chunk
            
            # Mark as done
            updated_chunk["status"] = "skipped_dry_run" if dry_run else "done"
            updated_chunk["last_result"] = "ok"
            updated_chunk["last_output_path"] = str(output_path)
            self.log(f"Chunk {chunk_id} completed", mode, chunk_id, "update_state")
            return True, updated_chunk
            
        except Exception as e:
            updated_chunk["status"] = "failed"
            updated_chunk["last_result"] = "error"
            self.log(f"ERROR processing chunk {chunk_id}: {str(e)}", mode, chunk_id, "error")
            return False, updated_chunk

    def run(self, from_id: Optional[int] = None, wait_seconds: Optional[int] = None, 
           limit: Optional[int] = None, dry_run: bool = False):
        """Process pending chunks."""
        state = self.load_state("run")
        chunks = state.get("chunks", [])
        
        if not chunks:
            self.log("No chunks found. Run 'init' first.", "run")
            return
        
        # Load PRD
        prd_path = self.repo_root / self.config["prd_path"]
        with open(prd_path, "r", encoding="utf-8") as f:
            prd_lines = f.readlines()
        
        wait = wait_seconds or self.config["default_wait_seconds"]
        
        # Filter chunks
        pending_chunks = [c for c in chunks if c.get("status") == "pending"]
        
        if from_id:
            pending_chunks = [c for c in pending_chunks if c["id"] >= from_id]
        
        if limit:
            pending_chunks = pending_chunks[:limit]
        
        if not pending_chunks:
            self.log("No pending chunks to process", "run")
            return
        
        self.log(f"Processing {len(pending_chunks)} chunk(s)", "run")
        
        for chunk in pending_chunks:
            success, updated_chunk = self.process_chunk(chunk, prd_lines, wait, dry_run, "run", state)
            # Update state after each chunk
            for i, c in enumerate(state["chunks"]):
                if c["id"] == updated_chunk["id"]:
                    state["chunks"][i] = updated_chunk
                    break
            self.save_state(state, "run")

    def enhance(self, from_id: Optional[int] = None, wait_seconds: Optional[int] = None,
               limit: Optional[int] = None, dry_run: bool = False):
        """Enhance PRD chunks."""
        state = self.load_state("enhance")
        chunks = state.get("chunks", [])
        
        if not chunks:
            self.log("No chunks found. Run 'init' first.", "enhance")
            return
        
        # Load PRD
        prd_path = self.repo_root / self.config["prd_path"]
        with open(prd_path, "r", encoding="utf-8") as f:
            prd_lines = f.readlines()
        
        wait = wait_seconds or self.config["default_wait_seconds"]
        
        # Filter chunks
        pending_chunks = [c for c in chunks if c.get("status") == "pending"]
        
        if from_id:
            pending_chunks = [c for c in pending_chunks if c["id"] >= from_id]
        
        if limit:
            pending_chunks = pending_chunks[:limit]
        
        if not pending_chunks:
            self.log("No pending chunks to enhance", "enhance")
            return
        
        self.log(f"Enhancing {len(pending_chunks)} chunk(s)", "enhance")
        
        for chunk in pending_chunks:
            success, updated_chunk = self.process_chunk(chunk, prd_lines, wait, dry_run, "enhance", state)
            # Update state after each chunk
            for i, c in enumerate(state["chunks"]):
                if c["id"] == updated_chunk["id"]:
                    state["chunks"][i] = updated_chunk
                    break
            self.save_state(state, "enhance")
        
        # Check if all chunks are done, then assemble final PRD
        state = self.load_state("enhance")
        all_done = all(c.get("status") == "done" for c in state["chunks"])
        
        if all_done and not dry_run:
            self.assemble_enhanced_prd(state)

    def assemble_enhanced_prd(self, state: Dict):
        """Assemble final enhanced PRD from all improved chunks."""
        self.log("Assembling enhanced PRD from all chunks", "enhance", phase="assemble")
        
        chunks = sorted(state["chunks"], key=lambda x: x["id"])
        enhanced_lines = []
        all_notes = []
        
        for chunk in chunks:
            improved_path = self.output_dir / f"improved_chunk_{chunk['id']}.md"
            if improved_path.exists():
                with open(improved_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    enhanced_lines.append(content)
                    enhanced_lines.append("\n\n")
            
            notes_path = self.output_dir / f"improved_chunk_{chunk['id']}_notes.md"
            if notes_path.exists():
                with open(notes_path, "r", encoding="utf-8") as f:
                    notes = f.read().strip()
                    if notes:
                        all_notes.append(f"## Chunk {chunk['id']} (lines {chunk['start_line']}-{chunk['end_line']})\n\n{notes}\n\n")
        
        # Write enhanced PRD
        enhanced_path = self.repo_root / self.config["enhanced_output_path"]
        with open(enhanced_path, "w", encoding="utf-8") as f:
            f.write("".join(enhanced_lines))
        self.log(f"Wrote enhanced PRD to {enhanced_path}", "enhance", phase="assemble")
        
        # Write notes
        if all_notes:
            notes_path = self.repo_root / self.config["enhanced_notes_output_path"]
            with open(notes_path, "w", encoding="utf-8") as f:
                f.write("# Enhancement Notes\n\n")
                f.write("".join(all_notes))
            self.log(f"Wrote enhancement notes to {notes_path}", "enhance", phase="assemble")

    def retry(self, chunk_ids: List[int], mode: str = "run"):
        """Reset chunks to pending status."""
        state = self.load_state(mode)
        chunks = state.get("chunks", [])
        
        for chunk_id in chunk_ids:
            for chunk in chunks:
                if chunk["id"] == chunk_id:
                    chunk["status"] = "pending"
                    chunk["last_result"] = None
                    self.log(f"Reset chunk {chunk_id} to pending", "retry", chunk_id)
        
        self.save_state(state, mode)

    def reset(self):
        """Rebuild chunk definitions from PRD."""
        self.log("Resetting state (rebuilding chunks)", "reset")
        self.init()

    def create_prd_if_missing(self):
        """Create PRD.md from template if it doesn't exist."""
        prd_path = self.repo_root / self.config["prd_path"]
        if prd_path.exists():
            self.log(f"PRD already exists at {prd_path}", "auto-improve", phase="check_prd")
            return False
        
        template_path = self.repo_root / "tools" / "automation" / "prd_template.md"
        if not template_path.exists():
            # Create minimal template
            template_content = """# Product Requirements Document

> This PRD is automatically managed by the PRD automation system.

---

## 1. Project Overview

### 1.1 Vision
[Describe your project vision]

### 1.2 Problem Statement
[Describe the problem you're solving]

### 1.3 Goals and Non-Goals
**Goals:**
1. [Goal 1]
2. [Goal 2]

**Non-Goals:**
- [Non-goal 1]

---

## 2. Product Scope

### 2.1 In-Scope
- [Feature 1]
- [Feature 2]

### 2.2 Out-of-Scope
- [Excluded feature]

---

## 3. Features

### 3.1 Feature Group A
[Describe your features]

---

## 4. Technical Architecture

[Describe technical architecture]

---

## 5. Future Work

[Future enhancements]
"""
            with open(prd_path, "w", encoding="utf-8") as f:
                f.write(template_content)
        else:
            # Copy from template
            with open(template_path, "r", encoding="utf-8") as f:
                template_content = f.read()
            with open(prd_path, "w", encoding="utf-8") as f:
                f.write(template_content)
        
        self.log(f"Created PRD from template at {prd_path}", "auto-improve", phase="create_prd")
        return True

    def split_prd_into_sections(self, prd_lines: List[str]) -> List[Dict]:
        """Split PRD into sections based on headings."""
        sections = []
        current_section = None
        current_lines = []
        section_start = 1
        
        for i, line in enumerate(prd_lines, start=1):
            # Detect section headers (## or ###)
            match = re.match(r"^(#{2,3})\s+(.+)$", line)
            if match:
                # Save previous section
                if current_section and current_lines:
                    sections.append({
                        "title": current_section,
                        "start_line": section_start,
                        "end_line": i - 1,
                        "lines": current_lines.copy()
                    })
                
                # Start new section
                current_section = match.group(2).strip()
                section_start = i
                current_lines = [line]
            else:
                if current_section:
                    current_lines.append(line)
        
        # Add final section
        if current_section and current_lines:
            sections.append({
                "title": current_section,
                "start_line": section_start,
                "end_line": len(prd_lines),
                "lines": current_lines.copy()
            })
        
        return sections

    def build_improvement_prompt(self, section: Dict, project_overview: str) -> str:
        """Build prompt for improving a PRD section."""
        section_text = "".join(section["lines"])
        
        prompt = f"""You are an expert product manager and technical writer helping to improve a Product Requirements Document (PRD).

## Project Overview

{project_overview}

---

## Your Task

Analyze and improve the following section of the PRD. Your goal is to:

1. **Preserve all information** – Do not remove or lose any content
2. **Improve clarity and structure** – Rewrite for better readability and professional language
3. **Expand vague parts** – Turn vague notes into:
   - Clear user stories
   - Explicit functional requirements
   - Non-functional requirements
   - Edge cases
   - Success criteria
4. **Mark assumptions** – If you infer details, mark them as: `[ASSUMPTION] <detail>`
5. **Identify open questions** – Mark unclear items as: `[OPEN_QUESTION] <description>`
6. **Preserve special markers** – Keep `[ASSUMPTION]`, `[OPEN_QUESTION]`, `[DEPRECATED]`, `PROMPT` blocks exactly as they are

## Section to Improve

**Section:** {section['title']}
**Lines:** {section['start_line']}-{section['end_line']}

```markdown
{section_text}
```

---

## Output Format

Provide ONLY the improved version of this section in clean Markdown format. Start with the section heading (## or ###) and include all content. Do not add any wrapper text or explanations - just the improved markdown section.
"""
        return prompt

    def call_cursor_new_chat(self, prompt: str, wait_seconds: int, dry_run: bool = False) -> str:
        """Call AppleScript driver to open new chat in Cursor."""
        if dry_run:
            return f"[DRY-RUN] Would open new chat and send prompt ({len(prompt)} chars) and wait {wait_seconds} seconds"
        
        driver_path = self.repo_root / "tools" / "automation" / "cursor_driver_new_chat.scpt"
        if not driver_path.exists():
            # Fallback to regular driver
            self.log("New chat driver not found, using regular driver", "auto-improve", phase="warning")
            return self.call_cursor_driver(prompt, wait_seconds, dry_run)
        
        try:
            result = subprocess.run(
                ["osascript", str(driver_path), prompt, str(wait_seconds)],
                capture_output=True,
                text=True,
                timeout=wait_seconds + 30
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"AppleScript error: {result.stderr}")
            
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Timeout waiting for Cursor response after {wait_seconds + 30} seconds")
        except Exception as e:
            raise RuntimeError(f"Error calling Cursor driver: {str(e)}")

    def extract_improved_section(self, transcript: str, original_title: str) -> Optional[str]:
        """Extract improved section from transcript."""
        # Look for markdown section starting with ## or ###
        lines = transcript.split("\n")
        improved_lines = []
        in_section = False
        
        for line in lines:
            # Check if this is a section header matching our section
            match = re.match(r"^(#{2,3})\s+(.+)$", line)
            if match:
                section_title = match.group(2).strip()
                # Check if it matches our section (flexible matching)
                if original_title.lower() in section_title.lower() or section_title.lower() in original_title.lower():
                    in_section = True
                    improved_lines.append(line)
                    continue
            
            if in_section:
                # Stop at next top-level section (##)
                if re.match(r"^##\s+", line) and not line.startswith("###"):
                    # Check if this is a different section
                    if not any(keyword in line.lower() for keyword in original_title.lower().split()):
                        break
                improved_lines.append(line)
        
        if improved_lines:
            return "\n".join(improved_lines).strip()
        
        # Fallback: try to find any markdown section
        for i, line in enumerate(lines):
            if re.match(r"^(#{2,3})\s+", line):
                return "\n".join(lines[i:]).strip()
        
        return None

    def full_auto(self, wait_seconds: Optional[int] = None, dry_run: bool = False, 
                  limit: Optional[int] = None):
        """Full automation: init, enhance PRD, build prd_enhanced.md."""
        self.log("=== STARTING FULL_AUTO PIPELINE ===", "full_auto", phase="pipeline_start")
        
        # Step 1: Ensure init is done
        self.log("Step 1: Ensuring system is initialized", "full_auto", phase="init_check")
        if not self.state_file.exists():
            self.log("State file not found, running init", "full_auto", phase="init")
            self.init()
        else:
            self.log("State file exists, skipping init", "full_auto", phase="init_skip")
        
        # Step 2: Create PRD if missing
        prd_path = self.repo_root / self.config["prd_path"]
        if not prd_path.exists():
            self.log("PRD not found, creating from template", "full_auto", phase="create_prd")
            created = self.create_prd_if_missing()
            if created:
                self.log("PRD created from template. Please fill in basic information before running full_auto again.", 
                        "full_auto", phase="info")
                return
        
        # Step 3: Read PRD and prepare for enhancement
        with open(prd_path, "r", encoding="utf-8") as f:
            prd_lines = f.readlines()
        
        self.log(f"Read PRD: {len(prd_lines)} lines", "full_auto", phase="read_prd")
        
        # Step 4: Use enhance mode to process chunks and build prd_enhanced.md
        self.log("Step 2: Starting enhancement process", "full_auto", phase="enhance_start")
        
        # Load state for enhance mode
        state = self.load_state("enhance")
        chunks = state.get("chunks", [])
        
        if not chunks:
            self.log("No chunks found, running init first", "full_auto", phase="init_required")
            self.init()
            state = self.load_state("enhance")
            chunks = state.get("chunks", [])
        
        # Filter pending chunks
        pending_chunks = [c for c in chunks if c.get("status") == "pending"]
        
        if limit:
            pending_chunks = pending_chunks[:limit]
        
        if not pending_chunks:
            self.log("No pending chunks to process", "full_auto", phase="no_pending")
            # Check if prd_enhanced.md already exists
            enhanced_path = self.repo_root / self.config["enhanced_output_path"]
            if enhanced_path.exists():
                self.log(f"prd_enhanced.md already exists at {enhanced_path}", "full_auto", phase="info")
            return
        
        wait = wait_seconds or self.config["default_wait_seconds"]
        
        # Process chunks using enhance mode
        improved_chunks = {}  # Store improved chunks by id
        failed_chunks = []
        
        for chunk in pending_chunks:
            chunk_id = chunk["id"]
            self.log(f"Processing chunk {chunk_id}/{len(chunks)}: lines {chunk['start_line']}-{chunk['end_line']} (section=\"{chunk['section']}\")", 
                    "full_auto", chunk_id, "process_chunk")
            
            try:
                # Build prompt using enhance template
                prompt = self.build_prompt(chunk, prd_lines, "enhance")
                
                # Send to Cursor (new chat for each chunk)
                self.log(f"Sending chunk {chunk_id} to Cursor (new chat tab)", 
                        "full_auto", chunk_id, "send_prompt")
                transcript = self.call_cursor_new_chat(prompt, wait, dry_run)
                
                if dry_run:
                    self.log(f"Dry-run: would wait {wait} seconds", "full_auto", chunk_id, "wait")
                else:
                    self.log(f"Waiting {wait} seconds for Cursor response", "full_auto", chunk_id, "wait")
                
                # Save transcript
                transcript_path = self.output_dir / f"enhanced_chunk_{chunk_id}.txt"
                if not dry_run:
                    with open(transcript_path, "w", encoding="utf-8") as f:
                        f.write(transcript)
                    self.log(f"Saved transcript to {transcript_path}", "full_auto", chunk_id, "save_transcript")
                
                # Extract improved chunk
                improved_chunk, notes = self.extract_improved_chunk(transcript)
                if improved_chunk:
                    improved_chunks[chunk_id] = {
                        "chunk": chunk,
                        "improved": improved_chunk,
                        "notes": notes
                    }
                    chunk["status"] = "skipped_dry_run" if dry_run else "done"
                    chunk["last_result"] = "ok"
                    chunk["last_output_path"] = str(transcript_path)
                    self.log(f"Extracted improved chunk {chunk_id}", "full_auto", chunk_id, "parse_improved_chunk")
                else:
                    chunk["status"] = "failed"
                    chunk["last_result"] = "parse_error"
                    failed_chunks.append(chunk_id)
                    self.log(f"ERROR: Could not find improved chunk markers in transcript", 
                            "full_auto", chunk_id, "error")
                
                chunk["attempts"] = chunk.get("attempts", 0) + 1
                chunk["last_updated_at"] = datetime.now().isoformat()
                
            except Exception as e:
                chunk["status"] = "failed"
                chunk["last_result"] = "error"
                chunk["last_updated_at"] = datetime.now().isoformat()
                failed_chunks.append(chunk_id)
                self.log(f"ERROR processing chunk {chunk_id}: {str(e)}", "full_auto", chunk_id, "error")
            
            # Update state after each chunk
            for i, c in enumerate(state["chunks"]):
                if c["id"] == chunk_id:
                    state["chunks"][i] = chunk
                    break
            self.save_state(state, "enhance")
        
        # Step 5: Build prd_enhanced.md from all improved chunks
        if improved_chunks and not dry_run:
            self.log(f"Building prd_enhanced.md from {len(improved_chunks)} improved chunks", 
                    "full_auto", phase="assemble_enhanced")
            
            # Sort chunks by id
            sorted_chunk_ids = sorted(improved_chunks.keys())
            enhanced_lines = []
            all_notes = []
            
            for chunk_id in sorted_chunk_ids:
                data = improved_chunks[chunk_id]
                enhanced_lines.append(data["improved"])
                enhanced_lines.append("\n\n")
                
                if data["notes"]:
                    all_notes.append(f"## Chunk {chunk_id} (lines {data['chunk']['start_line']}-{data['chunk']['end_line']})\n\n{data['notes']}\n\n")
            
            # Write prd_enhanced.md
            enhanced_path = self.repo_root / self.config["enhanced_output_path"]
            with open(enhanced_path, "w", encoding="utf-8") as f:
                f.write("".join(enhanced_lines))
            self.log(f"Wrote prd_enhanced.md to {enhanced_path}", "full_auto", phase="save_enhanced")
            
            # Write notes if any
            if all_notes:
                notes_path = self.repo_root / self.config["enhanced_notes_output_path"]
                with open(notes_path, "w", encoding="utf-8") as f:
                    f.write("# Enhancement Notes\n\n")
                    f.write("".join(all_notes))
                self.log(f"Wrote enhancement notes to {notes_path}", "full_auto", phase="save_notes")
        
        # Final summary
        self.log("=== FULL_AUTO PIPELINE COMPLETED ===", "full_auto", phase="pipeline_complete")
        self.log(f"Summary: Processed {len(pending_chunks)} chunks, improved {len(improved_chunks)}, failed {len(failed_chunks)}", 
                "full_auto", phase="summary")
        
        if failed_chunks:
            self.log(f"Failed chunks: {failed_chunks}. Use 'retry --mode=enhance <ids>' to retry them.", 
                    "full_auto", phase="failed_chunks")
        
        if improved_chunks and not dry_run:
            enhanced_path = self.repo_root / self.config["enhanced_output_path"]
            self.log(f"Review {enhanced_path} and decide whether to replace prd.md or keep both.", 
                    "full_auto", phase="next_steps")

    def git_operation(self, operation: str, dry_run: bool = False) -> Tuple[bool, str]:
        """Perform git operations."""
        if dry_run:
            self.log(f"[DRY-RUN] Would run: git {operation}", "git", phase=operation)
            return True, f"[DRY-RUN] git {operation}"
        
        try:
            result = subprocess.run(
                ["git"] + operation.split(),
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                error_msg = result.stderr.strip()
                self.log(f"Git {operation} failed: {error_msg}", "git", phase=operation)
                return False, error_msg
            
            output = result.stdout.strip()
            self.log(f"Git {operation} succeeded", "git", phase=operation)
            return True, output
            
        except subprocess.TimeoutExpired:
            error_msg = f"Timeout running git {operation}"
            self.log(error_msg, "git", phase=operation)
            return False, error_msg
        except Exception as e:
            error_msg = f"Error running git {operation}: {str(e)}"
            self.log(error_msg, "git", phase=operation)
            return False, error_msg

    def git_sync(self, commit_message: Optional[str] = None, push: bool = True, 
                dry_run: bool = False):
        """Sync with GitHub: fetch, merge, add, commit, push."""
        self.log("Starting git sync", "git-sync", phase="start")
        
        # Fetch
        success, output = self.git_operation("fetch", dry_run)
        if not success:
            self.log("Git fetch failed, continuing anyway", "git-sync", phase="warning")
        
        # Pull/merge
        success, output = self.git_operation("pull", dry_run)
        if not success:
            self.log("Git pull failed, continuing anyway", "git-sync", phase="warning")
        
        # Add all changes
        success, output = self.git_operation("add .", dry_run)
        if not success:
            self.log("Git add failed", "git-sync", phase="error")
            return
        
        # Check if there are changes to commit
        success, output = self.git_operation("status --porcelain", dry_run)
        if success and output.strip():
            # Commit
            message = commit_message or f"Auto-update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            success, output = self.git_operation(f'commit -m "{message}"', dry_run)
            if not success:
                self.log("Git commit failed", "git-sync", phase="error")
                return
            
            # Push
            if push:
                success, output = self.git_operation("push", dry_run)
                if not success:
                    self.log("Git push failed", "git-sync", phase="error")
                    return
        else:
            self.log("No changes to commit", "git-sync", phase="info")
        
        self.log("Git sync completed", "git-sync", phase="complete")

    def cleanup(self, dry_run: bool = False):
        """Clean up unnecessary files."""
        self.log("Starting cleanup", "cleanup", phase="start")
        
        patterns_to_remove = [
            "**/__pycache__",
            "**/*.pyc",
            "**/*.pyo",
            "**/.DS_Store",
            "**/.AppleDouble",
        ]
        
        removed_count = 0
        for pattern in patterns_to_remove:
            for path in self.repo_root.rglob(pattern.replace("**/", "")):
                if path.is_file() or path.is_dir():
                    if dry_run:
                        self.log(f"[DRY-RUN] Would remove: {path}", "cleanup", phase="remove")
                    else:
                        try:
                            if path.is_dir():
                                import shutil
                                shutil.rmtree(path)
                            else:
                                path.unlink()
                            self.log(f"Removed: {path}", "cleanup", phase="remove")
                            removed_count += 1
                        except Exception as e:
                            self.log(f"Error removing {path}: {str(e)}", "cleanup", phase="error")
        
        self.log(f"Cleanup completed. Removed {removed_count} items", "cleanup", phase="complete")


def main():
    parser = argparse.ArgumentParser(description="PRD Automation Orchestrator")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # init
    subparsers.add_parser("init", help="Initialize system")
    
    # status
    status_parser = subparsers.add_parser("status", help="Show status")
    status_parser.add_argument("--verbose", action="store_true")
    status_parser.add_argument("--mode", choices=["run", "enhance"], default="run")
    
    # run
    run_parser = subparsers.add_parser("run", help="Process chunks")
    run_parser.add_argument("--from", type=int, dest="from_id", help="Start from chunk ID")
    run_parser.add_argument("--wait", type=int, help="Wait seconds after sending prompt")
    run_parser.add_argument("--limit", type=int, help="Process only N chunks")
    run_parser.add_argument("--dry-run", action="store_true")
    
    # enhance
    enhance_parser = subparsers.add_parser("enhance", help="Enhance PRD chunks")
    enhance_parser.add_argument("--from", type=int, dest="from_id", help="Start from chunk ID")
    enhance_parser.add_argument("--wait", type=int, help="Wait seconds after sending prompt")
    enhance_parser.add_argument("--limit", type=int, help="Process only N chunks")
    enhance_parser.add_argument("--dry-run", action="store_true")
    
    # retry
    retry_parser = subparsers.add_parser("retry", help="Retry failed chunks")
    retry_parser.add_argument("chunk_ids", type=int, nargs="+", help="Chunk IDs to retry")
    retry_parser.add_argument("--mode", choices=["run", "enhance"], default="run")
    
    # reset
    subparsers.add_parser("reset", help="Reset state")
    
    # full_auto
    full_auto_parser = subparsers.add_parser("full_auto", help="Full automation: init, enhance PRD, build prd_enhanced.md")
    full_auto_parser.add_argument("--wait", type=int, help="Wait seconds after sending prompt")
    full_auto_parser.add_argument("--limit", type=int, help="Process only N chunks")
    full_auto_parser.add_argument("--dry-run", action="store_true")
    
    # git-sync
    git_sync_parser = subparsers.add_parser("git-sync", help="Sync with GitHub (fetch, pull, add, commit, push)")
    git_sync_parser.add_argument("--message", type=str, help="Commit message")
    git_sync_parser.add_argument("--no-push", action="store_true", help="Don't push after commit")
    git_sync_parser.add_argument("--dry-run", action="store_true")
    
    # cleanup
    cleanup_parser = subparsers.add_parser("cleanup", help="Clean up unnecessary files")
    cleanup_parser.add_argument("--dry-run", action="store_true")
    
    # start (full automation pipeline)
    start_parser = subparsers.add_parser("start", help="Full automation: full_auto + cleanup + git-sync")
    start_parser.add_argument("--wait", type=int, help="Wait seconds after sending prompt to Cursor")
    start_parser.add_argument("--no-git", action="store_true", help="Skip git operations")
    start_parser.add_argument("--no-cleanup", action="store_true", help="Skip cleanup")
    start_parser.add_argument("--dry-run", action="store_true")
    start_parser.add_argument("--commit-message", type=str, help="Git commit message")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Find repo root (directory containing prd.md or tools/automation/)
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent.parent
    
    automation = PRDAutomation(repo_root)
    
    if args.command == "init":
        automation.init()
    elif args.command == "status":
        automation.status(args.verbose, args.mode)
    elif args.command == "run":
        automation.run(args.from_id, args.wait, args.limit, args.dry_run)
    elif args.command == "enhance":
        automation.enhance(args.from_id, args.wait, args.limit, args.dry_run)
    elif args.command == "retry":
        automation.retry(args.chunk_ids, args.mode)
    elif args.command == "reset":
        automation.reset()
    elif args.command == "full_auto":
        automation.full_auto(args.wait, args.dry_run, args.limit)
    elif args.command == "git-sync":
        automation.git_sync(args.message, not args.no_push, args.dry_run)
    elif args.command == "cleanup":
        automation.cleanup(args.dry_run)
    elif args.command == "start":
        # Full automation pipeline (wrapper around full_auto + cleanup + git)
        automation.log("=== STARTING FULL AUTOMATION PIPELINE ===", "start", phase="pipeline_start")
        
        # Step 1: Full auto (init + enhance)
        automation.log("Step 1: Running full_auto", "start", phase="step1")
        automation.full_auto(args.wait, args.dry_run, None)
        
        # Step 2: Cleanup
        if not args.no_cleanup:
            automation.log("Step 2: Cleaning up unnecessary files", "start", phase="step2")
            automation.cleanup(args.dry_run)
        else:
            automation.log("Step 2: Skipped (--no-cleanup)", "start", phase="step2")
        
        # Step 3: Git sync
        if not args.no_git:
            automation.log("Step 3: Syncing with GitHub", "start", phase="step3")
            automation.git_sync(args.commit_message, True, args.dry_run)
        else:
            automation.log("Step 3: Skipped (--no-git)", "start", phase="step3")
        
        automation.log("=== FULL AUTOMATION PIPELINE COMPLETED ===", "start", phase="pipeline_complete")


if __name__ == "__main__":
    main()

