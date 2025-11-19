#!/usr/bin/env python3
"""
PRD Master - Minimal Single-File PRD Enhancement System

One master .md file that grows automatically to 100,000+ lines.
Non-destructive enhancement only - never shrinks content.
"""

import json
import re
import subprocess
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class PRDMaster:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.config = self.load_config()
        self.master_file = repo_root / self.config["master_md_path"]
        self.state_file = repo_root / ".auto_state.json"
        self.log_file = repo_root / "auto_master.log"
        self.cursor_driver = repo_root / self.config["cursor_driver_path"]
        
        # Ensure log file exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def load_config(self) -> Dict:
        """Load configuration from auto_config.json."""
        config_path = self.repo_root / "auto_config.json"
        if not config_path.exists():
            # Create default config
            default = {
                "master_md_path": "master_prd.md",
                "project_name": "PRD Master System",
                "chunk_strategy": "by_heading",
                "chunk_size_lines": 200,
                "min_chunk_lines": 50,
                "max_chunk_lines": 500,
                "wait_seconds": 60,
                "min_length_ratio": 0.90,
                "target_lines": 100000,
                "single_window_new_tab": True,
                "cursor_driver_path": "cursor_driver.scpt"
            }
            config_path.write_text(json.dumps(default, indent=2))
            return default
        return json.loads(config_path.read_text())

    def log(self, message: str, command: str = "general", chunk_id: Optional[int] = None, phase: str = ""):
        """Log to file and stdout."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        chunk_str = f"[chunk={chunk_id}]" if chunk_id else ""
        phase_str = f"[phase={phase}]" if phase else ""
        log_line = f"[{timestamp}][{command}]{chunk_str}{phase_str} {message}"
        print(log_line)
        with open(self.log_file, "a") as f:
            f.write(log_line + "\n")

    def create_master_skeleton(self, description: Optional[str] = None) -> str:
        """Create initial master_prd.md skeleton with all sections embedded."""
        project_name = self.config["project_name"]
        
        skeleton = f"""# MASTER PRD - {project_name}

<!-- AUTOMATION_METADATA -->
<!-- version: 1.0 -->
<!-- total_lines: 0 -->
<!-- created: {datetime.now().isoformat()} -->
<!-- last_enhanced: {datetime.now().isoformat()} -->
<!-- -->

{f"**Project Description:** {description}" if description else "[Describe your product vision here]"}

---

# 1. PRODUCT OVERVIEW

## 1.1 Vision

[Describe your product vision here]

## 1.2 Mission

[What problem does this solve?]

## 1.3 Goals

- [Goal 1]
- [Goal 2]
- [Goal 3]

## 1.4 Non-Goals

