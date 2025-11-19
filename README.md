# PRD Auto Template – Quick Start

A universal, fully-automated PRD (Product Requirements Document) enhancement system that can grow a single master document to 100,000+ lines through AI-powered expansion.

## 🚀 One-Command Start (Recommended)

The easiest way to use this system is with the **Meta-Orchestrator Agent Prompt**:

1. **Open this repo in your AI IDE** (Cursor, Google AI Studio, Claude Desktop, etc.)
2. **Open a new chat**
3. **Copy the Agent Start Prompt**:
   - Open `prd.md`
   - Find section **"11. META-ORCHESTRATOR AGENT INSTRUCTIONS"**
   - Copy everything between `<!-- META_ORCHESTRATOR_PROMPT_START -->` and `<!-- META_ORCHESTRATOR_PROMPT_END -->`
4. **Paste it into your AI chat**
5. **Describe your app** in 2-5 sentences (e.g., "I want to build a mobile task management app with AI suggestions")
6. **Type**: `start`
7. **Let the AI orchestrate** the full automation pipeline hands-free

The Meta-Orchestrator will automatically:
- Initialize the system
- Grow your PRD to 100,000+ lines
- Generate implementation plans
- Implement code phases
- Handle all safety checks and error recovery

You can then use simple commands like:
- `status` - Check system status
- `regrow` - Continue growing the PRD
- `fix` - Diagnose and repair issues
- `implement phase 3.2.1` - Implement a specific phase
- `implement 5 tasks` - Implement multiple tasks

---

## Manual Usage (Advanced)

## Overview

This automation system can be added to any repository and used to generate and evolve a detailed PRD/prompt document. It supports:

- **Single master document** (`prd.md`) containing PRD content, role library, and prompt templates
- **Autonomous growth** towards configurable target sizes
- **AI integration** via Cursor IDE (macOS) or local stub mode
- **Git automation** for automatic commits and pushes (optional)
- **Universal design** - works for mobile apps, web apps, games, AI tools, backend services, etc.

## 1. Clone / Use as Template

### Option A: Use as GitHub Template

1. Create a new repository from this template on GitHub
2. Clone your new repository locally

### Option B: Add to Existing Project

1. Copy these files into your existing project repository:
   - `prd.md`
   - `auto_master.py`
   - `auto_config.json`
   - `auto_master.sh`
   - `cursor_driver.scpt` (optional, macOS only)
   - `.gitignore`
   - `LICENSE`

## 2. First-Time Setup

```bash
# Initialize the system (builds state from prd.md)
python3 auto_master.py init

# Sync Omni-Corp Role Library and Prompt Templates into prd.md
python3 auto_master.py sync_roles

# Check system status
python3 auto_master.py status --verbose
```

## 3. Configuration

Edit `auto_config.json` to customize:

- **Growth settings**: Target line count, max passes, chunks per pass
- **AI integration**: Enable Cursor driver (`use_cursor_driver: true`) or use local stub mode
- **Git automation**: Enable auto-commit/push (`git.enable_auto: true`)

### Example: Enable Cursor Integration (macOS)

```json
{
  "use_cursor_driver": true,
  "cursor_driver_path": "cursor_driver.scpt"
}
```

**Prerequisites for Cursor mode:**
- macOS operating system
- Cursor IDE installed
- macOS Accessibility permissions granted
- Cursor's "New Chat" shortcut configured (default: Cmd+Option+L)

### Example: Enable Git Automation

```json
{
  "git": {
    "enable_auto": true,
    "commit_after_each_pass": true,
    "push_after_each_pass": false,
    "pull_before_sync": true
  }
}
```

## 4. Growing the PRD

### Run One Pass (Debug/Testing)

```bash
# Process a limited number of chunks
python3 auto_master.py enhance --limit 2

# Dry-run to see what would happen
python3 auto_master.py enhance --limit 1 --dry-run
```

### Run Fully Automatic Growth Loop

```bash
# Start autonomous growth towards target line count
python3 auto_master.py grow
```

The `grow` command will:
- Run multiple enhancement passes
- Rebuild state as the document grows
- Process chunks using AI (Cursor or local stub)
- Optionally commit changes after each pass (if Git automation enabled)
- Stop when target reached, all chunks done, or max passes reached

## 5. Git Automation

### Check Git Status

```bash
# Show git repository and automation status
python3 auto_master.py git_status
```

### Manual Git Sync

```bash
# Manually sync changes to git (add, commit, push)
python3 auto_master.py git_sync
```

**Note:** `git_sync` respects `git.enable_auto` for safety. To enable automatic git operations, set `git.enable_auto: true` in `auto_config.json`.

### Automatic Git Sync

When `git.enable_auto: true` and `git.commit_after_each_pass: true`:
- The `grow` command will automatically commit after each pass
- Optionally push if `git.push_after_each_pass: true`
- Pull before sync if `git.pull_before_sync: true`

## 6. Commands Reference

