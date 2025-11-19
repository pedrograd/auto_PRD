# PRD Automation System

This repository is a **universal PRD automation template** that anyone can clone and use in their own projects. It reads a long `prd.md`, sends it to an AI assistant (Cursor) in chunks, and optionally generates an enhanced `prd_enhanced.md`.

## What This Repo Is

A complete automation system that:
- Splits your PRD into deterministic chunks
- Sends each chunk to Cursor via AppleScript automation
- Tracks progress in JSON state files
- Optionally enhances the entire PRD and rebuilds it from improved chunks
- Provides detailed logging and CLI controls

## How to Use in Your Own Project

### Option A: Use as GitHub Template

1. Click "Use this template" on GitHub
2. Clone your new repository
3. Replace `prd.md` with your own PRD
4. Update `tools/automation/prd_auto_config.json` (project name, PRD path, etc.)
5. Run `python3 tools/automation/prd_auto.py init`

### Option B: Copy into Existing Repo

1. Copy the `tools/automation/` directory into your repo
2. Copy `AUTOMATION_README.md` and `QUICK_START.md` to your repo root
3. Write your own `prd.md`
4. Update `tools/automation/prd_auto_config.json` with your project settings
5. Run `python3 tools/automation/prd_auto.py init`

## File Overview

**At repo root:**
- `prd.md` – Your Product Requirements Document (sample included)
- `AUTOMATION_README.md` – This file (main documentation)
- `QUICK_START.md` – Quick reference guide
- `.gitignore` – Ignores state files, logs, and generated outputs
- `README.md` – Project overview (optional)
- `LICENSE` – License file (optional)

**Under `tools/automation/`:**
- `prd_auto.py` – Main orchestrator script (CLI)
- `prd_auto.sh` – Shell wrapper: `python3 tools/automation/prd_auto.py "$@"`
- `prd_auto_config.json` – Repo-specific settings
- `worker_prompt.md` – Worker instruction template for normal runs
- `worker_prompt_enhance.md` – Specialized template for PRD enhancement
- `cursor_driver.scpt` – AppleScript driver for Cursor/Antigravity on macOS
- `QUICK_START.md` – Quick-start focused on automation CLI

**Runtime files (auto-generated, ignored by git):**
- `.prd_auto_state.json` – Chunk state for normal runs
- `.prd_enhance_state.json` – Chunk state for enhancement runs
- `tools/automation/prd_auto.log` – Detailed operation logs
- `tools/automation/output_chunk_*.txt` – Chat transcripts (normal mode)
- `tools/automation/enhanced_chunk_*.txt` – Chat transcripts (enhancement mode)
- `tools/automation/improved_chunk_*.md` – Individual improved chunks
- `prd_enhanced.md` – Final enhanced PRD (generated when all chunks done)
- `prd_enhanced_notes.md` – Aggregated notes from enhancement

## Requirements

- **Python**: Python 3.7 or higher
- **macOS**: Required for AppleScript automation (Cursor driver)
- **Cursor or Antigravity**: AI coding assistant that supports AppleScript automation
- **Permissions**: macOS Automation permissions must be granted (System Settings → Privacy & Security → Accessibility)

## Configuring `prd_auto_config.json`

Update these fields for your project:

```json
{
  "project_name": "Your Project Name",
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
```

**Key settings:**
- `project_name`: Human-friendly name
- `prd_path`: Path to your PRD (relative to repo root)
- `chunk_size_lines`: Lines per chunk (100 is a good default)
- `chat_strategy`: `single_chat` (reuse same chat) or `multi_chat` (new tab per chunk)
- `default_wait_seconds`: How long to wait for Cursor response (60+ recommended)

## Structuring `prd.md`

For best automation results:

1. **Include a "Project Overview" section** near the top. The orchestrator extracts this and prepends it to every chunk.
2. **Use clear headings** (`#`, `##`, `###`) to give chunks contextual section names.
3. **Keep content self-contained** where possible (avoid code blocks that rely on context outside the chunk).
4. **Add an "Automation Hints" section** (optional) with special instructions for automated processing.

See the included `prd.md` for an example structure.

## CLI Commands

### `init` – Initialize System

```bash
python3 tools/automation/prd_auto.py init
```

- Creates default `prd_auto_config.json` if missing
- Builds initial chunking of `prd.md` and writes `.prd_auto_state.json`
- Detects existing `prd_enhanced.md` if present

### `status` – Show Status

