# PRD Automation Quick Start Guide

## 🚀 Quick Start (One Command)

```bash
# ÖNEMLİ: Önce doğru dizine gidin
cd PRD_auto

# Full automation: creates/improves PRD, builds prd_enhanced.md
python3 tools/automation/prd_auto.py full_auto --wait 60
```

This single command will:
1. ✅ Create `prd.md` if it doesn't exist (from template)
2. ✅ Initialize the system (chunk PRD)
3. ✅ Process each chunk in Cursor (new chat tab per chunk)
4. ✅ Build `prd_enhanced.md` with all improvements
5. ✅ Log everything to `tools/automation/prd_auto.log`

## First-Time Setup

1. **Navigate to PRD_auto directory:**
   ```bash
   cd PRD_auto
   ```

2. **Initialize the system:**
   ```bash
   python3 tools/automation/prd_auto.py init
   ```
   This creates:
   - `tools/automation/prd_auto_config.json` (if missing)
   - `.prd_auto_state.json` (chunk state from your PRD)

3. **Check status:**
   ```bash
   # Basic summary
   python3 tools/automation/prd_auto.py status
   
   # Detailed table
   python3 tools/automation/prd_auto.py status --verbose
   ```

## Running Automation

### Full Automation (Recommended)
```bash
cd PRD_auto
python3 tools/automation/prd_auto.py full_auto --wait 60
```
- Creates `prd.md` if missing (from template)
- Initializes system automatically
- Processes all chunks through enhancement
- Builds single `prd_enhanced.md` file (no intermediate files)
- All transcripts saved to `tools/automation/enhanced_chunk_*.txt`

### Process All Pending Chunks (Normal Mode)
```bash
cd PRD_auto
python3 tools/automation/prd_auto.py run --wait 60
```
- Processes all `pending` chunks sequentially
- Waits 60 seconds after sending each chunk to Cursor
- Saves transcripts to `tools/automation/output_chunk_<id>.txt`
- Updates state after each chunk

### Process from a Specific Chunk
```bash
cd PRD_auto
python3 tools/automation/prd_auto.py run --from 5 --wait 60
```
Starts from chunk #5 (useful for resuming after interruption).

### Process Limited Chunks (Testing)
```bash
cd PRD_auto
python3 tools/automation/prd_auto.py run --limit 3 --wait 60
```
Processes only 3 chunks then stops (useful for testing).

### Dry-Run Mode (No Cursor Calls)
```bash
cd PRD_auto
python3 tools/automation/prd_auto.py full_auto --dry-run --limit 1
```
Simulates processing without actually calling Cursor. Useful for:
- Testing without Cursor set up
- Validating prompt composition
- Checking chunk boundaries

### Retry Failed Chunks
```bash
cd PRD_auto
# Normal mode
python3 tools/automation/prd_auto.py retry 3 4 5

# Enhancement mode
python3 tools/automation/prd_auto.py retry --mode=enhance 3 4 5
```
Resets chunks #3, #4, and #5 to `pending` status.

### Reset Everything
```bash
cd PRD_auto
python3 tools/automation/prd_auto.py reset
```
Rebuilds state from scratch (useful if PRD changed significantly). Does not delete outputs or logs.

### Enhance the Entire PRD
```bash
cd PRD_auto
python3 tools/automation/prd_auto.py enhance --wait 60
```
- Reuses existing chunk definitions
- Sends each chunk through the enhancement worker prompt
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

## What Happens During `full_auto`

1. **PRD Detection:**
   - Checks if `prd.md` exists
   - If missing, creates from `prd_template.md`

2. **Initialization:**
   - Splits PRD into chunks (default: 100 lines per chunk)
   - Saves chunk definitions to `.prd_enhance_state.json`

3. **Processing:**
   - For each pending chunk:
     - Opens new chat tab in Cursor (single window)
     - Sends chunk with enhancement prompt
     - Waits for AI response
     - Extracts improved chunk from transcript

4. **Output:**
   - Builds single `prd_enhanced.md` file
   - Saves transcripts to `tools/automation/enhanced_chunk_*.txt`
   - Logs everything to `tools/automation/prd_auto.log`

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
   - Saves transcript to `tools/automation/output_chunk_<id>.txt`
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
3. Extracts improved chunk and saves to memory
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

### "No such file or directory" Error
**Problem:** You're in the wrong directory.

**Solution:**
```bash
# Make sure you're in the PRD_auto directory
cd PRD_auto
pwd  # Should show: /path/to/auto_PRD/PRD_auto

# Then run commands
python3 tools/automation/prd_auto.py full_auto --wait 60
```

### Cursor Driver Fails
- Ensure Cursor is installed and accessible
- Grant macOS Automation permissions (System Settings → Privacy & Security → Accessibility)
- Check that `cursor_driver_new_chat.scpt` exists and is readable
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
- **Final Enhanced PRD:** `prd_enhanced.md` - complete enhanced PRD (when all chunks done)
- **Enhancement Notes:** `prd_enhanced_notes.md` - aggregated notes, assumptions, questions

## Example Workflow

```bash
# 1. Navigate to PRD_auto directory
cd PRD_auto

# 2. Initialize
python3 tools/automation/prd_auto.py init

# 3. Check what we have
python3 tools/automation/prd_auto.py status --verbose

# 4. Test with dry-run
python3 tools/automation/prd_auto.py full_auto --dry-run --limit 1

# 5. Process first few chunks
python3 tools/automation/prd_auto.py full_auto --wait 60 --limit 3

# 6. Check progress
python3 tools/automation/prd_auto.py status --verbose

# 7. If chunk #3 failed, retry it
python3 tools/automation/prd_auto.py retry --mode=enhance 3

# 8. Continue processing all chunks
python3 tools/automation/prd_auto.py full_auto --wait 60

# 9. Review the enhanced PRD
cat prd_enhanced.md
```

## Detailed Logging

All operations are logged to `tools/automation/prd_auto.log` with phase tracking:

```
[2025-01-10 12:34:56][full_auto][chunk=5][phase=prepare_prompt] Processing chunk 5 (lines 120-185, section="Feature A")
[2025-01-10 12:34:57][full_auto][chunk=5][phase=send_prompt] Sending chunk 5 to Cursor (new chat tab)
[2025-01-10 12:34:58][full_auto][chunk=5][phase=wait] Waiting 60 seconds for Cursor to respond
[2025-01-10 12:35:58][full_auto][chunk=5][phase=save_transcript] Saved transcript to tools/automation/enhanced_chunk_5.txt
[2025-01-10 12:35:58][full_auto][chunk=5][phase=parse_improved_chunk] Extracted improved chunk 5
[2025-01-10 12:35:58][full_auto][chunk=5][phase=update_state] Chunk 5 completed
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
4. Run `init`, then `full_auto`, and start capturing chunk-by-chunk improvements

The core automation code (`prd_auto.py`, `cursor_driver_new_chat.scpt`, worker prompts) is reusable across all projects.
