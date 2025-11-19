# PRD Automation Quick Start Guide

## First-Time Setup

1. **Initialize the system:**
   ```bash
   python3 tools/automation/prd_auto.py init
   ```
   This creates:
   - `tools/automation/prd_auto_config.json` (if missing)
   - `.prd_auto_state.json` (chunk state from your PRD)

2. **Check status:**
   ```bash
   # Basic summary
   python3 tools/automation/prd_auto.py status
   
   # Detailed table
   python3 tools/automation/prd_auto.py status --verbose
   ```

## Running Automation

### Process All Pending Chunks
```bash
python3 tools/automation/prd_auto.py run --wait 60
```
- Processes all `pending` chunks sequentially
- Waits 60 seconds after sending each chunk to Cursor
- Saves transcripts to `tools/automation/output_chunk_<id>.txt`
- Updates state after each chunk

### Process from a Specific Chunk
```bash
python3 tools/automation/prd_auto.py run --from 5 --wait 60
```
Starts from chunk #5 (useful for resuming after interruption).

### Process Limited Chunks (Testing)
```bash
python3 tools/automation/prd_auto.py run --limit 3 --wait 60
```
Processes only 3 chunks then stops (useful for testing).

### Dry-Run Mode (No Cursor Calls)
```bash
python3 tools/automation/prd_auto.py run --dry-run --limit 1
```
Simulates processing without actually calling Cursor. Useful for:
- Testing without Cursor set up
- Validating prompt composition
- Checking chunk boundaries

### Retry Failed Chunks
```bash
# Normal mode
python3 tools/automation/prd_auto.py retry 3 4 5

# Enhancement mode
python3 tools/automation/prd_auto.py retry --mode=enhance 3 4 5
```
Resets chunks #3, #4, and #5 to `pending` status.

### Reset Everything
```bash
python3 tools/automation/prd_auto.py reset
```
Rebuilds state from scratch (useful if PRD changed significantly). Does not delete outputs or logs.

### Enhance the Entire PRD
```bash
python3 tools/automation/prd_auto.py enhance --wait 60
```
- Reuses existing chunk definitions
- Sends each chunk through the enhancement worker prompt
- Creates `tools/automation/improved_chunk_<id>.md` files
- Once all chunks are done, writes `prd_enhanced.md` (and optional `prd_enhanced_notes.md`)

**With options:**
```bash
# Resume from chunk 10
python3 tools/automation/prd_auto.py enhance --from 10 --wait 60

# Test with dry-run
python3 tools/automation/prd_auto.py enhance --dry-run --limit 1

# Process only 5 chunks
python3 tools/automation/prd_auto.py enhance --limit 5 --wait 60
```

## What Happens During `run`

For each pending chunk:

1. **Prompt Composition:**
   - Extracts project overview from PRD
   - Loads worker prompt template
   - Combines: Overview + Template + Chunk text

2. **Cursor Interaction:**
   - Activates Cursor app
   - Opens/reuses chat (based on `chat_strategy`)
   - Pastes the composed prompt
   - Sends it (simulates Enter key)
   - Waits for the specified duration
   - Selects all and copies the chat transcript

3. **State Management:**
   - Marks chunk as `running` → `done` (or `failed` on error)
   - Saves transcript to `output_chunk_<id>.txt`
   - Updates `.prd_auto_state.json` with metadata

## What Happens During `enhance`

Similar to `run`, but:

1. Uses `worker_prompt_enhance.md` template
2. Expects AI to wrap improved chunk between markers:
   ```
   <<<IMPROVED_CHUNK_START>>>
   ... improved markdown ...
   <<<IMPROVED_CHUNK_END>>>
   ```
3. Extracts improved chunk and saves to `improved_chunk_<id>.md`
4. Once all chunks are `done`, concatenates into `prd_enhanced.md`

## Configuration

Edit `tools/automation/prd_auto_config.json`:

```json
{
  "project_name": "Your Project",
  "prd_path": "prd.md",
  "chunk_size_lines": 100,
  "chat_strategy": "single_chat",
  "default_wait_seconds": 60
}
```

## Troubleshooting

### Cursor Driver Fails
- Ensure Cursor is installed and accessible
- Grant macOS Automation permissions (System Settings → Privacy & Security → Accessibility)
- Check that `cursor_driver.scpt` exists and is readable
- Try `--dry-run` to test without Cursor