```bash
# Basic summary
python3 tools/automation/prd_auto.py status

# Detailed table of all chunks
python3 tools/automation/prd_auto.py status --verbose

# Show enhancement status instead
python3 tools/automation/prd_auto.py status --mode=enhance --verbose
```

**Example verbose output:**
```
[2025-01-10 12:34:56][status] Chunk status summary (run mode):
[2025-01-10 12:34:56][status] Total chunks: 42
[2025-01-10 12:34:56][status] pending: 35, done: 5, failed: 2

ID    Section                                  Lines          Status       Attempts  Result          Updated
--------------------------------------------------------------------------------------------------------------------
1     Sample Productivity Companion            1-100          done         1         ok              2025-01-10 12:30:15
2     Project Overview                         101-200        done         1         ok              2025-01-10 12:31:22
3     Goals & Non-Goals                        201-300        failed       2         cursor_error    2025-01-10 12:32:10
...
```

### `run` – Process Chunks (Normal Mode)

```bash
# Process all pending chunks
python3 tools/automation/prd_auto.py run --wait 60

# Start from chunk 5
python3 tools/automation/prd_auto.py run --from 5 --wait 60

# Process only 3 chunks (testing)
python3 tools/automation/prd_auto.py run --limit 3 --wait 60

# Dry-run (simulate without calling Cursor)
python3 tools/automation/prd_auto.py run --dry-run --limit 1
```

**What happens:**
1. Reads chunk text + project overview
2. Builds worker prompt from `worker_prompt.md`
3. Sends to Cursor via AppleScript
4. Waits `--wait` seconds
5. Copies entire chat transcript
6. Saves to `tools/automation/output_chunk_<id>.txt`
7. Updates `.prd_auto_state.json`

### `enhance` – Enhance PRD Chunks

```bash
# Enhance all chunks
python3 tools/automation/prd_auto.py enhance --wait 60

# Resume from chunk 10
python3 tools/automation/prd_auto.py enhance --from 10 --wait 60

# Test with dry-run
python3 tools/automation/prd_auto.py enhance --dry-run --limit 1
```

**What happens:**
1. Uses enhancement worker template (`worker_prompt_enhance.md`)
2. Expects AI to wrap improved chunk between markers:
   ```
   <<<IMPROVED_CHUNK_START>>>
   ... improved markdown ...
   <<<IMPROVED_CHUNK_END>>>
   ```
3. Saves transcripts to `tools/automation/enhanced_chunk_<id>.txt`
4. Extracts improved chunk to `tools/automation/improved_chunk_<id>.md`
5. Once all chunks are `done`, concatenates into `prd_enhanced.md`
6. Aggregates notes into `prd_enhanced_notes.md`

### `retry` – Reset Failed Chunks

```bash
# Retry specific chunks (normal mode)
python3 tools/automation/prd_auto.py retry 3 4 5

# Retry in enhancement mode
python3 tools/automation/prd_auto.py retry --mode=enhance 3 4 5
```

Resets chunks back to `pending` status so they can be reprocessed.

### `reset` – Rebuild State

```bash
python3 tools/automation/prd_auto.py reset
```

Rebuilds `.prd_auto_state.json` from `prd.md`. Does not delete outputs or logs (they remain as historical artifacts).

## Detailed Logging

All operations are logged to both stdout and `tools/automation/prd_auto.log` with phase tracking:

```
[2025-01-10 12:34:56][run][chunk=5][phase=prepare_prompt] Processing chunk 5 (lines 120-185, section="Feature A")
[2025-01-10 12:34:57][run][chunk=5][phase=send_prompt] Sending chunk 5 to Cursor
[2025-01-10 12:34:58][run][chunk=5][phase=wait] Waiting 60 seconds for Cursor to respond
[2025-01-10 12:35:58][run][chunk=5][phase=save_transcript] Saved transcript to tools/automation/output_chunk_5.txt
[2025-01-10 12:35:58][run][chunk=5][phase=update_state] Chunk 5 completed
```

**Log phases:**
- `prepare_prompt` – Building prompt from template
- `send_prompt` – Invoking Cursor driver
- `wait` – Waiting for response
- `copy_transcript` – Copying chat transcript
- `save_transcript` – Saving transcript file
- `parse_improved_chunk` – Extracting improved chunk (enhance mode)
- `update_state` – Updating state file
- `error` – Error occurred (with details)

## Dry-Run Mode

Use `--dry-run` to test without actually calling Cursor:

```bash
python3 tools/automation/prd_auto.py run --dry-run --limit 1
python3 tools/automation/prd_auto.py enhance --dry-run --limit 1
```