- [What we explicitly won't build]

---

# 2. USERS & USE CASES

## 2.1 Target Users

[Describe your target users]

## 2.2 Primary Use Cases

[Key use cases]

## 2.3 User Personas

[User personas]

## 2.4 User Stories

[Detailed user stories]

---

# 3. FUNCTIONAL REQUIREMENTS

## 3.1 Core Features

[Core features]

## 3.2 Feature Details

[Detailed feature requirements]

## 3.3 Edge Cases

[Edge cases and error handling]

---

# 4. NON-FUNCTIONAL REQUIREMENTS

## 4.1 Performance

[Performance requirements]

## 4.2 Security

[Security requirements]

## 4.3 Scalability

[Scalability requirements]

## 4.4 Reliability

[Reliability and availability requirements]

---

# 5. ARCHITECTURE

## 5.1 System Architecture

[High-level architecture]

## 5.2 Technology Stack

[Tech stack decisions]

## 5.3 Design Patterns

[Design patterns used]

## 5.4 Component Design

[Component-level design details]

---

# 6. DATA MODELS

## 6.1 Core Entities

[Data models]

## 6.2 Relationships

[Entity relationships]

## 6.3 Database Schema

[Database design]

---

# 7. API DESIGN

## 7.1 API Endpoints

[API endpoints]

## 7.2 Request/Response Formats

[API formats]

## 7.3 Authentication & Authorization

[Auth design]

---

# 8. UX & FLOWS

## 8.1 User Flows

[Key user flows]

## 8.2 Wireframes & Mockups

[UX notes and designs]

## 8.3 UI Components

[Component design]

---

# 9. IMPLEMENTATION STRATEGY

## 9.1 Development Phases

[Implementation phases]

## 9.2 Milestones

[Key milestones]

## 9.3 Technical Roadmap

[Technical implementation roadmap]

---

# 10. QA & TESTING

## 10.1 Testing Strategy

[Testing approach]

## 10.2 Test Cases

[Test cases]

## 10.3 Quality Assurance

[QA processes]

---

# 11. PROMPT LIBRARY

## 11.1 Development Prompts

[Prompts for dev agents]

### Example Dev Agent Prompt

```
[Place dev agent prompts here]
```

## 11.2 UX Prompts

[Prompts for UX agents]

### Example UX Agent Prompt

```
[Place UX agent prompts here]
```

## 11.3 Architecture Prompts

[Prompts for architecture work]

---

# 12. TASKS & PROGRESS

## 12.1 Current Tasks

[Active tasks]

## 12.2 Completed Tasks

[Completed work]

## 12.3 Blockers & Issues

[Current blockers]

---

# 13. ARCHITECTURE NOTES

[Former ARCHITECTURE.md content - all architecture notes go here]

## 13.1 System Design

[System design notes]

## 13.2 Technical Decisions

[Technical decision records]

---

# 14. IMPLEMENTATION NOTES

[Former IMPLEMENTATION_NOTES.md content]

## 14.1 Development Notes

[Development implementation notes]

## 14.2 Code Patterns

[Code patterns and conventions]

---

# 15. PROGRESS LOG

[Former PROGRESS_LOG.md content]

## 15.1 Daily Progress

[Progress tracking]

---

# 16. NOTES & FUTURE WORK

## 16.1 Open Questions

[Open questions]

## 16.2 Future Enhancements

[Future ideas]

## 16.3 Deprecated Items

[Items marked as deprecated but preserved for reference]

---

<!-- END OF DOCUMENT -->
"""
        return skeleton

    def merge_existing_files(self) -> str:
        """Merge content from existing files (prd.md, omni_corp_prompts.md, etc.) into master_prd.md structure."""
        merged_content = []
        merged_content.append("# MASTER PRD - " + self.config["project_name"])
        merged_content.append("")
        merged_content.append("<!-- AUTOMATION_METADATA -->")
        merged_content.append(f"<!-- version: 1.0 -->")
        merged_content.append(f"<!-- total_lines: 0 -->")
        merged_content.append(f"<!-- created: {datetime.now().isoformat()} -->")
        merged_content.append(f"<!-- last_enhanced: {datetime.now().isoformat()} -->")
        merged_content.append("<!-- -->")
        merged_content.append("")
        
        # Try to merge prd.md (main content)
        prd_path = self.repo_root / "prd.md"
        if prd_path.exists():
            self.log(f"Merging content from prd.md", "init", phase="merge")
            prd_content = prd_path.read_text()
            merged_content.append(prd_content)
            merged_content.append("")
            merged_content.append("---")
            merged_content.append("")
        
        # Add prompt library section with omni_corp_prompts.md
        merged_content.append("# 11. PROMPT LIBRARY")
        merged_content.append("")
        merged_content.append("## 11.1 Omni-Corp Master Prompt Library")
        merged_content.append("")
        omni_path = self.repo_root / "omni_corp_prompts.md"
        if omni_path.exists():
            self.log(f"Merging content from omni_corp_prompts.md", "init", phase="merge")
            omni_content = omni_path.read_text()
            merged_content.append(omni_content)
            merged_content.append("")
        
        # Add phase-by-phase prompts from prompt.md
        prompt_path = self.repo_root / "prompt.md"
        if prompt_path.exists():
            self.log(f"Merging content from prompt.md", "init", phase="merge")
            merged_content.append("## 11.2 Phase-by-Phase Development Prompts")
            merged_content.append("")
            prompt_content = prompt_path.read_text()
            merged_content.append(prompt_content)
            merged_content.append("")
        
        # Add architecture notes
        arch_path = self.repo_root / "ARCHITECTURE.md"
        if arch_path.exists():
            self.log(f"Merging content from ARCHITECTURE.md", "init", phase="merge")
            merged_content.append("---")
            merged_content.append("")
            merged_content.append("# 13. ARCHITECTURE NOTES")
            merged_content.append("")
            arch_content = arch_path.read_text()
            merged_content.append(arch_content)
            merged_content.append("")
        
        # Add implementation notes
        impl_path = self.repo_root / "IMPLEMENTATION_NOTES.md"
        if impl_path.exists():
            self.log(f"Merging content from IMPLEMENTATION_NOTES.md", "init", phase="merge")
            merged_content.append("---")
            merged_content.append("")
            merged_content.append("# 14. IMPLEMENTATION NOTES")
            merged_content.append("")
            impl_content = impl_path.read_text()
            merged_content.append(impl_content)
            merged_content.append("")
        
        # Add tasks
        tasks_path = self.repo_root / "TASKS.md"
        if tasks_path.exists():
            self.log(f"Merging content from TASKS.md", "init", phase="merge")
            merged_content.append("---")
            merged_content.append("")
            merged_content.append("# 12. TASKS & PROGRESS")
            merged_content.append("")
            tasks_content = tasks_path.read_text()
            merged_content.append(tasks_content)
            merged_content.append("")
        
        # Add progress log
        progress_path = self.repo_root / "PROGRESS_LOG.md"
        if progress_path.exists():
            self.log(f"Merging content from PROGRESS_LOG.md", "init", phase="merge")
            merged_content.append("---")
            merged_content.append("")
            merged_content.append("# 15. PROGRESS LOG")
            merged_content.append("")
            progress_content = progress_path.read_text()
            merged_content.append(progress_content)
            merged_content.append("")
        
        merged_content.append("")
        merged_content.append("<!-- END OF DOCUMENT -->")
        
        return "\n".join(merged_content)

    def init(self, description: Optional[str] = None):
        """Initialize system - create master_prd.md if missing, merging existing files."""
        if self.master_file.exists():
            self.log(f"master_prd.md already exists at {self.master_file}", "init")
            # Still rebuild chunk map if state is missing
            state = self.load_state()
            if not state.get("chunks"):
                self.build_chunk_map()
            return
        
        # Check if we have existing files to merge
        has_existing = any([
            (self.repo_root / "prd.md").exists(),
            (self.repo_root / "omni_corp_prompts.md").exists(),
            (self.repo_root / "prompt.md").exists(),
        ])
        
        if has_existing:
            self.log("Merging existing files into master_prd.md", "init", phase="merge")
            merged_content = self.merge_existing_files()
            self.master_file.write_text(merged_content)
            self.log(f"Merged existing files into master_prd.md ({len(merged_content.splitlines())} lines)", "init", phase="merge_complete")
        else:
            self.log("Creating master_prd.md skeleton", "init", phase="create")
            skeleton = self.create_master_skeleton(description)
            self.master_file.write_text(skeleton)
            self.log(f"Created master_prd.md with {len(skeleton.splitlines())} lines", "init", phase="create_complete")
        
        # Build initial chunk map
        self.build_chunk_map()
        self.log("Initialization complete", "init", phase="complete")

    def build_chunk_map(self) -> List[Dict]:
        """Build chunk map covering all lines in master_prd.md exactly once."""
        if not self.master_file.exists():
            return []
        
        content = self.master_file.read_text()
        lines = content.splitlines()
        
        chunks = []
        
        if self.config["chunk_strategy"] == "by_heading":
            # Split by top-level headings (# 1., # 2., etc.)
            current_chunk = None
            current_lines = []
            chunk_start = 1
            first_section_start = 1
            
            for i, line in enumerate(lines, start=1):
                # Detect top-level heading (starts with # followed by number)
                match = re.match(r"^#\s+(\d+)\.\s+(.+)$", line)
                if match:
                    # Save previous chunk
                    if current_chunk:
                        chunks.append({
                            "id": len(chunks) + 1,
                            "title": current_chunk,
                            "start_line": chunk_start,
                            "end_line": i - 1,
                            "status": "pending",
                            "attempts": 0
                        })
                    else:
                        # First section - include any preamble/metadata
                        if chunk_start < i:
                            chunks.append({
                                "id": len(chunks) + 1,
                                "title": "Document Header & Metadata",
                                "start_line": 1,
                                "end_line": i - 1,
                                "status": "pending",
                                "attempts": 0
                            })
                    
                    # Start new chunk
                    current_chunk = match.group(2).strip()
                    chunk_start = i
                    current_lines = [line]
                else:
                    current_lines.append(line)
            
            # Add final chunk
            if current_chunk:
                chunks.append({
                    "id": len(chunks) + 1,
                    "title": current_chunk,
                    "start_line": chunk_start,
                    "end_line": len(lines),
                    "status": "pending",
                    "attempts": 0
                })
            elif chunk_start == 1:
                # No numbered sections found, but we have content - create header chunk
                chunks.append({
                    "id": 1,
                    "title": "Document Header & Metadata",
                    "start_line": 1,
                    "end_line": min(100, len(lines)),  # First 100 lines or all if less
                    "status": "pending",
                    "attempts": 0
                })
                # If there's more content, create another chunk
                if len(lines) > 100:
                    chunks.append({
                        "id": 2,
                        "title": "Complete Document",
                        "start_line": 101,
                        "end_line": len(lines),
                        "status": "pending",
                        "attempts": 0
                    })
            
            # If no chunks found (no numbered headings), create one chunk for entire file
            if not chunks:
                chunks.append({
                    "id": 1,
                    "title": "Complete Document",
                    "start_line": 1,
                    "end_line": len(lines),
                    "status": "pending",
                    "attempts": 0
                })
        else:
            # Fixed line ranges
            chunk_size = self.config["chunk_size_lines"]
            for i in range(0, len(lines), chunk_size):
                chunk_id = len(chunks) + 1
                start = i + 1
                end = min(i + chunk_size, len(lines))
                
                # Find section title (nearest heading above)
                title = "Unknown"
                for j in range(i, max(0, i - 50), -1):
                    match = re.match(r"^#+\s+(.+)$", lines[j])
                    if match:
                        title = match.group(1).strip()
                        break
                
                chunks.append({
                    "id": chunk_id,
                    "title": title,
                    "start_line": start,
                    "end_line": end,
                    "status": "pending",
                    "attempts": 0
                })
        
        # Validate: every line must be covered exactly once
        covered_lines = set()
        for chunk in chunks:
            for line_num in range(chunk["start_line"], chunk["end_line"] + 1):
                if line_num in covered_lines:
                    self.log(f"WARNING: Line {line_num} covered multiple times", "chunk_map", phase="validation")
                covered_lines.add(line_num)
        
        missing_lines = set(range(1, len(lines) + 1)) - covered_lines
        if missing_lines:
            self.log(f"WARNING: Uncovered lines: {sorted(missing_lines)[:10]}...", "chunk_map", phase="validation")
        
        # Save state
        state = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "master_file": str(self.master_file),
            "total_lines": len(lines),
            "chunks": chunks
        }
        self.save_state(state)
        
        self.log(f"Built chunk map: {len(chunks)} chunks covering {len(lines)} lines", "init", phase="chunk_map")
        return chunks

    def load_state(self) -> Dict:
        """Load state from .auto_state.json."""
        if not self.state_file.exists():
            return {"chunks": []}
        return json.loads(self.state_file.read_text())

    def save_state(self, state: Dict):
        """Save state to .auto_state.json."""
        state["updated_at"] = datetime.now().isoformat()
        self.state_file.write_text(json.dumps(state, indent=2))

    def status(self, verbose: bool = False):
        """Show processing status."""
        state = self.load_state()
        chunks = state.get("chunks", [])
        
        if not chunks:
            self.log("No chunks found. Run 'init' first.", "status")
            return
        
        # Count by status
        counts = {"pending": 0, "done": 0, "failed": 0, "running": 0}
        for chunk in chunks:
            status = chunk.get("status", "pending")
            counts[status] = counts.get(status, 0) + 1
        
        current_lines = len(self.master_file.read_text().splitlines()) if self.master_file.exists() else 0
        target_lines = self.config["target_lines"]
        
        self.log(f"Status: {len(chunks)} total chunks, {current_lines}/{target_lines} lines", "status")
        self.log(f"  pending: {counts['pending']}, done: {counts['done']}, failed: {counts['failed']}, running: {counts['running']}", "status")
        
        # Show failed chunks
        failed = [c for c in chunks if c.get("status") == "failed"]
        if failed:
            self.log(f"Failed chunks: {[c['id'] for c in failed]}", "status")
        
        # Verbose mode: show table
        if verbose:
            self.log("", "status")
            self.log("Detailed Chunk Status:", "status")
            self.log(f"{'ID':<5} {'Lines':<15} {'Section':<30} {'Status':<10} {'Attempts':<10} {'Last Updated':<20}", "status")
            self.log("-" * 100, "status")
            for chunk in chunks:
                line_range = f"{chunk['start_line']}-{chunk['end_line']}"
                title = chunk.get('title', 'Unknown')[:28]
                status = chunk.get('status', 'pending')
                attempts = chunk.get('attempts', 0)
                last_updated = chunk.get('last_updated', 'N/A')[:19] if chunk.get('last_updated') else 'N/A'
                self.log(f"{chunk['id']:<5} {line_range:<15} {title:<30} {status:<10} {attempts:<10} {last_updated:<20}", "status")
                if chunk.get('last_error'):
                    self.log(f"      Error: {chunk['last_error'][:80]}", "status")

    def build_enhancement_prompt(self, chunk: Dict, chunk_text: str) -> str:
        """Build prompt for enhancing a chunk."""
        project_name = self.config["project_name"]
        
        # Get high-level project summary from top of master file
        project_summary = ""
        if self.master_file.exists():
            try:
                content = self.master_file.read_text()
                lines = content.splitlines()
                # Get first 50 lines as context
                project_summary = "\n".join(lines[:50])
            except:
                pass
        
        prompt = f"""# Enhancement Task - {project_name}

You are enhancing a section of a Master PRD document. This is a **NON-DESTRUCTIVE** enhancement process.

## CRITICAL RULES

1. **Preserve ALL information** - Do NOT delete, summarize, or shorten any content
2. **Expand and improve** - Add detail, examples, edge cases, requirements
3. **Improve structure** - Better organization, clarity, formatting
4. **Minimum length** - Improved section must be ≥90% of original length (ideally 100%+)
5. **Mark deprecated** - If something seems obsolete, mark as `[DEPRECATED]` but keep it
6. **No line deletion** - Every concept, requirement, detail must be retained
7. **Mark assumptions** - If you add assumptions, mark as `[ASSUMPTION]`
8. **Mark open questions** - If something is unclear, mark as `[OPEN_QUESTION]`
9. **Mark prompt candidates** - If you think something could be a prompt, mark as `[PROMPT_CANDIDATE]`

## What to Do

- Expand vague notes into detailed requirements
- Add concrete examples and use cases
- Include edge cases and error handling
- Improve clarity and professional language
- Add structure and organization
- Preserve all original content
- Add cross-references where appropriate
- Expand technical specifications
- Rephrase, expand, clarify, structure
- If something is unclear, mark `[OPEN_QUESTION]`
- If you add assumptions, mark `[ASSUMPTION]`
- If something is obsolete, mark `[DEPRECATED]` but keep it

## Output Format

Wrap your improved section between these exact markers:

<<<IMPROVED_CHUNK_START>>>
... your improved markdown section, same scope ...
<<<IMPROVED_CHUNK_END>>>

### Notes for This Chunk

- [ASSUMPTION] ... (if any)
- [OPEN_QUESTION] ... (if any)
- [PROMPT_CANDIDATE] ... (if any)

---

# Project Context (for reference)

{project_summary[:2000] if project_summary else "[Project context not available]"}

---

# Section to Enhance

**Section:** {chunk['title']}
**Lines:** {chunk['start_line']}-{chunk['end_line']}

{chunk_text}
"""
        return prompt

    def call_cursor(self, prompt: str, wait_seconds: int) -> str:
        """Call Cursor via AppleScript."""
        if not self.cursor_driver.exists():
            raise FileNotFoundError(f"Cursor driver not found: {self.cursor_driver}")
        
        try:
            result = subprocess.run(
                ["osascript", str(self.cursor_driver), prompt, str(wait_seconds)],
                capture_output=True,
                text=True,
                timeout=wait_seconds + 30
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"AppleScript error: {result.stderr}")
            
            transcript = result.stdout.strip()
            
            # Validate transcript
            if len(transcript) < 10:
                raise RuntimeError("Transcript too short - may not have copied correctly")
            
            return transcript
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Timeout waiting for Cursor response")
        except Exception as e:
            raise RuntimeError(f"Error calling Cursor: {str(e)}")

    def extract_improved_section(self, transcript: str, original_text: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract improved section from transcript. Returns (improved_text, error_message)."""
        # Try new format first
        start_marker = "<<<IMPROVED_CHUNK_START>>>"
        end_marker = "<<<IMPROVED_CHUNK_END>>>"
        
        # Fallback to old format for compatibility
        if start_marker not in transcript:
            start_marker = "<<<IMPROVED_SECTION_START>>>"
            end_marker = "<<<IMPROVED_SECTION_END>>>"
        
        start_idx = transcript.find(start_marker)
        end_idx = transcript.find(end_marker)
        
        if start_idx == -1 or end_idx == -1:
            return None, "Missing markers in transcript"
        
        improved = transcript[start_idx + len(start_marker):end_idx].strip()
        
        # CRITICAL: Validate length - must be ≥90% of original
        original_len = len(original_text)
        improved_len = len(improved)
        min_ratio = self.config["min_length_ratio"]
        
        if improved_len < original_len * min_ratio:
            error = f"Improved section too short: {improved_len} chars vs {original_len} chars ({improved_len/original_len*100:.1f}%). Minimum: {min_ratio*100}%. Content may have been lost."
            return improved, error
        
        # Log if close to minimum (warning)
        ratio = improved_len / original_len if original_len > 0 else 0
        if ratio < 1.0:
            self.log(f"Warning: Chunk length ratio {ratio*100:.1f}% (acceptable but not expanded)", "extract", phase="length_check")
        
        return improved, None

    def update_master_file(self, chunk: Dict, improved_text: str):
        """Update master_prd.md with improved chunk. Non-destructive - preserves all content."""
        content = self.master_file.read_text()
        lines = content.splitlines()
        
        # CRITICAL: Before update, verify original chunk still matches
        original_chunk_lines = lines[chunk["start_line"]-1:chunk["end_line"]]
        original_chunk_text = "\n".join(original_chunk_lines)
        
        # Replace chunk lines
        new_lines = lines[:chunk["start_line"]-1] + improved_text.splitlines() + lines[chunk["end_line"]:]
        
        # Calculate new line count
        new_line_count = len(new_lines)
        original_line_count = len(lines)
        
        # Update metadata
        content_text = "\n".join(new_lines)
        content_text = re.sub(
            r"<!-- total_lines: \d+ -->",
            f"<!-- total_lines: {new_line_count} -->",
            content_text
        )
        content_text = re.sub(
            r"<!-- last_enhanced: .+? -->",
            f"<!-- last_enhanced: {datetime.now().isoformat()} -->",
            content_text
        )
        
        # Write updated file
        self.master_file.write_text(content_text)
        
        self.log(f"Updated master_prd.md: chunk {chunk['id']} ({original_line_count} -> {new_line_count} lines)", 
                "update", chunk["id"], "file_update")

    def enhance_chunk(self, chunk: Dict, wait_seconds: int, dry_run: bool = False) -> Tuple[bool, Dict]:
        """Enhance a single chunk. Returns (success, updated_chunk)."""
        chunk_id = chunk["id"]
        updated_chunk = chunk.copy()
        
        try:
            # Load master file
            content = self.master_file.read_text()
            lines = content.splitlines()
            
            # Verify chunk bounds are still valid
            if chunk["end_line"] > len(lines):
                self.log(f"ERROR: Chunk {chunk_id} end_line {chunk['end_line']} exceeds file length {len(lines)}", 
                        "enhance", chunk_id, "error")
                updated_chunk["status"] = "failed"
                updated_chunk["last_error"] = "Chunk bounds invalid - file may have changed"
                return False, updated_chunk
            
            # Extract chunk text
            chunk_lines = lines[chunk["start_line"]-1:chunk["end_line"]]
            chunk_text = "\n".join(chunk_lines)
            
            if not chunk_text.strip():
                self.log(f"WARNING: Chunk {chunk_id} is empty, skipping", "enhance", chunk_id, "warning")
                updated_chunk["status"] = "done"
                updated_chunk["last_result"] = "skipped_empty"
                return True, updated_chunk
            
            # Build prompt
            prompt = self.build_enhancement_prompt(chunk, chunk_text)
            
            # Update status
            updated_chunk["status"] = "running"
            updated_chunk["attempts"] = updated_chunk.get("attempts", 0) + 1
            updated_chunk["last_updated"] = datetime.now().isoformat()
            
            self.log(f"Enhancing chunk {chunk_id}: {chunk['title']} (lines {chunk['start_line']}-{chunk['end_line']})", 
                    "enhance", chunk_id, "start")
            
            if dry_run:
                self.log(f"DRY-RUN: Would enhance chunk {chunk_id}", "enhance", chunk_id, "dry_run")
                updated_chunk["status"] = "skipped_dry_run"
                return True, updated_chunk
            
            # Send to Cursor
            self.log(f"Sending chunk {chunk_id} to Cursor", "enhance", chunk_id, "send")
            transcript = self.call_cursor(prompt, wait_seconds)
            
            # Extract improved section
            improved, error = self.extract_improved_section(transcript, chunk_text)
            
            if error:
                updated_chunk["status"] = "failed"
                updated_chunk["last_error"] = error
                self.log(f"ERROR: {error}", "enhance", chunk_id, "error")
                return False, updated_chunk
            
            # Update master file
            self.update_master_file(chunk, improved)
            
            # Mark as done
            updated_chunk["status"] = "done"
            updated_chunk["last_result"] = "ok"
            updated_chunk["original_length"] = len(chunk_text)
            updated_chunk["improved_length"] = len(improved)
            updated_chunk["length_ratio"] = len(improved) / len(chunk_text) if len(chunk_text) > 0 else 0
            
            self.log(f"Chunk {chunk_id} enhanced successfully ({updated_chunk['length_ratio']*100:.1f}% of original)", 
                    "enhance", chunk_id, "complete")
            
            return True, updated_chunk
            
        except Exception as e:
            updated_chunk["status"] = "failed"
            updated_chunk["last_error"] = str(e)
            self.log(f"ERROR enhancing chunk {chunk_id}: {str(e)}", "enhance", chunk_id, "error")
            return False, updated_chunk

    def enhance(self, section_id: Optional[int] = None, wait_seconds: Optional[int] = None, dry_run: bool = False):
        """Enhance chunks."""
        state = self.load_state()
        chunks = state.get("chunks", [])
        
        if not chunks:
            self.log("No chunks found. Run 'init' first.", "enhance")
            return
        
        wait = wait_seconds or self.config["wait_seconds"]
        
        # Filter chunks
        if section_id:
            chunks_to_process = [c for c in chunks if c["id"] == section_id]
        else:
            chunks_to_process = [c for c in chunks if c.get("status") == "pending"]
        
        if not chunks_to_process:
            self.log("No chunks to enhance", "enhance")
            return
        
        self.log(f"Enhancing {len(chunks_to_process)} chunk(s)", "enhance")
        
        for chunk in chunks_to_process:
            success, updated_chunk = self.enhance_chunk(chunk, wait, dry_run)
            
            # Update state
            for i, c in enumerate(state["chunks"]):
                if c["id"] == updated_chunk["id"]:
                    state["chunks"][i] = updated_chunk
                    break
            
            self.save_state(state)

    def start(self, target_lines: Optional[int] = None, wait_seconds: Optional[int] = None, dry_run: bool = False):
        """Full automation - continuously enhance until target lines reached."""
        target = target_lines or self.config["target_lines"]
        wait = wait_seconds or self.config["wait_seconds"]
        
        self.log(f"Starting full automation (target: {target} lines)", "start", phase="begin")
        
        # Ensure init is done
        if not self.master_file.exists():
            self.log("master_prd.md not found. Running init...", "start", phase="init")
            self.init()
        
        # Build chunk map if needed
        state = self.load_state()
        if not state.get("chunks"):
            self.log("Building chunk map...", "start", phase="chunk_map")
            self.build_chunk_map()
            state = self.load_state()
        
        iteration = 0
        max_iterations = self.config.get("max_iterations", 1000)  # Safety limit
        
        while iteration < max_iterations:
            iteration += 1
            
            # Get current line count
            current_lines = len(self.master_file.read_text().splitlines())
            self.log(f"Iteration {iteration}: Current {current_lines} lines, target {target} lines", 
                    "start", phase=f"iter_{iteration}")
            
            if current_lines >= target:
                self.log(f"Target reached: {current_lines} lines", "start", phase="complete")
                break
            
            # Get pending chunks
            pending_chunks = [c for c in state["chunks"] if c.get("status") == "pending"]
            
            if not pending_chunks:
                # Rebuild chunk map (document may have grown, new sections added)
                self.log("No pending chunks, rebuilding chunk map...", "start", phase="rebuild")
                self.build_chunk_map()
                state = self.load_state()
                pending_chunks = [c for c in state["chunks"] if c.get("status") == "pending"]
                
                if not pending_chunks:
                    self.log("No more chunks to process", "start", phase="complete")
                    break
            
            # Process pending chunks (configurable batch size)
            chunks_per_batch = self.config.get("chunks_per_batch", 5)
            processed = 0
            for chunk in pending_chunks[:chunks_per_batch]:
                success, updated_chunk = self.enhance_chunk(chunk, wait, dry_run)
                
                # Update state
                for i, c in enumerate(state["chunks"]):
                    if c["id"] == updated_chunk["id"]:
                        state["chunks"][i] = updated_chunk
                        break
                
                self.save_state(state)
                
                if success:
                    processed += 1
                
                # Small delay between chunks
                if not dry_run:
                    import time
                    delay = self.config.get("delay_between_chunks_seconds", 2)
                    time.sleep(delay)
            
            if processed == 0:
                self.log("No chunks processed successfully, stopping", "start", phase="error")
                break
        
        final_lines = len(self.master_file.read_text().splitlines())
        self.log(f"Full automation complete: {final_lines} lines", "start", phase="complete")
        
        # Auto git sync if enabled
        if self.config.get("allow_git_auto", False) and not dry_run:
            self.log("Running git auto-sync...", "start", phase="git_sync")
            self.git_auto_sync()

    def retry(self, chunk_ids: List[int]):
        """Retry failed chunks."""
        state = self.load_state()
        
        for chunk_id in chunk_ids:
            for chunk in state["chunks"]:
                if chunk["id"] == chunk_id:
                    chunk["status"] = "pending"
                    chunk["last_error"] = None
                    chunk["attempts"] = 0
                    self.log(f"Reset chunk {chunk_id} to pending", "retry", chunk_id)
        
        self.save_state(state)

    def reset(self):
        """Clear state and optionally rotate logs."""
        if self.state_file.exists():
            backup_path = self.repo_root / f".auto_state.json.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.state_file.rename(backup_path)
            self.log(f"State file backed up to {backup_path.name}", "reset")
        
        # Create empty state
        state = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "master_file": str(self.master_file),
            "total_lines": 0,
            "chunks": []
        }
        self.save_state(state)
        self.log("State reset. Run 'init' to rebuild chunk map.", "reset")
        
        # Optionally rotate log
        if self.log_file.exists() and self.log_file.stat().st_size > 10 * 1024 * 1024:  # 10MB
            log_backup = self.repo_root / f"auto_master.log.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.log_file.rename(log_backup)
            self.log(f"Log file rotated to {log_backup.name}", "reset")

    def git_auto_sync(self):
        """Automatically add, commit, pull, and push changes."""
        if not self.config.get("allow_git_auto", False):
            self.log("Git automation is disabled in config. Set 'allow_git_auto': true to enable.", "git_sync")
            return
        
        try:
            # Check if we're in a git repo
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.repo_root,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                self.log("Not in a git repository. Skipping git sync.", "git_sync")
                return
            
            # Get status
            self.log("Checking git status...", "git_sync", phase="status")
            result = subprocess.run(
                ["git", "status", "--short"],
                cwd=self.repo_root,
                capture_output=True,
                text=True
            )
            changes = result.stdout.strip()
            
            if not changes:
                self.log("No changes to commit.", "git_sync", phase="status")
                return
            
            # Add relevant files
            files_to_add = [
                "master_prd.md",
                "auto_config.json",
                "auto_master.py",
                "auto_master.sh",
                "cursor_driver.scpt",
                "README.md",
                "AUTOMATION_README.md",
                "QUICK_START.md",
                "START_GUIDE.md",
                ".gitignore"
            ]
            
            added_files = []
            for file in files_to_add:
                file_path = self.repo_root / file
                if file_path.exists():
                    result = subprocess.run(
                        ["git", "add", file],
                        cwd=self.repo_root,
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        added_files.append(file)
            
            if not added_files:
                self.log("No files to add.", "git_sync", phase="add")
                return
            
            self.log(f"Added files: {', '.join(added_files)}", "git_sync", phase="add")
            
            # Count enhanced chunks for commit message
            state = self.load_state()
            done_chunks = len([c for c in state.get("chunks", []) if c.get("status") == "done"])
            current_lines = len(self.master_file.read_text().splitlines()) if self.master_file.exists() else 0
            
            # Create commit message
            commit_msg = f"chore(auto): update master_prd.md ({done_chunks} chunks enhanced, {current_lines} lines)"
            
            # Commit
            self.log("Creating commit...", "git_sync", phase="commit")
            result = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=self.repo_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
                    self.log("Nothing to commit.", "git_sync", phase="commit")
                else:
                    self.log(f"Commit failed: {result.stderr}", "git_sync", phase="commit")
                    return
            else:
                self.log(f"Committed: {commit_msg}", "git_sync", phase="commit")
            
            # Pull with rebase
            self.log("Pulling latest changes...", "git_sync", phase="pull")
            result = subprocess.run(
                ["git", "pull", "--rebase"],
                cwd=self.repo_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                self.log(f"Pull failed (this is OK if no remote is configured): {result.stderr}", "git_sync", phase="pull")
                self.log("You may need to pull manually or configure remote.", "git_sync", phase="pull")
            else:
                self.log("Pulled latest changes.", "git_sync", phase="pull")
            
            # Push
            self.log("Pushing changes...", "git_sync", phase="push")
            result = subprocess.run(
                ["git", "push"],
                cwd=self.repo_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                self.log(f"Push failed (this is OK if no remote is configured): {result.stderr}", "git_sync", phase="push")
                self.log("You may need to push manually or configure remote.", "git_sync", phase="push")
            else:
                self.log("Pushed changes successfully.", "git_sync", phase="push")
                
        except Exception as e:
            self.log(f"Git sync error (non-fatal): {str(e)}", "git_sync", phase="error")
            self.log("You can run git commands manually if needed.", "git_sync", phase="error")


def main():
    parser = argparse.ArgumentParser(description="PRD Master - Minimal Single-File PRD System")
    subparsers = parser.add_subparsers(dest="command")
    
    # init
    init_parser = subparsers.add_parser("init", help="Initialize master_prd.md")
    init_parser.add_argument("--description", type=str, help="Project description")
    
    # status
    status_parser = subparsers.add_parser("status", help="Show status")
    status_parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed chunk table")
    
    # enhance
    enhance_parser = subparsers.add_parser("enhance", help="Enhance chunks")
    enhance_parser.add_argument("--section", type=int, help="Section/chunk ID to enhance")
    enhance_parser.add_argument("--wait", type=int, help="Wait seconds")
    enhance_parser.add_argument("--dry-run", action="store_true")
    
    # start
    start_parser = subparsers.add_parser("start", help="Full automation")
    start_parser.add_argument("--target-lines", type=int, help="Target line count")
    start_parser.add_argument("--wait", type=int, help="Wait seconds")
    start_parser.add_argument("--dry-run", action="store_true")
    
    # retry
    retry_parser = subparsers.add_parser("retry", help="Retry failed chunks")
    retry_parser.add_argument("chunk_ids", type=int, nargs="+", help="Chunk IDs to retry")
    
    # reset
    subparsers.add_parser("reset", help="Clear state and reset")
    
    # git_sync
    subparsers.add_parser("git_sync", help="Manually trigger git sync (add/commit/pull/push)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Find repo root
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent
    
    master = PRDMaster(repo_root)
    
    if args.command == "init":
        master.init(getattr(args, 'description', None))
    elif args.command == "status":
        master.status(getattr(args, 'verbose', False))
    elif args.command == "enhance":
        master.enhance(getattr(args, 'section', None), getattr(args, 'wait', None), args.dry_run)
    elif args.command == "start":
        master.start(getattr(args, 'target_lines', None), getattr(args, 'wait', None), args.dry_run)
    elif args.command == "retry":
        master.retry(args.chunk_ids)
    elif args.command == "reset":
        master.reset()
    elif args.command == "git_sync":
        master.git_auto_sync()


if __name__ == "__main__":
    main()
