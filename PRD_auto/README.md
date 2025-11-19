# PRD Master - Minimal Single-File PRD Automation System

A minimal, fully automatic PRD (Product Requirements Document) enhancement system that grows a single master Markdown file to 100,000+ lines through iterative AI-powered enhancement.

## 🎯 Core Philosophy

**ONE master .md file** contains everything:
- Product vision, requirements, architecture
- API design, data models, UX flows
- Implementation strategies, QA plans
- Prompt libraries for future AI agents
- Tasks, progress logs, architecture notes
- All documentation in one place

**MINIMAL file set** (max 5 files):
1. `master_prd.md` - The single source of truth
2. `auto_config.json` - Configuration
3. `auto_master.py` - Main automation script
4. `auto_master.sh` - Shell wrapper
5. `cursor_driver.scpt` - Cursor integration (optional)

## 🚀 Quick Start

### 1. Initialize

```bash
python3 auto_master.py init --description "Your app description here"
```

This creates `master_prd.md` with a comprehensive skeleton structure.

### 2. Check Status

```bash
python3 auto_master.py status
```

Shows chunk processing status, line counts, and progress.

### 3. Start Full Automation

```bash
python3 auto_master.py start
```

The system will:
- Process all chunks in `master_prd.md`
- Enhance each section iteratively
- Grow the document toward 100,000+ lines
- Never shrink or delete content (≥90% length preservation)

### 4. Manual Enhancement

```bash
# Enhance all pending chunks
python3 auto_master.py enhance

# Enhance specific chunk
python3 auto_master.py enhance --section 5

# Dry run (test without making changes)
python3 auto_master.py enhance --dry-run
```

### 5. Retry Failed Chunks

```bash
python3 auto_master.py retry 3 7 12
```

## 📋 Commands

| Command | Description |
|---------|-------------|
| `init [--description TEXT]` | Initialize `master_prd.md` if missing |
| `status` | Show processing status and progress |
| `start [--target-lines N] [--wait SEC] [--dry-run]` | Full automation mode |
| `enhance [--section N] [--wait SEC] [--dry-run]` | Enhance chunks manually |
| `retry CHUNK_IDS...` | Reset failed chunks to pending |

## ⚙️ Configuration (`auto_config.json`)

```json
{
  "master_md_path": "master_prd.md",
  "project_name": "PRD Master System",
  "chunk_strategy": "by_heading",
  "chunk_size_lines": 200,
  "min_chunk_lines": 50,
  "max_chunk_lines": 500,
  "wait_seconds": 60,
  "min_length_ratio": 0.90,
  "target_lines": 100000,
  "single_window_new_tab": true,
  "cursor_driver_path": "cursor_driver.scpt",
  "max_iterations": 1000,
  "chunks_per_batch": 5,
  "delay_between_chunks_seconds": 2
}
```

### Key Settings

- **`chunk_strategy`**: `"by_heading"` (split by `# 1.`, `# 2.` headings) or `"fixed_lines"` (fixed line ranges)
- **`min_length_ratio`**: Minimum length preservation (0.90 = 90% of original must be preserved)
- **`target_lines`**: Target document size (default: 100,000 lines)
- **`wait_seconds`**: Time to wait for AI response in Cursor

## 🛡️ Safety Guarantees

### Non-Destructive Enhancement

1. **Never shrinks content** - Enhanced chunks must be ≥90% of original length
2. **Never deletes lines** - All content is preserved, obsolete items marked `[DEPRECATED]`
3. **Processes all lines** - Every line belongs to exactly one chunk, no gaps or overlaps
4. **Validates before update** - Length checks prevent data loss

### Error Handling

- Failed chunks are marked `failed` and logged
- Original content is never modified if enhancement fails
- State is saved after each chunk to allow recovery
- Retry mechanism for failed chunks

## 📁 File Structure

```
PRD_auto/
├── master_prd.md          # Single master PRD (grows to 100k+ lines)
├── auto_config.json       # Configuration
├── auto_master.py         # Main automation script
├── auto_master.sh         # Shell wrapper
├── cursor_driver.scpt     # Cursor integration (macOS)
├── .auto_state.json       # Runtime state (git-ignored)
├── auto_master.log        # Log file (git-ignored)
└── .gitignore            # Git ignore rules
```

