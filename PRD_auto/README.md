# PRD Automation Template

This repository is a **complete automation system** for creating, improving, and maintaining Product Requirements Documents (PRDs) using AI assistance.

## 🚀 Quick Start

### Full Automation (Recommended)

```bash
# Start the complete automation pipeline
python3 tools/automation/prd_auto.py start --wait 60
```

This single command will:
1. ✅ Create `prd.md` if it doesn't exist (from template)
2. ✅ Read and analyze your PRD section by section
3. ✅ Open new chats in Cursor for each section
4. ✅ Improve each section using AI
5. ✅ Update `prd.md` with improvements
6. ✅ Clean up unnecessary files
7. ✅ Sync with GitHub (fetch, commit, push)

### What's Included

- **Auto-Improve System**: Automatically improves PRD sections using Cursor AI
- **PRD Template**: Auto-generates PRD structure if file doesn't exist
- **GitHub Integration**: Automatic fetch, merge, commit, and push
- **Cleanup Tools**: Removes unnecessary files automatically
- **Detailed Logging**: Comprehensive logs for all operations
- **Section-by-Section Processing**: Processes PRD in manageable sections
- **New Chat Per Section**: Opens fresh Cursor chat for each section

## 📚 Documentation

- **[START_GUIDE.md](START_GUIDE.md)** - Complete guide for the auto-improve system
- **[QUICK_START.md](QUICK_START.md)** - Quick reference for all commands
- **[AUTOMATION_README.md](AUTOMATION_README.md)** - Detailed automation documentation

## 🎯 Key Features

### 1. Automatic PRD Creation
If `prd.md` doesn't exist, the system creates it from a template automatically.

### 2. Section-by-Section Improvement
- Splits PRD into sections based on headings (##, ###)
- Processes each section independently
- Opens new Cursor chat for each section
- Preserves all original content and special markers

### 3. GitHub Integration
- Automatic `git fetch` and `pull`
- Automatic `git add`, `commit`, and `push`
- Custom commit messages
- Safe error handling

### 4. Cleanup
- Removes `__pycache__/` directories
- Removes `*.pyc`, `*.pyo` files
- Removes `.DS_Store` files
- Keeps repository clean

## 📖 Usage Examples

### Basic Usage
```bash
# Full automation - one command to rule them all (recommended)
python3 tools/automation/prd_auto.py full_auto --wait 60

# Full pipeline with cleanup and git (start command)
python3 tools/automation/prd_auto.py start --wait 60

# Only improve PRD (no Git, no cleanup)
python3 tools/automation/prd_auto.py full_auto --wait 60

# Test mode (dry-run)
python3 tools/automation/prd_auto.py full_auto --dry-run --limit 1
```

### Advanced Usage
```bash
# Custom commit message
python3 tools/automation/prd_auto.py start --commit-message "Update PRD with new features"

# Only cleanup
python3 tools/automation/prd_auto.py cleanup

# Only Git sync
python3 tools/automation/prd_auto.py git-sync --message "Manual update"
```

## 🔧 Requirements

- **Python 3.7+**
- **macOS** (for AppleScript automation)
- **Cursor** installed and running
- **macOS Automation Permissions** (System Settings → Privacy & Security → Accessibility)

## 📝 Commands

| Command | Description |
|---------|-------------|
| `full_auto` | **Main command**: Creates/improves PRD, builds prd_enhanced.md |
| `start` | Full pipeline: full_auto + cleanup + git-sync |
| `enhance` | Enhance existing PRD chunks |
| `run` | Process chunks (normal mode) |
| `git-sync` | Sync with GitHub (fetch, pull, commit, push) |
| `cleanup` | Remove unnecessary files |
| `init` | Initialize system (create chunks) |
| `status` | Show chunk status |
| `retry` | Retry failed chunks |
| `reset` | Reset state (rebuild chunks) |

## 🎓 Getting Started

1. **Clone or copy this repository**
   ```bash
   git clone your-repo
   cd your-repo
   ```

2. **Run the automation**
   ```bash
   # Recommended: Full automation
   python3 tools/automation/prd_auto.py full_auto --wait 60
   
   # Or: Full pipeline with cleanup and git
   python3 tools/automation/prd_auto.py start --wait 60
   ```

3. **Check the results**
   - View improved `prd.md`
   - Check logs: `tail -f tools/automation/prd_auto.log`
   - Verify Git commits: `git log`

## 🔍 How It Works

1. **PRD Detection**: Checks if `prd.md` exists, creates from template if missing
2. **Section Analysis**: Splits PRD into sections based on markdown headings
3. **AI Processing**: For each section:
   - Opens new Cursor chat
   - Sends section to AI for improvement
   - Extracts improved version
4. **PRD Update**: Replaces original sections with improved versions
5. **Cleanup**: Removes unnecessary files
6. **Git Sync**: Commits and pushes changes to GitHub

## 📋 File Structure

```
.
├── prd.md                          # Your PRD (auto-created if missing)
├── START_GUIDE.md                  # Complete usage guide
├── QUICK_START.md                  # Quick reference
├── AUTOMATION_README.md            # Detailed docs
├── README.md                       # This file
└── tools/
    └── automation/
        ├── prd_auto.py             # Main automation script
        ├── prd_auto_config.json    # Configuration
        ├── cursor_driver.scpt      # Cursor driver (reuse chat)
        ├── cursor_driver_new_chat.scpt  # Cursor driver (new chat)
        ├── prd_template.md         # PRD template
        ├── worker_prompt.md        # Worker prompt template
        └── worker_prompt_enhance.md # Enhancement prompt template
```

## 🛠️ Configuration

Edit `tools/automation/prd_auto_config.json`:

```json
{
  "project_name": "Your Project",
  "prd_path": "prd.md",
  "chunk_size_lines": 100,
  "default_wait_seconds": 60
}
```

## 🐛 Troubleshooting

### Cursor Not Responding
- Ensure Cursor is running
- Check macOS Automation permissions
- Try `--dry-run` to test without Cursor

### Git Errors
- Check Git configuration: `git config --list`
- Verify remote: `git remote -v`
- Use `--no-git` to skip Git operations

### Section Not Found
- Ensure PRD has proper markdown headings (##, ###)
- Check section name spelling
- Use `--dry-run` to see which sections are found

## 📊 Logging

All operations are logged to `tools/automation/prd_auto.log`:

```bash
# View logs
tail -f tools/automation/prd_auto.log

# Search logs
grep "auto-improve" tools/automation/prd_auto.log
```

## 🤝 Contributing

This is a template repository. Feel free to:
- Fork and customize for your needs
- Report issues
- Suggest improvements

## 📄 License

See [LICENSE](LICENSE) file.

---

**Ready to start?** Run: `python3 tools/automation/prd_auto.py full_auto --wait 60`

