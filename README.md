# Universal PRD Automation Template

A minimal, open-source template for creating comprehensive Product Requirements Documents (PRDs) and generating implementation plans using AI assistance.

## What Is This?

This template provides:

- **One-file PRDs** (`prd.md`) that also act as prompt libraries and technical manuals
- **Automated PRD growth** using AI to expand from a simple idea to 100,000+ lines of detailed specifications
- **Structured implementation planning** that maps PRD phases to concrete code modules
- **Code generation scaffolding** for progressive implementation
- **Deployment, security, performance, and analytics** frameworks built-in

**Key Philosophy**: Everything lives in `prd.md` - specs, prompts, roles, progress, and history - making it the single source of truth for your project.

## Using This Repo as a Template

This repository is designed to be used as a **GitHub template**.

### Quick Start

1. **Click "Use this template"** on GitHub
2. **Create a new repository** (private or public)
3. **Clone your new repository locally**:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>
   ```

4. **Run a quick validation**:
   ```bash
   python3 auto_master.py init
   python3 auto_master.py validate --dry-run
   ```

5. **Open `prd.md`** and start describing your application using the prompts and sections provided

6. **Use your IDE's AI assistant** together with the Meta-Orchestrator instructions inside `prd.md` to:
   - Grow the PRD
   - Plan implementation
   - Generate code

### What Happens Next

After creating a project from this template:

- The template core files are copied to your new repository
- You can start customizing `auto_config.json` for your project
- You can begin expanding `prd.md` with your project-specific content
- Runtime files (`.auto_state.json`, `auto_master.log`) will be generated as you use the automation
- You can add your application code in `src/`, `app/`, or other directories

For detailed instructions, see:
- `prd.md` → `# 24. TEMPLATE PACKAGING & GITHUB PUBLISHING`
- `prd.md` → `# 0. HOW TO READ THIS DOCUMENT` (Quick Start)

## Quick Start

### 1. Clone or Use as Template

**Option A: Use GitHub Template** (Recommended)
1. Click "Use this template" on GitHub
2. Create your new repository
3. Clone locally: `git clone <your-repo-url>`

**Option B: Clone and Customize**
```bash
git clone <this-repo> my-app
cd my-app
```

### 2. Install Requirements

- **Python 3.x** (3.8+ recommended)
- **(Optional) Cursor IDE** (for macOS, enables AI automation)
- **(Optional) Your AI IDE of choice** (Claude Desktop, Google AI Studio, etc.)

### 3. Configure Your Project

Edit `auto_config.json`:

```json
{
  "implementation": {
    "primary_target_type": "mobile",  // or "web", "game", "backend", "ai_tool"
    "primary_language": "typescript",
    "primary_framework": "react_native"
  },
  "domain_packs": {
    "default_pack": "mobile_app"
  }
}
```

Edit `prd.md` Section 1:
- Update project name and description
- Add your app idea (2-5 sentences)

### 4. Initialize Automation

```bash
python3 auto_master.py init
python3 auto_master.py status
```

### 5. Let the AI Drive (Recommended)

1. **Open this repo in your AI IDE** (Cursor, Claude Desktop, etc.)
2. **Open `prd.md`**, find Section 11: "META-ORCHESTRATOR AGENT INSTRUCTIONS"
3. **Copy the complete prompt** between `<!-- META_ORCHESTRATOR_PROMPT_START -->` and `<!-- META_ORCHESTRATOR_PROMPT_END -->`
4. **Paste it into a new AI chat**
5. **Describe your app idea** in natural language (e.g., "I want to build a mobile task management app with AI suggestions")
6. **Type**: `start`

The AI will automatically:
- Initialize the system
- Sync role library
- Grow your PRD to detailed specifications
- Generate implementation plans
- Suggest next steps

### 6. Or Use Manual Commands

```bash
python3 auto_master.py sync_roles    # Sync role library
python3 auto_master.py grow          # Expand PRD (runs multiple passes)
python3 auto_master.py plan_impl     # Generate implementation plan
python3 auto_master.py impl_phase --phase 3.2.1  # Generate code for a phase
```

## Key Files

| File | Purpose |
|------|---------|
| `prd.md` | **Single master document** - PRD, prompts, roles, progress, everything |
| `auto_master.py` | CLI orchestrator - all automation commands |
| `auto_config.json` | Configuration - paths, AI, domain packs, deployment, security, performance, analytics |
| `auto_master.sh` | Shell wrapper (optional convenience) |
| `cursor_driver.scpt` | Cursor IDE automation bridge (macOS, optional) |
| `README.md` | This file - quick start guide |
| `.gitignore` | Git ignore rules |
| `LICENSE` | License file |