## 🔄 How It Works

### Chunking Strategy

**By Heading** (default):
- Splits document by top-level headings (`# 1.`, `# 2.`, etc.)
- Each section becomes one chunk
- Natural semantic boundaries

**Fixed Lines**:
- Splits into fixed-size chunks (e.g., 200 lines)
- Respects heading boundaries when possible
- Useful for very large documents

### Enhancement Process

1. **Load chunk** from `master_prd.md`
2. **Build prompt** with enhancement instructions
3. **Send to Cursor** via AppleScript (or API)
4. **Extract improved section** from transcript
5. **Validate length** (must be ≥90% of original)
6. **Update file** with improved content
7. **Save state** for recovery

### Iterative Growth

- Each chunk is enhanced multiple times as document grows
- New sections are automatically detected and added to chunk map
- System continues until target line count reached
- Can run overnight to generate comprehensive PRD

## 🎨 Master PRD Structure

The `master_prd.md` file contains these sections:

1. **Product Overview** - Vision, mission, goals
2. **Users & Use Cases** - Personas, stories, flows
3. **Functional Requirements** - Features, details, edge cases
4. **Non-Functional Requirements** - Performance, security, scalability
5. **Architecture** - System design, tech stack, patterns
6. **Data Models** - Entities, relationships, schema
7. **API Design** - Endpoints, formats, auth
8. **UX & Flows** - User flows, wireframes, components
9. **Implementation Strategy** - Phases, milestones, roadmap
10. **QA & Testing** - Strategy, test cases, QA processes
11. **Prompt Library** - Prompts for dev/UX/arch agents
12. **Tasks & Progress** - Current tasks, completed work, blockers
13. **Architecture Notes** - System design notes, technical decisions
14. **Implementation Notes** - Development notes, code patterns
15. **Progress Log** - Daily progress tracking
16. **Notes & Future Work** - Open questions, enhancements, deprecated items

## 🔧 Cursor Integration

The system uses AppleScript to interact with Cursor on macOS:

1. Activates existing Cursor window (no new window)
2. Opens new chat tab (Cmd+K)
3. Pastes enhancement prompt
4. Sends message
5. Waits for response
6. Copies transcript
7. Returns to Python for processing

**Requirements:**
- macOS with Cursor installed
- Cursor must be running
- Accessibility permissions may be required

## 📊 State Management

State is saved in `.auto_state.json`:

```json
{
  "version": "1.0",
  "created_at": "2025-01-XX...",
  "updated_at": "2025-01-XX...",
  "master_file": "master_prd.md",
  "total_lines": 1234,
  "chunks": [
    {
      "id": 1,
      "title": "Product Overview",
      "start_line": 1,
      "end_line": 150,
      "status": "done",
      "attempts": 1,
      "length_ratio": 1.15
    },
    ...
  ]
}
```

## 🐛 Troubleshooting

### Cursor not responding
- Ensure Cursor is running and frontmost
- Check AppleScript permissions in System Preferences
- Try increasing `wait_seconds` in config

### Chunks failing
- Check `auto_master.log` for error messages
- Verify chunk bounds are valid (file may have changed)
- Use `retry` command to reset failed chunks

### Content being lost
- Check `min_length_ratio` in config (should be 0.90+)
- Review logs for length validation warnings
- Failed chunks preserve original content

### Slow processing
- Reduce `chunks_per_batch` in config
- Increase `delay_between_chunks_seconds`
- Process chunks manually with `enhance --section N`

## 🎯 Use Cases

1. **New Project**: Start with `init`, describe your app, run `start`
2. **Existing PRD**: Place content in `master_prd.md`, run `init` to build chunk map
3. **Incremental Enhancement**: Use `enhance` to improve specific sections
4. **Overnight Generation**: Run `start` and let it work toward 100k lines

## 📝 License

See LICENSE file.

## 🤝 Contributing

This is a template system designed to be copied and customized for each project. Feel free to adapt it to your needs!
