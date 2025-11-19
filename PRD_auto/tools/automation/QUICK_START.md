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
   python3 tools/automation/prd_auto.py status
   ```
   Shows all chunks and their status (pending/running/done/failed).

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

### Retry Failed Chunks
```bash
python3 tools/automation/prd_auto.py retry 3 4 5
```
Resets chunks #3, #4, and #5 to `pending` status.

### Reset Everything
```bash
python3 tools/automation/prd_auto.py reset
```
Rebuilds state from scratch (useful if PRD changed significantly).

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

### Chunks Stuck in "running"
- Manually reset: `python3 tools/automation/prd_auto.py retry <chunk_id>`
- Check logs: `tail -f tools/automation/prd_auto.log`

### PRD Changed
- Run `python3 tools/automation/prd_auto.py reset` to rebuild chunks
- Note: This will reset all chunk statuses

### Enhance the Entire PRD
```bash
python3 tools/automation/prd_auto.py enhance --wait 60
```
- Reuses the same chunks defined in `.prd_auto_state.json`.
- Sends each chunk through the enhancement worker prompt (with `<<<IMPROVED_CHUNK_*>>>` markers).
- Stores transcripts in `tools/automation/enhanced_chunk_<id>.txt`.
- Writes improved content to `tools/automation/improved_chunk_<id>.md`.
- When all chunks finish, concatenates into `prd_enhanced.md` and aggregates notes.

## Output Files

- **State:** `.prd_auto_state.json` - Chunk metadata, status, timestamps
- **Enhancement State:** `.prd_enhance_state.json` - Enhancement-specific metadata
- **Logs:** `tools/automation/prd_auto.log` - All operations logged
- **Transcripts:** `tools/automation/output_chunk_<id>.txt` - Cursor chat responses
- **Enhancement Transcripts:** `tools/automation/enhanced_chunk_<id>.txt`
- **Enhanced PRD:** `prd_enhanced.md` (+ optional `prd_enhanced_notes.md`)

## Example Workflow

```bash
# 1. Initialize
python3 tools/automation/prd_auto.py init

# 2. Check what we have
python3 tools/automation/prd_auto.py status

# 3. Process first 10 chunks (manually stop after testing)
python3 tools/automation/prd_auto.py run --from 1 --wait 45

# 4. Check progress
python3 tools/automation/prd_auto.py status

# 5. If chunk #3 failed, retry it
python3 tools/automation/prd_auto.py retry 3

# 6. Continue processing
python3 tools/automation/prd_auto.py run --wait 60

# 7. Enhance the PRD
python3 tools/automation/prd_auto.py enhance --wait 60
```

## Reusing in Other Projects

1. Copy the entire `tools/automation/` directory
2. Update `prd_auto_config.json` with project-specific settings
3. Place your `prd.md` in the repo root (or update `prd_path` in config)
4. Run `init` and start processing!

The core automation code (`prd_auto.py`, `cursor_driver.scpt`, `worker_prompt.md`) is reusable across all projects.