**What dry-run does:**
- Builds prompts normally
- Logs what would be sent
- Creates mock transcript files
- Marks chunks as `skipped_dry_run` in state
- Never calls AppleScript/Cursor

Useful for:
- Testing the system without Cursor set up
- Validating prompt composition
- Checking chunk boundaries

## Error Handling

The system handles errors gracefully:

- **Missing Cursor driver**: Clear error message with setup instructions
- **AppleScript failure**: Chunk marked as `failed` with `cursor_error` result
- **Missing markers (enhance)**: Chunk marked as `failed` with `parse_error` result
- **Timeout**: Clear timeout message with suggestion to increase `--wait`

All errors are logged with:
- Which chunk failed
- Which phase failed
- What went wrong
- What to do next (e.g., "Use 'retry <id>' to retry")

## Outputs & Monitoring

**State files:**
- `.prd_auto_state.json` – Tracks normal run progress
- `.prd_enhance_state.json` – Tracks enhancement progress

**Logs:**
- `tools/automation/prd_auto.log` – All operations with timestamps and phases

**Transcripts:**
- `tools/automation/output_chunk_<id>.txt` – Full Cursor chat transcripts (normal)
- `tools/automation/enhanced_chunk_<id>.txt` – Full Cursor chat transcripts (enhance)

**Enhanced outputs:**
- `tools/automation/improved_chunk_<id>.md` – Individual improved chunks
- `prd_enhanced.md` – Final concatenated enhanced PRD (when all chunks done)
- `prd_enhanced_notes.md` – Aggregated notes, assumptions, open questions

## Troubleshooting

### Cursor Driver Fails

**Symptoms:** Error message about missing driver or AppleScript failure

**Solutions:**
1. Ensure Cursor is installed and running
2. Grant macOS Automation permissions:
   - System Settings → Privacy & Security → Accessibility
   - Add Cursor (or Terminal) to allowed apps
3. Check that `cursor_driver.scpt` exists and is readable
4. Try `--dry-run` to test without Cursor

### Chunks Stuck in "running"

**Symptoms:** Chunks remain in `running` status after interruption

**Solutions:**
```bash
# Reset specific chunks
python3 tools/automation/prd_auto.py retry <chunk_id>

# Check logs for details
tail -f tools/automation/prd_auto.log
```

### PRD Changed

**Symptoms:** Chunk boundaries no longer match PRD

**Solution:**
```bash
python3 tools/automation/prd_auto.py reset
```

Note: This rebuilds state but does NOT delete outputs/logs (they remain as historical artifacts).

### Missing Markers in Enhancement

**Symptoms:** Enhancement fails with "Could not find improved chunk markers"

**Solutions:**
1. Check `tools/automation/enhanced_chunk_<id>.txt` to see what Cursor returned
2. Ensure `worker_prompt_enhance.md` clearly instructs about markers
3. Retry the chunk: `python3 tools/automation/prd_auto.py retry --mode=enhance <id>`

## Enhancement Flow Details

The `enhance` command creates a professional, improved version of your PRD:

1. **Reuses chunk definitions** from `.prd_auto_state.json` (same boundaries as normal runs)
2. **Sends each chunk** through `worker_prompt_enhance.md` which enforces:
   - Improved chunk wrapped in `<<<IMPROVED_CHUNK_START/END>>>` markers
   - Notes section with assumptions, open questions, prompt candidates
3. **Stores intermediate files:**
   - Transcripts: `tools/automation/enhanced_chunk_<id>.txt`
   - Improved chunks: `tools/automation/improved_chunk_<id>.md`
   - Notes: `tools/automation/improved_chunk_<id>_notes.md`
4. **Assembles final outputs** (when all chunks are `done`):
   - `prd_enhanced.md` – Complete enhanced PRD in correct order
   - `prd_enhanced_notes.md` – All notes aggregated by chunk

Enhancement progress is tracked separately in `.prd_enhance_state.json`, so you can:
- Interrupt and resume safely
- Mix normal runs and enhancements
- Retry failed enhancement chunks independently

## Mega PRD Transformation Prompt

When you want to restructure an existing, messy `prd.md` into the single-source-of-truth format, open a fresh Cursor chat (with the repo loaded) and paste the following prompt:

```
You are a senior product architect and AI prompt engineer.

Your task is to transform my existing `prd.md` into a **single-source-of-truth** document that is:

- Professional and well structured,
- Compatible with an external automation system (`prd_auto.py`) that processes the PRD in chunks,
- A complete reference for BOTH:
  - product documentation, and
  - application prompt definitions (prompt library).

### INPUT FILE

- There is an existing `prd.md` in this repository.
- It may be very long (tens of thousands of lines).
- It already contains a lot of content (notes, requirements, ideas, sometimes messy).

### GOAL STRUCTURE

Reshape the PRD into the following sections (keep numbering):

0. Metadata & Index
1. Project Overview
2. Product Scope
3. Core Use Cases
4. Features
5. UX & Flows
6. Technical Architecture
7. AI & Behaviour
8. Analytics & Experiments
9. Prompt Library (global + feature-level prompts)
10. Automation Hints (for external tools)
11. Risks, Open Questions, Future Work

(You can add subsections as needed, but keep this top-level outline.)

### RULES

1. **Preserve Meaning, Do Not Delete Information**
   - Do NOT throw away existing content.
   - You may rewrite, reorganize, merge, split, or move text to a better section.
   - If something seems obsolete or duplicated, mark it as:
     `[DEPRECATED] <reason>`
   - If you need to infer or invent reasonable details, mark them as:
     `[ASSUMPTION] <assumed detail>`

2. **Enhance and Professionalize**
   - Improve wording, clarity, and structure.
   - Turn vague notes into explicit requirements and user stories.
   - For each major feature, add:
     - User Stories
     - Functional Requirements
     - Non-Functional Requirements
     - Edge Cases
     - Analytics / events
   - Write in clear, professional product language.

3. **Prompt Library (Section 9)**
   - Identify any existing prompts in the current `prd.md` (system, user, tool, etc.) and move them into a dedicated **Prompt Library** section.
   - Normalize them into a consistent format:

     ### PROMPT: <Human Name>
     - ID: `<machine_id_like_this>`
     - Scope: <where in the app this is used>
     - Type: system | user | tool | few-shot | etc.

     ```prompt
     <the actual prompt text here>
     ```

   - For each major feature and important flow, create **at least one** well-designed prompt (if missing).
   - These prompts should be ready to plug into the app.

4. **Automation Hints (Section 10)**
   - Add a short section explaining to external tools (like `prd_auto.py`):
     - That the document is long and will be processed in chunks.
     - That all `[ASSUMPTION]`, `[OPEN_QUESTION]`, `[DEPRECATED]` tags must be preserved.
     - That Section 9 is the main Prompt Library.
   - This section should be written in plain English, as instructions to an automation system.

5. **Open Questions and Assumptions**
   - Whenever you see ambiguity, missing decisions, or conflicting requirements, add:
     `[OPEN_QUESTION] <clearly describe the issue>`
   - At the end, create a consolidated list in Section 11.

### OUTPUT

- Produce a **complete, enhanced version of `prd.md`**, in Markdown, following the structure above.
- The output should be large and detailed; it can be tens of thousands of lines if needed.
- You may generate additional useful detail where appropriate, but always mark pure inventions as `[ASSUMPTION]`.
```

Use it as a one-time restructuring tool or run it periodically to keep the PRD clean.

## Example Workflow

```bash
# 1. First-time setup
python3 tools/automation/prd_auto.py init
python3 tools/automation/prd_auto.py status --verbose

# 2. Test with dry-run
python3 tools/automation/prd_auto.py run --dry-run --limit 1

# 3. Process a few chunks
python3 tools/automation/prd_auto.py run --limit 3 --wait 60

# 4. Check progress
python3 tools/automation/prd_auto.py status --verbose

# 5. If chunk #3 failed, retry it
python3 tools/automation/prd_auto.py retry 3

# 6. Continue processing
python3 tools/automation/prd_auto.py run --wait 60

# 7. Once all chunks are done, enhance the PRD
python3 tools/automation/prd_auto.py enhance --wait 60

# 8. Check enhancement status
python3 tools/automation/prd_auto.py status --mode=enhance --verbose

# 9. Review the enhanced PRD
cat prd_enhanced.md
```

## Reusing in Other Projects

1. Copy the entire `tools/automation/` directory
2. Copy `AUTOMATION_README.md` and `QUICK_START.md` to your repo root
3. Update `tools/automation/prd_auto_config.json` with project-specific settings
4. Write your own `prd.md` (or adjust `prd_path` in config)
5. Run `python3 tools/automation/prd_auto.py init`
6. Start processing with `python3 tools/automation/prd_auto.py run --wait 60`

The core automation code (`prd_auto.py`, `cursor_driver.scpt`, worker prompts) is reusable across all projects.