**Runtime Files** (git-ignored):
- `.auto_state.json` - Automation state (can be rebuilt)
- `auto_master.log` - Operation logs

## Common Commands

```bash
# Initialization & Status
python3 auto_master.py init              # Initialize system
python3 auto_master.py status            # Show status
python3 auto_master.py doctor            # Health check

# PRD Growth
python3 auto_master.py sync_roles        # Sync roles
python3 auto_master.py grow              # Grow PRD
python3 auto_master.py enhance --limit 2 # Process 2 chunks

# Implementation
python3 auto_master.py plan_impl                    # Generate plan
python3 auto_master.py impl_phase --phase 3.2.1     # Implement phase

# Evaluation & Diagnostics
python3 auto_master.py smoke_test        # Quick verification
python3 auto_master.py security_check    # Security check
python3 auto_master.py perf_status       # Performance status

# Help
python3 auto_master.py --help            # Show all commands
```

## Documentation

**For Quick Orientation**:
- **This README.md** - Quick start and common commands
- **`prd.md` Section 0** - How to read the master document
- **`prd.md` Section 20** - Developer experience and onboarding

**For Deep Dives**:
- **`prd.md` Section 11** - Meta-Orchestrator instructions (for AI-driven workflows)
- **`prd.md` Section 12** - Evaluation and benchmarks
- **`prd.md` Section 13** - Governance and contribution
- **`prd.md` Sections 15-19** - Domain packs, deployment, security, performance, analytics

## Features

### Domain Packs
Pre-configured bundles for different project types:
- `mobile_app` - Mobile-first apps (React Native, Flutter)
- `web_app` - Web/SaaS dashboards (Next.js, React)
- `game_2d` - 2D games (Unity, Godot)
- `ai_tool` - AI assistants and tools (Python, FastAPI)
- `backend_service` - Backend APIs (Node.js, Python, Go)
- And more...

### Deployment & Monitoring
Generic deployment model supporting any cloud provider and CI/CD system.

### Security & Privacy
Built-in security architecture, data classification, and compliance frameworks.

### Performance & Cost
Configuration knobs for AI usage, chunk sizes, and cost optimization.

### Analytics & Feedback
Structured frameworks for event tracking, KPIs, experiments, and user feedback.

## Extensions & Long-Term Evolution

This template has a **minimal core** on purpose:

**Core Files** (managed by template maintainers):
- `prd.md` – single master spec & prompt library
- `auto_master.py` – CLI orchestrator
- `auto_config.json` – configuration
- `auto_master.sh`, `cursor_driver.scpt`, `.gitignore`, `LICENSE`, `README.md` – repo hygiene

**To Extend the System**:

1. **Add Project-Specific Scripts**:
   - Create scripts in `tools/` or `scripts/` directories
   - Use `auto_master.py` commands as your API
   - Register in `auto_config.json` under `"extensions.known_extensions"`

2. **Document Extensions**:
   - Document in `prd.md` → `# 21. EXTENSIBILITY, PLUGINS & LONG-TERM EVOLUTION`
   - Include: purpose, usage, dependencies