| Command | Description |
|---------|-------------|
| `init` | Initialize system (build state from PRD) |
| `status` | Show system status (use `--verbose` for chunk details) |
| `start` / `enhance` | Run single enhancement pass (use `--limit N` to limit chunks) |
| `grow` | Run autonomous growth loop towards target line count |
| `reset` | Reset automation state (removes state and rotates logs) |
| `sync_roles` | Sync Omni-Corp Role Library and Prompt Templates into prd.md |
| `git_status` | Show git repository and automation status |
| `git_sync` | Manually sync changes to git (add, commit, push) |
| `doctor` | Run health check and diagnostics |
| `plan_impl` | Generate implementation plan from PRD |
| `impl_phase` | Implement a specific phase/task (requires `--phase`) |
| `impl_loop` | Run automated implementation loop for multiple tasks |
| `smoke_test` | Run smoke tests to verify system works |
| `benchmark_growth` | Measure PRD expansion performance |
| `benchmark_impl` | Test code generation pipeline |
| `deploy` | Deploy application to environment (requires `--env`) |
| `deploy_status` | Show deployment status for environment (requires `--env`) |
| `monitor` | Monitor application health and generate report |
| `security_check` | Check security configuration and status |
| `quick_test` | Run quick test suite (`--scope basic|full`) |

## 7. File Structure

### Core Files (Permanent)

- `prd.md` - Master PRD document (grows automatically)
- `auto_master.py` - Main automation orchestrator
- `auto_config.json` - Configuration file
- `auto_master.sh` - Shell wrapper (optional)
- `cursor_driver.scpt` - Cursor integration driver (macOS, optional)
- `.gitignore` - Git ignore rules
- `LICENSE` - License file
- `README.md` - This file

### Runtime Files (Git-ignored)

- `.auto_state.json` - Chunk and growth state
- `auto_master.log` - Detailed operation logs

## 8. Safety Features

- **Length ratio checks**: Ensures enhanced chunks don't lose content
- **Atomic file writes**: Prevents corruption during updates
- **State persistence**: Can resume after crashes
- **Error handling**: Failed chunks are marked, don't break the pipeline
- **Git safety**: Never force-pushes, checks for conflicts before pushing

## 9. Troubleshooting

### No chunks to process

If `status` shows all chunks as "done", you can:
- Reset state: `python3 auto_master.py reset` then `init`
- Or manually edit `prd.md` to add new content

### Git sync fails

- Check `git_status` to see repository state
- Ensure `git.enable_auto: true` if using automatic sync
- Verify remote and branch names in config match your repository

### Cursor integration not working

- Verify macOS Accessibility permissions
- Check Cursor's "New Chat" shortcut matches `cursor_driver.scpt`
- Use local stub mode (`use_cursor_driver: false`) for testing

## 10. Domain Packs & Presets

This template supports "Domain Packs" – reusable bundles of roles, prompts, and patterns for different kinds of projects:

- `generic_app` – General-purpose apps (default)
- `mobile_app` – Mobile-first apps (React Native / Flutter)
- `web_app` – Web/SaaS dashboards (Next.js / React)
- `game_2d` – 2D games (Unity / Godot)
- `ai_tool` – AI assistants and tools (Python / FastAPI)

When you describe your app to the Meta-Orchestrator and type `start`, it will:
- Infer an appropriate domain pack from your description
- Apply recommended roles and phase patterns
- Configure implementation settings (language/framework) where possible

You can customize domain packs and presets in:
- `auto_config.json` → `"domain_packs"` section
- `prd.md` → `# 15. DOMAIN PACKS & PRESETS`

## 11. Deployment & Environments

This template includes a generic model for deployment and runtime monitoring:

- Configure your environments and hooks in `auto_config.json` under `"deployment"`
- Use commands: `deploy --env <environment>`, `deploy_status --env <environment>`, `monitor`
- Works with any CI/CD system (GitHub Actions, GitLab CI, etc.) and cloud provider (AWS, GCP, Azure, etc.)

See `prd.md` Section 16 for detailed deployment documentation.

## 12. Security, Privacy & Testing

This template includes placeholders and patterns for:
- Security architecture (auth, authorization, rate limiting, secret handling)
- Privacy & data classification
- Compliance considerations (GDPR/CCPA/etc., project-specific)
- Testing strategy (unit/integration/security tests)

Configure defaults in `auto_config.json` under `"security"`, and document project-specific details in `prd.md` → `# 17. SECURITY, PRIVACY, COMPLIANCE & TESTING`.

## 13. App Factory Mode

This template can be used as an "App Factory" to manage multiple independent projects:

- Each app lives in its own repo using this template
- Use GitHub "Use this template" or `git clone` to create new repos
- Master Controller pattern (AI agent or script) can manage multiple projects
- See `prd.md` Section 14 for multi-project workflows

## 14. Advanced Usage

### Custom Growth Targets

Edit `auto_config.json`:

```json
{
  "growth": {
    "target_line_count": 50000,
    "max_passes": 100,
    "max_chunks_per_pass": 10
  }
}
```

### Integration with Existing Projects

This system is designed to work alongside existing codebases. The `prd.md` file can be:
- Kept in the project root
- Moved to a `docs/` directory (update `master_md_path` in config)
- Integrated into monorepo structures

## License

See `LICENSE` file for details.

## Support

For issues, questions, or contributions, please refer to the repository's issue tracker.