### Chunks Stuck in "running"
- Manually reset: `python3 tools/automation/prd_auto.py retry <chunk_id>`
- Check logs: `tail -f tools/automation/prd_auto.log`

### PRD Changed
- Run `python3 tools/automation/prd_auto.py reset` to rebuild chunks
- Note: This will reset all chunk statuses

### Missing Markers in Enhancement
- Check `tools/automation/enhanced_chunk_<id>.txt` to see what Cursor returned
- Retry: `python3 tools/automation/prd_auto.py retry --mode=enhance <id>`

## Output Files

- **State:** `.prd_auto_state.json` - chunk metadata, status, timestamps (normal mode)
- **Enhancement State:** `.prd_enhance_state.json` - tracks enhancement progress
- **Logs:** `tools/automation/prd_auto.log` - all operations logged with phases
- **Transcripts:** `tools/automation/output_chunk_<id>.txt` - Cursor chat responses (normal)
- **Enhancement Transcripts:** `tools/automation/enhanced_chunk_<id>.txt` - Cursor chat responses (enhance)
- **Improved Chunks:** `tools/automation/improved_chunk_<id>.md` - individual enhanced chunks
- **Final Enhanced PRD:** `prd_enhanced.md` - complete enhanced PRD (when all chunks done)
- **Enhancement Notes:** `prd_enhanced_notes.md` - aggregated notes, assumptions, questions

## Example Workflow

```bash
# 1. Initialize
python3 tools/automation/prd_auto.py init

# 2. Check what we have
python3 tools/automation/prd_auto.py status --verbose

# 3. Test with dry-run
python3 tools/automation/prd_auto.py run --dry-run --limit 1

# 4. Process first few chunks
python3 tools/automation/prd_auto.py run --limit 3 --wait 60

# 5. Check progress
python3 tools/automation/prd_auto.py status --verbose

# 6. If chunk #3 failed, retry it
python3 tools/automation/prd_auto.py retry 3

# 7. Continue processing
python3 tools/automation/prd_auto.py run --wait 60

# 8. Once ready, enhance the PRD
python3 tools/automation/prd_auto.py enhance --wait 60

# 9. Check enhancement status
python3 tools/automation/prd_auto.py status --mode=enhance --verbose

# 10. Review the enhanced PRD
cat prd_enhanced.md
```

## Detailed Logging

All operations are logged to `tools/automation/prd_auto.log` with phase tracking:

```
[2025-01-10 12:34:56][run][chunk=5][phase=prepare_prompt] Processing chunk 5 (lines 120-185, section="Feature A")
[2025-01-10 12:34:57][run][chunk=5][phase=send_prompt] Sending chunk 5 to Cursor
[2025-01-10 12:34:58][run][chunk=5][phase=wait] Waiting 60 seconds for Cursor to respond
[2025-01-10 12:35:58][run][chunk=5][phase=save_transcript] Saved transcript to tools/automation/output_chunk_5.txt
[2025-01-10 12:35:58][run][chunk=5][phase=update_state] Chunk 5 completed
```

View logs in real-time:
```bash
tail -f tools/automation/prd_auto.log
```

## Status Output Examples

**Basic status:**
```
[2025-01-10 12:34:56][status] Chunk status summary (run mode):
[2025-01-10 12:34:56][status] Total chunks: 42
[2025-01-10 12:34:56][status] pending: 35, done: 5, failed: 2
```

**Verbose status:**
```
ID    Section                                  Lines          Status       Attempts  Result          Updated
--------------------------------------------------------------------------------------------------------------------
1     Sample Productivity Companion            1-100          done         1         ok              2025-01-10 12:30:15
2     Project Overview                         101-200        done         1         ok              2025-01-10 12:31:22
3     Goals & Non-Goals                        201-300        failed       2         cursor_error    2025-01-10 12:32:10
...
```

## Reusing in Other Projects

1. Copy the entire `tools/automation/` directory
2. Update `prd_auto_config.json` with project-specific settings
3. Replace `prd.md` with your own PRD (or adjust `prd_path` in the config)
4. Run `init`, then `run`, and start capturing chunk-by-chunk improvements

The core automation code (`prd_auto.py`, `cursor_driver.scpt`, worker prompts) is reusable across all projects.