3. **Follow Extension Protocols**:
   - Use core as API (call commands, don't replace them)
   - Respect core safety constraints
   - Keep extensions in designated zones

**Example Extension**:
```bash
#!/bin/bash
# scripts/ci_helper.sh - Example extension

python3 auto_master.py doctor
python3 auto_master.py smoke_test
python3 auto_master.py security_check --dry-run
```

**Commands**:

```bash
# Show configured extensions and whether their files exist
python3 auto_master.py extensions_status

# Check for missing or undocumented extensions (conceptual)
python3 auto_master.py extensions_doctor
```

**Evolution**:
- Core template uses Semantic Versioning (see `prd.md` Section 13.2)
- Breaking changes require MAJOR version bump
- Extensions evolve independently
- See `prd.md` Section 21 for extension patterns and evolution rules

## AI Providers & Tools

This template is **AI-provider-agnostic**. It can work with:

- **IDE-based assistants** (Cursor, Google AI agent, VSCode AI, etc.)
- **Remote LLM APIs** (OpenAI, Anthropic, etc.)
- **Local models** (Ollama, local LLM, etc.)
- **Stub mode** (no AI, for validation and manual workflows)

### Configuration

Configure AI strategy in `auto_config.json` under `"ai"`:

- **Choose a `default_provider`**: Primary AI provider to use
- **Describe available `providers`**: Catalog of configured providers
- **Define `task_routing`**: Map tasks (PRD growth, code generation, evaluation) to providers
- **Set `execution_modes`**: Control what's allowed (IDE-only, API calls, local models)

### Example Configuration

```json
{
  "ai": {
    "enabled": true,
    "default_provider": "cursor",
    "execution_modes": {
      "allow_ide_only": true,
      "allow_api_calls": false,
      "allow_local_models": false
    },
    "task_routing": {
      "prd_growth": {
        "preferred_provider": "cursor",
        "fallback_providers": ["openai"]
      }
    }
  }
}
```

### Commands

```bash
# Show AI providers, routing, and execution modes
python3 auto_master.py ai_status

# Summarize AI usage policy (what's allowed and what isn't)
python3 auto_master.py ai_policy
```

### Meta-Orchestrator Commands

The Meta-Orchestrator also supports chat commands:

- `ai status` - Show current AI configuration
- `ai policy` - Explain AI usage policy
- `optimize ai usage` - Suggest AI usage optimizations
- `prefer offline mode` - Configure for offline/local AI
- `prefer cheap models` - Optimize for cost

### Provider Setup

**IDE Integration** (Cursor, etc.):
- No additional setup required
- Uses IDE's built-in AI capabilities
- Configured via `cursor_driver.scpt` (macOS + Cursor)

**API Providers** (OpenAI, Anthropic):
- Set API keys via environment variables
- Set `execution_modes.allow_api_calls=true`
- Configure provider details in `ai.providers`

**Local Models**:
- Install local model (e.g., Ollama)
- Set `execution_modes.allow_local_models=true`
- Configure model endpoint in `ai.providers.local_llm`

**Note**: Provider-specific secrets and API keys are **not** stored in this repository. Configure them via environment variables or secure configuration files.

### Documentation

For detailed AI strategy and configuration, see:
- `prd.md` → `# 22. AI PROVIDERS, MODEL STRATEGY & TOOL INTEGRATION`

## How to Test This Template in Your Environment

After cloning or creating a new project from this template, you can run a **safe validation dry-run** to make sure everything is wired correctly.

### Quick Validation

```bash
# 1. Initialize state
python3 auto_master.py init

# 2. Check status
python3 auto_master.py status

# 3. Run full validation in dry-run mode (no destructive changes)
python3 auto_master.py validate --dry-run
```

This will:
- ✅ Verify `prd.md` structure
- ✅ Exercise growth and implementation planning in non-destructive mode
- ✅ Run basic health checks
- ✅ Check AI and extensions configuration
- ✅ Verify Git integration (if enabled)
- ✅ Log everything to `auto_master.log`

### Review Results

**In Terminal**:
- Validation summary shows success/warnings/failures
- Detailed output for each check

**In Logs**:
- `auto_master.log` contains detailed operation logs
- Look for `[VALIDATION]` and `[DRY_RUN]` entries

**In PRD**:
- `prd.md` → `# 23. VALIDATION, DRY-RUNS & EXPERIMENT LOG`
- Validation runs table tracks all validation cycles

### Individual Command Testing

You can also test individual commands in dry-run mode:

```bash
# Test PRD growth (dry-run)
python3 auto_master.py grow --dry-run

# Test implementation planning (dry-run)
python3 auto_master.py plan_impl --dry-run

# Test phase implementation (dry-run)
python3 auto_master.py impl_phase --phase 3.2.1 --dry-run

# Test Git sync (dry-run)
python3 auto_master.py git_sync --dry-run
```

### Safety Guarantees

**Dry-Run Mode**:
- ✅ Never modifies `prd.md` destructively
- ✅ Never commits to git
- ✅ Never deploys anything
- ✅ Never creates unexpected files
- ✅ Only logs what would happen

**Validation Command**:
- ✅ Always runs in dry-run mode
- ✅ Safe to run multiple times
- ✅ No data loss risk
- ✅ Can be run in CI/CD

### Troubleshooting

If validation fails:
1. Check `auto_master.log` for detailed error messages
2. Run `python3 auto_master.py doctor` for diagnostics
3. Review `prd.md` Section 23 for validation guidelines
4. See `prd.md` Section 20 (DX & Onboarding) for troubleshooting

For more details, see:
- `prd.md` → `# 23. VALIDATION, DRY-RUNS & EXPERIMENT LOG`

## Files You Should Not Commit

The automation system generates some runtime files which should stay **local**:

- `.auto_state.json` - Automation state (per project)
- `auto_master.log` - Automation log
- Temporary outputs (`.tmp`, `.temp` files)

These are already listed in `.gitignore`.

**If you see them staged in `git status`, remove them before committing:**

```bash
git rm --cached .auto_state.json auto_master.log
```

**Note**: These files are safe to delete - they will be regenerated when you run automation commands.

## Upgrading an Existing Project When the Template Evolves

Over time, this template may get new features or fixes.

### Upgrade Process

1. **Inspect changes** in the template repository:
   - Check release notes or changelog
   - Review new version tag or release notes

2. **Backup your project**:
   ```bash
   git commit -a -m "Backup before template upgrade"
   git branch backup-before-upgrade
   ```

3. **Manually copy or cherry-pick updates** for:
   - `auto_master.py` - Replace with new version
   - `auto_config.json` - Merge carefully with your local modifications
   - `prd.md` - Update only template sections (Sections 0, 11-24); keep your project-specific content (Sections 1-9)
   - `.gitignore`, `README.md` - Update if relevant

4. **Run validation**:
   ```bash
   python3 auto_master.py template_check
   python3 auto_master.py validate --dry-run
   ```

5. **Fix any reported issues** and commit the changes:
   ```bash
   git add .
   git commit -m "Upgrade template to v1.0.0"
   ```

### What to Update

**Always Update**:
- `auto_master.py` - Core automation code
- Template sections in `prd.md` (Sections 0, 11-24)

**Merge Carefully**:
- `auto_config.json` - Preserve your project-specific settings
- `README.md` - Merge template updates with your project-specific content

**Never Overwrite**:
- Your project-specific PRD content (Sections 1-9 in `prd.md`)
- Your application source code
- Your project-specific scripts and tools

For detailed upgrade instructions, see:
- `prd.md` → `# 24. TEMPLATE PACKAGING & GITHUB PUBLISHING` (Section 24.7)

## Optional: Sandbox & Experiments

This template includes a **Sandbox** concept for trying new ideas without breaking the core.

### What is the Sandbox?

The Sandbox is an optional, experimental space for:
- Testing new automation commands
- Experimenting with different chunking or AI strategies
- Trying future ideas safely
- Recording results for potential promotion to core

### Key Features

- **Disabled by default**: Sandbox is off unless explicitly enabled
- **Clearly labeled**: All experimental features are marked as such
- **Isolated**: Experiments don't affect core behavior
- **Documented**: All experiments are logged in `prd.md` Section 25

### How to Use

**Enable Sandbox**:
1. Edit `auto_config.json`
2. Set `"sandbox.enabled": true`
3. Optionally enable specific experimental flags

**Check Status**:
```bash
python3 auto_master.py sandbox_status
```

**Learn More**:
```bash
python3 auto_master.py sandbox_explain
```

**Log Experiments**:
- Use Meta-Orchestrator: `log experiment EXP-XXX`
- Or manually add to `prd.md` → `# 25. EXPERIMENTS, SANDBOX MODES & FUTURE IDEAS`

### Safety

- Sandbox features never run automatically
- Core template behavior is never modified by sandbox features
- Experiments are clearly marked in logs and output
- Sandbox can be disabled entirely if not needed

### When to Use

**Use Sandbox If**:
- You want to try experimental features
- You're contributing improvements to the template
- You're testing new ideas before promoting them

**Don't Use Sandbox If**:
- You just want to use the template normally
- You need stable, production-ready features
- You're not comfortable with experimental code

**Note**: If you are not actively experimenting, you can safely ignore the sandbox features. The template works perfectly fine without them.

For detailed information, see:
- `prd.md` → `# 25. EXPERIMENTS, SANDBOX MODES & FUTURE IDEAS`

## Troubleshooting

**System seems broken?**
```bash
python3 auto_master.py doctor    # Diagnose issues
tail -n 100 auto_master.log      # Check logs
```

**Common issues**:
- State corrupted: `python3 auto_master.py init` (rebuilds state)
- Config invalid: `python -m json.tool auto_config.json` (validate JSON)
- Need help: See `prd.md` Section 20.3 (FAQ) and Section 20.6 (Troubleshooting Guide)

## License

See `LICENSE` file for details.

## Support

For issues, questions, or contributions:
- Check `prd.md` Section 20 (Developer Experience) for detailed guidance
- Review `prd.md` Section 13 (Governance) for contribution guidelines
- See repository's issue tracker (if applicable)
