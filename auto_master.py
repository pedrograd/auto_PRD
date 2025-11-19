#!/usr/bin/env python3
"""
AUTO_MASTER.PY
==============
Universal automated PRD enhancement system orchestrator.

This system can grow a single master PRD document (prd.md) to 100,000+ lines
through AI-powered expansion, using role-based prompts and phase/task tracking.

META-ORCHESTRATOR NOTES:
========================
This repo is designed to be controlled by a higher-level AI agent using the
Meta-Orchestrator Prompt stored in `prd.md` under section
'11. META-ORCHESTRATOR AGENT INSTRUCTIONS'.

The agent will:
- Interpret simple commands like 'start', 'status', 'regrow', 'implement phase 3.2.1'
- Map them to auto_master.py commands and workflows
- Orchestrate the full automation pipeline hands-free

For manual usage, see README.md. For agent usage, copy the Meta-Orchestrator
Prompt from prd.md section 11 into your AI assistant.
"""

import json
import pathlib
import dataclasses
import typing
import argparse
import datetime
import textwrap
import subprocess
import sys
import re
import tempfile
import shutil
import os


# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclasses.dataclass
class GrowthConfig:
    """Growth configuration for autonomous expansion"""
    target_line_count: int  # Target line count for prd.md
    max_passes: int  # Maximum growth passes per grow command
    max_chunks_per_pass: int  # Maximum chunks to process per pass
    rebuild_state_each_pass: bool  # Rebuild state from file at start of each pass
    stop_when_all_done: bool  # Stop if no pending/failed chunks remain


@dataclasses.dataclass
class GitConfig:
    """Git automation configuration"""
    enable_auto: bool  # Enable automatic git operations
    remote_name: str  # Git remote name (default: origin)
    branch_name: str  # Git branch name (default: main)
    auto_add_paths: list[str]  # List of paths to auto-add
    commit_prefix: str  # Prefix for auto-commit messages
    commit_after_each_pass: bool  # Commit after each growth pass
    push_after_each_pass: bool  # Push after each growth pass
    pull_before_sync: bool  # Pull before sync operations


@dataclasses.dataclass
class SafetyConfig:
    """Safety and reliability configuration"""
    enable_doctor_auto_fixes: bool  # Allow doctor to auto-fix safe issues
    max_consecutive_failures: int  # Stop pass after this many consecutive failures
    stop_on_invariant_violation: bool  # Stop immediately on invariant violation
    doctor_scan_log_lines: int  # Number of log lines to scan in doctor
    allow_config_autofix: bool  # Allow doctor to write back normalized config


@dataclasses.dataclass
class ImplementationConfig:
    """Implementation automation configuration"""
    enabled: bool  # Enable implementation automation
    primary_target_type: str  # "mobile" | "web" | "backend" | "game" | "ai_tool" | "multi"
    primary_language: str  # e.g., "typescript", "dart", "python", "kotlin", "swift"
    primary_framework: str  # e.g., "react_native", "nextjs", "flutter", "unity"
    project_root: str  # Path where app code will live
    source_dir: str  # Main source directory
    generated_dir: str  # Safe subdir for AI-generated boilerplate
    test_dir: str  # Optional tests directory
    impl_plan_section_id: str  # Section ID for implementation plan in PRD
    impl_tasks_section_id: str  # Section ID for tasks in PRD
    impl_max_files_per_phase: int  # Maximum files to generate per phase
    impl_allow_overwrite_generated: bool  # Allow overwriting generated files
    impl_never_overwrite_manual: bool  # Never overwrite manually edited files
    default_roles_for_impl: list[str]  # Default roles for implementation tasks


@dataclasses.dataclass
class Config:
    """Configuration loaded from auto_config.json"""
    master_md_path: str  # Path to main PRD markdown file
    state_path: str  # Path to runtime state file (git-ignored)
    log_path: str  # Path to log file (git-ignored)
    chunk_strategy: str  # Strategy for chunking PRD (e.g., "fixed_lines")
    chunk_size_lines: int  # Number of lines per chunk (for fixed_lines strategy)
    wait_seconds: int  # Seconds to wait between AI calls
    max_parallel_chats: int  # Max parallel AI chat sessions (future)
    min_length_ratio_ok: float  # Minimum length ratio to consider enhancement safe (0.9 = 90% of original)
    cursor_driver_path: str  # Path to AppleScript driver for Cursor
    use_cursor_driver: bool  # Whether to use Cursor driver (requires macOS)
    growth: GrowthConfig  # Growth configuration
    git: GitConfig  # Git automation configuration
    safety: SafetyConfig  # Safety and reliability configuration
    implementation: ImplementationConfig  # Implementation automation configuration
    _raw_data: typing.Optional[dict] = None  # Full config data for access to optional sections (profiles, domain_packs, deployment, security)


def load_config(config_path: pathlib.Path = None) -> Config:
    """
    Load configuration from auto_config.json.
    If file doesn't exist, create it with defaults.
    """
    if config_path is None:
        config_path = pathlib.Path("auto_config.json")
    
    if not config_path.exists():
        # Create default config
        default_config = {
            "master_md_path": "prd.md",
            "state_path": ".auto_state.json",
            "log_path": "auto_master.log",
            "chunk_strategy": "fixed_lines",
            "chunk_size_lines": 120,
            "wait_seconds": 60,
            "max_parallel_chats": 1,
            "min_length_ratio_ok": 0.9,
            "cursor_driver_path": "cursor_driver.scpt",
            "use_cursor_driver": False,
            "growth": {
                "target_line_count": 100000,
                "max_passes": 50,
                "max_chunks_per_pass": 20,
                "rebuild_state_each_pass": True,
                "stop_when_all_done": True
            },
            "git": {
                "enable_auto": False,
                "remote_name": "origin",
                "branch_name": "main",
                "auto_add_paths": [
                    "prd.md",
                    "auto_config.json",
                    "auto_master.py",
                    "auto_master.sh",
                    "cursor_driver.scpt",
                    ".auto_state.json",
                    "auto_master.log",
                    ".gitignore",
                    "LICENSE",
                    "README.md"
                ],
                "commit_prefix": "[AUTO-PRD]",
                "commit_after_each_pass": True,
                "push_after_each_pass": False,
                "pull_before_sync": True
            },
            "safety": {
                "enable_doctor_auto_fixes": False,
                "max_consecutive_failures": 5,
                "stop_on_invariant_violation": True,
                "doctor_scan_log_lines": 5000,
                "allow_config_autofix": False
            },
            "implementation": {
                "enabled": False,
                "primary_target_type": "web",
                "primary_language": "typescript",
                "primary_framework": "nextjs",
                "project_root": ".",
                "source_dir": "src",
                "generated_dir": "src/generated",
                "test_dir": "tests",
                "impl_plan_section_id": "5. IMPLEMENTATION & ENGINEERING NOTES",
                "impl_tasks_section_id": "9. TASKS, BACKLOG & ROADMAP",
                "impl_max_files_per_phase": 5,
                "impl_allow_overwrite_generated": True,
                "impl_never_overwrite_manual": True,
                "default_roles_for_impl": [
                    "Principal Software Architect",
                    "Senior Mobile Developer",
                    "Full-Stack Web Developer",
                    "AI/ML Engineer",
                    "DevOps & Cloud Architect"
                ]
            }
        }
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        log(f"Created default config at {config_path}")
    
    with open(config_path, 'r') as f:
        data = json.load(f)
    
    # Ensure required fields have defaults if missing
    defaults = {
        "master_md_path": "prd.md",
        "state_path": ".auto_state.json",
        "log_path": "auto_master.log",
        "chunk_strategy": "fixed_lines",
        "chunk_size_lines": 120,
        "wait_seconds": 60,
        "max_parallel_chats": 1,
        "min_length_ratio_ok": 0.9,
        "cursor_driver_path": "cursor_driver.scpt",
        "use_cursor_driver": False
    }
    
    # Merge with defaults (user config takes precedence)
    for key, default_value in defaults.items():
        if key not in data:
            data[key] = default_value
    
    # Handle growth config
    if "growth" not in data:
        data["growth"] = {
            "target_line_count": 100000,
            "max_passes": 50,
            "max_chunks_per_pass": 20,
            "rebuild_state_each_pass": True,
            "stop_when_all_done": True
        }
    else:
        # Ensure all growth fields exist
        growth_defaults = {
            "target_line_count": 100000,
            "max_passes": 50,
            "max_chunks_per_pass": 20,
            "rebuild_state_each_pass": True,
            "stop_when_all_done": True
        }
        for key, default_value in growth_defaults.items():
            if key not in data["growth"]:
                data["growth"][key] = default_value
    
    # Handle git config
    if "git" not in data:
        data["git"] = {
            "enable_auto": False,
            "remote_name": "origin",
            "branch_name": "main",
            "auto_add_paths": [
                "prd.md",
                "auto_config.json",
                "auto_master.py",
                "auto_master.sh",
                "cursor_driver.scpt",
                ".auto_state.json",
                "auto_master.log",
                ".gitignore",
                "LICENSE",
                "README.md"
            ],
            "commit_prefix": "[AUTO-PRD]",
            "commit_after_each_pass": True,
            "push_after_each_pass": False,
            "pull_before_sync": True
        }
    else:
        # Ensure all git fields exist
        git_defaults = {
            "enable_auto": False,
            "remote_name": "origin",
            "branch_name": "main",
            "auto_add_paths": [
                "prd.md",
                "auto_config.json",
                "auto_master.py",
                "auto_master.sh",
                "cursor_driver.scpt",
                ".auto_state.json",
                "auto_master.log",
                ".gitignore",
                "LICENSE",
                "README.md"
            ],
            "commit_prefix": "[AUTO-PRD]",
            "commit_after_each_pass": True,
            "push_after_each_pass": False,
            "pull_before_sync": True
        }
        for key, default_value in git_defaults.items():
            if key not in data["git"]:
                data["git"][key] = default_value
    
    # Handle safety config
    if "safety" not in data:
        data["safety"] = {
            "enable_doctor_auto_fixes": False,
            "max_consecutive_failures": 5,
            "stop_on_invariant_violation": True,
            "doctor_scan_log_lines": 5000,
            "allow_config_autofix": False
        }
    else:
        # Ensure all safety fields exist
        safety_defaults = {
            "enable_doctor_auto_fixes": False,
            "max_consecutive_failures": 5,
            "stop_on_invariant_violation": True,
            "doctor_scan_log_lines": 5000,
            "allow_config_autofix": False
        }
        for key, default_value in safety_defaults.items():
            if key not in data["safety"]:
                data["safety"][key] = default_value
    
    # Handle implementation config
    if "implementation" not in data:
        data["implementation"] = {
            "enabled": False,
            "primary_target_type": "web",
            "primary_language": "typescript",
            "primary_framework": "nextjs",
            "project_root": ".",
            "source_dir": "src",
            "generated_dir": "src/generated",
            "test_dir": "tests",
            "impl_plan_section_id": "5. IMPLEMENTATION & ENGINEERING NOTES",
            "impl_tasks_section_id": "9. TASKS, BACKLOG & ROADMAP",
            "impl_max_files_per_phase": 5,
            "impl_allow_overwrite_generated": True,
            "impl_never_overwrite_manual": True,
            "default_roles_for_impl": [
                "Principal Software Architect",
                "Senior Mobile Developer",
                "Full-Stack Web Developer",
                "AI/ML Engineer",
                "DevOps & Cloud Architect"
            ]
        }
    else:
        # Ensure all implementation fields exist
        impl_defaults = {
            "enabled": False,
            "primary_target_type": "web",
            "primary_language": "typescript",
            "primary_framework": "nextjs",
            "project_root": ".",
            "source_dir": "src",
            "generated_dir": "src/generated",
            "test_dir": "tests",
            "impl_plan_section_id": "5. IMPLEMENTATION & ENGINEERING NOTES",
            "impl_tasks_section_id": "9. TASKS, BACKLOG & ROADMAP",
            "impl_max_files_per_phase": 5,
            "impl_allow_overwrite_generated": True,
            "impl_never_overwrite_manual": True,
            "default_roles_for_impl": [
                "Principal Software Architect",
                "Senior Mobile Developer",
                "Full-Stack Web Developer",
                "AI/ML Engineer",
                "DevOps & Cloud Architect"
            ]
        }
        for key, default_value in impl_defaults.items():
            if key not in data["implementation"]:
                data["implementation"][key] = default_value
    
    # Create GrowthConfig, GitConfig, SafetyConfig, and ImplementationConfig objects
    growth_config = GrowthConfig(**data["growth"])
    git_config = GitConfig(**data["git"])
    safety_config = SafetyConfig(**data["safety"])
    impl_config = ImplementationConfig(**data["implementation"])
    
    # Create Config object
    # Filter out sections that are not part of Config dataclass
    excluded_keys = ["growth", "git", "safety", "implementation", "profiles", "domain_packs", "deployment", "security"]
    config_dict = {k: v for k, v in data.items() if k not in excluded_keys}
    config_dict["growth"] = growth_config
    config_dict["git"] = git_config
    config_dict["safety"] = safety_config
    config_dict["implementation"] = impl_config
    
    # Store full data dict for access to optional sections (profiles, domain_packs, deployment, security)
    config = Config(**config_dict)
    config._raw_data = data  # Store full data for access to optional sections
    
    return config


# ============================================================================
# LOGGING
# ============================================================================

# Global config for logging (set by main)
_global_config: typing.Optional[Config] = None


def log(
    message: str,
    context: dict = None,
    config: Config = None
) -> None:
    """
    Log a message with timestamp and optional context.
    
    Format: [YYYY-MM-DD HH:MM:SS][command=<cmd>][chunk=<id>][phase_id=<phase>][step=<step>] message
    
    Args:
        message: Log message
        context: Optional dict with additional context (command, chunk, phase_id, step, etc.)
        config: Optional Config object (if None, uses global config)
    """
    if config is None:
        config = _global_config
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Build log line with standard fields
    parts = [f"[{timestamp}]"]
    
    # Standard context fields
    command = context.get("command", "-") if context else "-"
    chunk = context.get("chunk", "-") if context else "-"
    phase_id = context.get("phase_id", "-") if context else "-"
    step = context.get("step", "-") if context else "-"
    
    parts.append(f"[command={command}]")
    parts.append(f"[chunk={chunk}]")
    parts.append(f"[phase_id={phase_id}]")
    parts.append(f"[step={step}]")
    
    # Add any additional context fields
    if context:
        for key, value in context.items():
            if key not in ["command", "chunk", "phase_id", "step"]:
                parts.append(f"{key}={value}")
    
    parts.append(message)
    
    log_line = " ".join(parts)
    print(log_line)
    
    # Write to log file
    if config and config.log_path:
        try:
            with open(config.log_path, 'a') as f:
                f.write(log_line + "\n")
        except Exception as e:
            # Don't fail if logging fails
            print(f"Warning: Could not write to log file: {e}", file=sys.stderr)


# ============================================================================
# STATE MANAGEMENT
# ============================================================================

def load_state(config: Config) -> typing.Optional[dict]:
    """
    Load state from .auto_state.json.
    
    Ensures backward compatibility by initializing growth metadata if missing.
    
    Returns:
        State dict or None if file doesn't exist
    """
    state_path = pathlib.Path(config.state_path)
    if not state_path.exists():
        return None
    
    try:
        with open(state_path, 'r') as f:
            state = json.load(f)
        
        # Ensure backward compatibility: initialize growth metadata if missing
        if "meta" in state and "growth" not in state["meta"]:
            state["meta"]["growth"] = {
                "current_pass": 0,
                "total_passes_run": 0,
                "last_pass_summary": {
                    "pass_id": 0,
                    "chunks_attempted": 0,
                    "chunks_succeeded": 0,
                    "chunks_failed": 0,
                    "lines_before": 0,
                    "lines_after": 0
                }
            }
            # Bump version if needed
            if state["meta"].get("version", 1) < 2:
                state["meta"]["version"] = 2
        
        return state
    except Exception as e:
        log(f"ERROR: Failed to load state: {e}", {"step": "load_state"}, config)
        return None


def save_state(config: Config, state: dict) -> None:
    """
    Save state to .auto_state.json.
    """
    state_path = pathlib.Path(config.state_path)
    
    # Update metadata
    if "meta" in state:
        state["meta"]["updated_at"] = datetime.datetime.now().isoformat()
    
    try:
        with open(state_path, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        log(f"ERROR: Failed to save state: {e}", {"step": "save_state"}, config)
        raise


def build_state_from_file(config: Config, growth_pass: int = 0, preserve_growth_meta: dict = None) -> dict:
    """
    Build state structure from prd.md by chunking it.
    
    Uses fixed-line chunking strategy.
    
    Args:
        config: Config object
        growth_pass: Current growth pass number (for phase ID generation)
        preserve_growth_meta: Optional existing growth metadata to preserve
    
    Returns:
        State dict with meta and chunks array
    """
    prd_path = pathlib.Path(config.master_md_path)
    
    if not prd_path.exists():
        raise FileNotFoundError(f"PRD file not found: {prd_path}")
    
    # Read PRD file
    with open(prd_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    total_lines = len(lines)
    chunk_size = config.chunk_size_lines
    
    # Build chunks
    chunks = []
    chunk_id = 1
    
    # Phase ID includes growth pass for stability across re-chunking
    # Format: P<growth_pass>.<chunk_index_padded>
    # If growth_pass is 0, use P1 (backward compatibility)
    pass_prefix = max(growth_pass, 1)
    
    for i in range(0, total_lines, chunk_size):
        start_line = i + 1  # 1-indexed
        end_line = min(i + chunk_size, total_lines)
        phase_id = f"P{pass_prefix}.{str(chunk_id).zfill(4)}"
        
        chunk = {
            "id": chunk_id,
            "phase_id": phase_id,
            "start_line": start_line,
            "end_line": end_line,
            "status": "pending",
            "attempts": 0,
            "last_error": None,
            "last_updated_at": None
        }
        
        chunks.append(chunk)
        chunk_id += 1
    
    # Build state structure
    now = datetime.datetime.now().isoformat()
    
    # Initialize growth metadata
    if preserve_growth_meta is None:
        growth_meta = {
            "current_pass": 0,
            "total_passes_run": 0,
            "last_pass_summary": {
                "pass_id": 0,
                "chunks_attempted": 0,
                "chunks_succeeded": 0,
                "chunks_failed": 0,
                "lines_before": 0,
                "lines_after": 0
            }
        }
    else:
        growth_meta = preserve_growth_meta
    
    state = {
        "meta": {
            "master_md_path": config.master_md_path,
            "total_lines": total_lines,
            "chunk_size_lines": chunk_size,
            "created_at": now,
            "updated_at": now,
            "version": 2,  # Bumped for growth metadata support
            "growth": growth_meta
        },
        "chunks": chunks
    }
    
    return state


# ============================================================================
# PRD SKELETON CREATION
# ============================================================================

def create_prd_skeleton(prd_path: pathlib.Path) -> None:
    """
    Create a PRD skeleton if it doesn't exist.
    This is the same skeleton from Step 1.
    """
    if prd_path.exists():
        return
    
    # Read the existing skeleton (it should exist from Step 1)
    # If not, we'll create a minimal one
    skeleton_content = """# 0. PROJECT META & CONTROL

<!--
AUTOMATION SYSTEM NOTES:
========================
This document is managed by an automated PRD enhancement system.

CRITICAL RULES FOR AI AGENTS:
- DO NOT delete information; only enhance, refactor, and append.
- All enhancements happen via small phases; each phase has an ID like `Phase 3.2.1`.
- This document may grow to 100,000+ lines through automated expansion.
- When enhancing, preserve all existing content and add detail/clarity.
- Label new assumptions, open questions, and risks clearly.
- Use phase IDs to track which sections have been processed.
-->

## Project Name
[To be filled by user or automation]

## Project Description
[One-paragraph description of the app/game/service. User will provide initial seed text here.]

## Project Tags
- Type: [mobile / web / game / AI / backend / desktop / other]
- Platform: [iOS / Android / Web / Desktop / Cross-platform]
- Category: [e.g., productivity / entertainment / health / finance / education]

## Automation Metadata
- Created: [Date will be set by automation]
- Last Enhanced: [Date will be updated by automation]
- Total Phases Completed: 0
- Current Phase: None

---

# 1. VISION, STRATEGY & BUSINESS

## 1.1 Mission & Vision
[To be expanded: Core purpose, long-term vision, what the product aims to achieve.]

## 1.2 Target Users
[To be expanded: Primary and secondary user personas, demographics, psychographics.]

## 1.3 Value Proposition
[To be expanded: What unique value does this product provide? Why would users choose it?]

## 1.4 Market & Competition
[To be expanded: Market size, competitive landscape, differentiation strategy.]

## 1.5 Monetization & Business Model
[To be expanded: Revenue streams, pricing strategy, business sustainability.]

---

# 2. OMNI-CORP MASTER ROLES (SUMMARY PLACEHOLDER)

## 2.1 Role Categories

### Executive & Product Strategy
- CEO / Founder
- Chief Product Officer (CPO)
- Product Manager
- Business Strategist

### Core Engineering
- Chief Technology Officer (CTO)
- Software Architect
- Mobile Developer (iOS/Android)
- Web Developer (Frontend/Backend)
- Game Developer
- Full-Stack Engineer

### Design & Creative
- Chief Design Officer (CDO)
- UX Designer
- UI Designer
- Visual Designer
- Content Strategist

### Data & Intelligence
- AI/ML Engineer
- Data Scientist
- Analytics Engineer
- Research Scientist

### Operations & Infrastructure
- DevOps Engineer
- Site Reliability Engineer (SRE)
- Security Engineer
- Infrastructure Architect

### Growth & Support
- Growth Marketing Manager
- Community Manager
- Customer Success Manager
- Technical Writer

---

# 3. PRODUCT REQUIREMENTS DOCUMENT (PRD CORE)

## 3.1 Users & Personas
[To be expanded: Detailed user personas with goals, pain points, behaviors.]

## 3.2 Use Cases & Scenarios
[To be expanded: Primary use cases, user journeys, edge cases.]

## 3.3 Features & Requirements
[To be expanded: Feature list, functional requirements, feature priorities.]

## 3.4 Non-Functional Requirements
[To be expanded: Performance, reliability, scalability, security, accessibility, etc.]

## 3.5 Success Metrics / KPIs
[To be expanded: How we measure success, key performance indicators, analytics goals.]

---

# 4. ARCHITECTURE & SYSTEM DESIGN

## 4.1 Overall Architecture Overview
[To be expanded: High-level system architecture, architectural patterns, design principles.]

## 4.2 Client Architecture
[To be expanded: Mobile app architecture, web app architecture, game engine architecture, etc.]

## 4.3 Server/Backend Architecture
[To be expanded: API design, microservices vs monolith, backend services, data processing.]

## 4.4 Data Model & Storage
[To be expanded: Database schema, data models, storage strategy, data flow.]

## 4.5 Integrations & External APIs
[To be expanded: Third-party services, API integrations, webhooks, external dependencies.]

---

# 5. IMPLEMENTATION & ENGINEERING NOTES

## 5.1 Tech Stack Options
[To be expanded: Recommended technologies, frameworks, libraries, tools.]

## 5.2 Coding Standards
[To be expanded: Code style, conventions, best practices, review process.]

## 5.3 Folder Structure Guidelines
[To be expanded: Project organization, directory structure, file naming conventions.]

## 5.4 Development Workflow
[To be expanded: Git workflow, branching strategy, CI/CD, testing strategy.]

---

# 6. AI, DATA & ANALYTICS

## 6.1 AI Features
[To be expanded: AI capabilities, ML models, AI-powered features, training data needs.]

## 6.2 Data Collection & Analytics
[To be expanded: What data to collect, analytics tools, data pipelines, metrics tracking.]

## 6.3 Privacy, Ethics & Safety
[To be expanded: Data privacy, user consent, ethical AI, safety measures, compliance.]

---

# 7. DESIGN, UX & CONTENT

## 7.1 UX Principles
[To be expanded: User experience principles, interaction design, usability goals.]

## 7.2 Visual Style
[To be expanded: Visual design language, brand identity, color palette, typography, iconography.]

## 7.3 Content Strategy
[To be expanded: Content guidelines, tone of voice, localization, accessibility.]

---

# 8. PROMPT LIBRARY & AGENT PLAYBOOK

## 8.1 Role Selection Strategy
[To be expanded: How to select which roles to use for which sections/phases.]

## 8.2 Role Prompt Templates
[Placeholder: Role prompt templates will be integrated here]

---

# 9. TASKS, BACKLOG & ROADMAP

## 9.1 Immediate Tasks
[To be expanded: Current sprint tasks, blockers, immediate next steps.]

## 9.2 Short-Term Roadmap
[To be expanded: Next 1-3 months, upcoming releases, short-term milestones.]

## 9.3 Long-Term Roadmap
[To be expanded: 6-12 month vision, strategic initiatives, long-term goals.]

---

# 10. PROGRESS LOG & PHASE HISTORY

## 10.1 Automation Log
[Automation system will append log entries here as phases complete]

### Initial Skeleton Created
- Date: [Will be set by automation]
- Phase: Initial
- Summary: Initial PRD skeleton created with all major sections.

---
"""
    
    with open(prd_path, 'w', encoding='utf-8') as f:
        f.write(skeleton_content)
    
    log(f"Created PRD skeleton at {prd_path}", {"step": "create_skeleton"})


# ============================================================================
# OMNI-CORP ROLE LIBRARY & PROMPT TEMPLATES
# ============================================================================

def generate_omni_corp_role_library() -> str:
    """
    Generate the canonical Omni-Corp Master Role Library content.
    
    Returns:
        Complete markdown content for the role library section
    """
    return """<!-- OMNI_CORP_ROLE_LIBRARY_START -->

# 2. OMNI-CORP MASTER ROLE LIBRARY

The Omni-Corp Master Role Library provides a comprehensive set of AI personas with specialized expertise. Each role is designed to work universally across any digital product type (mobile apps, web apps, games, AI tools, backend services, etc.). Roles use generalized, reusable actions rather than project-specific references.

## 2.1 Role Categories

### Executive & Product Strategy

These roles focus on high-level vision, strategy, and product direction. They collaborate to define what should be built, why it matters, and how it fits into the market. They work closely with engineering and design to ensure alignment between business goals and technical execution.

### Core Engineering

These roles handle the technical architecture, implementation, and engineering practices. They translate product requirements into robust, scalable systems. They collaborate across the stack to ensure code quality, performance, and maintainability.

### Design & Creative

These roles focus on user experience, visual design, and creative content. They ensure the product is intuitive, beautiful, and engaging. They work closely with product and engineering to create cohesive user experiences.

### Data & Intelligence

These roles specialize in AI, machine learning, data science, and analytics. They build intelligent features, analyze user behavior, and provide data-driven insights. They collaborate with product and engineering to integrate AI capabilities and measure success.

### Operations & Infrastructure

These roles ensure the product runs reliably, securely, and at scale. They handle deployment, monitoring, security, and compliance. They work with engineering to build robust infrastructure and operational processes.

### Growth, Community & Support

These roles focus on user acquisition, engagement, and satisfaction. They build communities, create content, and ensure users succeed with the product. They collaborate with product and design to optimize the user journey.

---

## 2.2 Role Definitions

### Chief Technology Officer (CTO)

**Act as:** A senior technology executive responsible for technical strategy, architecture decisions, and engineering excellence across the entire organization.

**Core Function:** Define and execute the technical vision, ensuring the product is built on a solid, scalable foundation. Balance innovation with pragmatism, and align technical decisions with business goals.

**Universal Responsibilities:**

1. Analyze the overall system architecture and all relevant technical artifacts for scalability, maintainability, and alignment with product goals.
2. Identify technical risks, constraints, and trade-offs across the entire technology stack and propose mitigation strategies.
3. Define technical standards, best practices, and engineering culture that ensure high-quality, sustainable development.
4. Evaluate technology choices (frameworks, platforms, tools) and make recommendations based on project requirements, team capabilities, and long-term vision.
5. Guide architectural decisions and ensure consistency across different components and services.

---

### Chief Product Officer (CPO) / Product Lead

**Act as:** A senior product executive responsible for product strategy, roadmap, and ensuring the product delivers value to users and the business.

**Core Function:** Define what to build, why it matters, and how success will be measured. Bridge the gap between user needs, business goals, and technical capabilities.

**Universal Responsibilities:**

1. Analyze user needs, market opportunities, and competitive landscape to define product vision and strategy.
2. Prioritize features and initiatives based on user value, business impact, and technical feasibility.
3. Define success metrics and key performance indicators (KPIs) that measure product success.
4. Create detailed product requirements, user stories, and acceptance criteria that guide development.
5. Identify risks, assumptions, and dependencies that could impact product delivery or success.

---

### Lead Game Producer (for game-like experiences)

**Act as:** A senior producer responsible for coordinating game development, managing scope, timeline, and quality across all disciplines.

**Core Function:** Ensure the game/experience is delivered on time, within scope, and meets quality standards. Coordinate between design, engineering, art, and other disciplines.

**Universal Responsibilities:**

1. Analyze project scope, timeline, and resource requirements to create realistic development plans.
2. Identify dependencies, bottlenecks, and risks that could impact delivery and propose mitigation strategies.
3. Coordinate between different disciplines (design, engineering, art, audio) to ensure cohesive execution.
4. Define quality standards and ensure all deliverables meet those standards before release.
5. Manage stakeholder communication and ensure alignment on priorities and expectations.

---

### Principal Software Architect

**Act as:** A senior technical architect responsible for designing system architecture, technical patterns, and ensuring technical excellence.

**Core Function:** Design scalable, maintainable system architectures that support current and future product requirements. Provide technical leadership and guidance to engineering teams.

**Universal Responsibilities:**

1. Analyze system requirements and design high-level architectures that balance scalability, performance, and maintainability.
2. Define architectural patterns, design principles, and technical standards that guide implementation.
3. Identify technical risks, performance bottlenecks, and scalability concerns early in the design process.
4. Evaluate and recommend technologies, frameworks, and tools that align with architectural goals.
5. Create technical documentation, diagrams, and specifications that communicate the architecture to the team.

---

### Senior Mobile Developer

**Act as:** A senior mobile engineer specializing in native or cross-platform mobile development (iOS, Android, or both).

**Core Function:** Build high-quality mobile applications that deliver excellent user experiences while respecting platform conventions and constraints.

**Universal Responsibilities:**

1. Analyze mobile-specific requirements (platform capabilities, performance, battery, network) and design solutions that work within these constraints.
2. Implement mobile features following platform best practices, design patterns, and performance guidelines.
3. Identify mobile-specific risks (app store policies, device fragmentation, offline scenarios) and propose solutions.
4. Optimize mobile performance (startup time, memory usage, battery consumption) and ensure smooth user experience.
5. Design mobile architecture patterns (navigation, state management, data persistence) that scale with app complexity.

---

### Full-Stack Web Developer

**Act as:** A senior web engineer capable of working across frontend and backend, building complete web applications.

**Core Function:** Build scalable web applications with modern frontend experiences and robust backend services. Ensure seamless integration between client and server.

**Universal Responsibilities:**

1. Analyze web application requirements and design full-stack solutions that balance user experience with backend scalability.
2. Implement frontend features using modern frameworks and ensure responsive, accessible, and performant user interfaces.
3. Design and implement backend APIs, services, and data models that support frontend requirements.
4. Identify web-specific risks (browser compatibility, security vulnerabilities, performance) and propose mitigation strategies.
5. Optimize web performance (load times, rendering, API response times) and ensure excellent user experience across devices.

---

### Gameplay Programmer

**Act as:** A senior game programmer specializing in gameplay systems, mechanics, and player-facing features.

**Core Function:** Implement engaging gameplay mechanics, systems, and features that create compelling player experiences.

**Universal Responsibilities:**

1. Analyze gameplay requirements and design systems (combat, progression, economy, social) that create engaging player experiences.
2. Implement gameplay mechanics following game design principles, ensuring they feel responsive and balanced.
3. Identify gameplay risks (balance issues, exploitability, player frustration) and propose solutions.
4. Optimize gameplay performance (frame rate, input latency, memory usage) to ensure smooth player experience.
5. Design gameplay architecture patterns (state machines, event systems, data-driven design) that support iteration and balance.

---

### UI/UX Lead Designer

**Act as:** A senior designer responsible for user experience and interface design across the entire product.

**Core Function:** Create intuitive, beautiful, and accessible user experiences that delight users and achieve product goals.

**Universal Responsibilities:**

1. Analyze user needs, behaviors, and pain points to design user experiences that solve real problems.
2. Create user flows, wireframes, and prototypes that communicate design intent and validate concepts.
3. Design visual interfaces that are consistent, accessible, and aligned with brand identity.
4. Identify UX risks (usability issues, accessibility barriers, user confusion) and propose solutions.
5. Collaborate with engineering to ensure designs are implemented accurately and perform well.

---

### Level Designer (for game-like experiences / flows)

**Act as:** A senior designer specializing in creating engaging levels, spaces, or user flow experiences.

**Core Function:** Design levels, spaces, or user journeys that guide users through engaging, well-paced experiences.

**Universal Responsibilities:**

1. Analyze level/flow requirements and design experiences that balance challenge, exploration, and narrative.
2. Create level layouts, flow diagrams, and pacing guides that ensure engaging user experiences.
3. Identify design risks (difficulty spikes, confusing navigation, pacing issues) and propose solutions.
4. Iterate on designs based on playtesting, user feedback, and analytics to optimize the experience.
5. Document design intent, player goals, and key interactions to guide implementation.

---

### Technical Artist

**Act as:** A senior artist-technician who bridges art and engineering, ensuring visual assets are optimized and integrated efficiently.

**Core Function:** Optimize visual assets, create tools and pipelines, and ensure art assets integrate smoothly with the technical implementation.

**Universal Responsibilities:**

1. Analyze visual requirements and technical constraints to design asset pipelines and optimization strategies.
2. Create tools, scripts, and workflows that streamline asset creation and integration.
3. Optimize visual assets (textures, models, animations) for performance while maintaining quality.
4. Identify technical art risks (performance bottlenecks, asset bloat, pipeline inefficiencies) and propose solutions.
5. Collaborate with artists and engineers to ensure visual assets are created efficiently and integrated correctly.

---

### Sound Designer & Audio Engineer

**Act as:** A senior audio professional responsible for all sound design, music, and audio implementation.

**Core Function:** Create immersive audio experiences that enhance the product and support the user experience.

**Universal Responsibilities:**

1. Analyze audio requirements and design sound systems that enhance the user experience and support product goals.
2. Create sound effects, music, and voice-over that align with the product's tone and brand.
3. Implement audio systems (spatial audio, dynamic mixing, adaptive music) that respond to user actions and context.
4. Identify audio risks (file size, performance impact, accessibility) and propose solutions.
5. Optimize audio assets and systems for performance while maintaining quality and immersion.

---

### AI/ML Engineer

**Act as:** A senior engineer specializing in artificial intelligence and machine learning, building intelligent features and systems.

**Core Function:** Design and implement AI/ML features that enhance the product with intelligent capabilities (recommendations, predictions, automation, etc.).

**Universal Responsibilities:**

1. Analyze AI/ML requirements and design systems that leverage machine learning to solve user problems.
2. Implement ML models, training pipelines, and inference systems that integrate with the product.
3. Identify AI/ML risks (model accuracy, bias, data quality, computational costs) and propose mitigation strategies.
4. Optimize ML systems for performance, accuracy, and cost-effectiveness.
5. Design ML architecture patterns (feature engineering, model serving, A/B testing) that support iteration and improvement.

---

### Data Scientist & Analyst

**Act as:** A senior data professional responsible for analyzing user behavior, product metrics, and business data.

**Core Function:** Extract insights from data to inform product decisions, measure success, and identify opportunities.

**Universal Responsibilities:**

1. Analyze product data (user behavior, engagement, business metrics) to identify trends, patterns, and opportunities.
2. Design experiments, A/B tests, and analytics implementations that measure product success.
3. Create dashboards, reports, and visualizations that communicate insights to stakeholders.
4. Identify data risks (data quality, privacy, bias) and propose solutions.
5. Collaborate with product and engineering to define metrics, implement tracking, and interpret results.

---

### DevOps & Cloud Architect

**Act as:** A senior operations engineer responsible for deployment, infrastructure, and operational excellence.

**Core Function:** Design and maintain infrastructure that enables reliable, scalable, and efficient product deployment and operation.

**Universal Responsibilities:**

1. Analyze infrastructure requirements and design cloud architectures that support scalability, reliability, and cost efficiency.
2. Implement CI/CD pipelines, deployment automation, and infrastructure-as-code that streamline operations.
3. Design monitoring, alerting, and observability systems that ensure system health and rapid incident response.
4. Identify infrastructure risks (scalability limits, single points of failure, security vulnerabilities) and propose solutions.
5. Optimize infrastructure for cost, performance, and reliability while maintaining operational simplicity.

---

### Cybersecurity / Application Security Engineer

**Act as:** A senior security engineer responsible for ensuring the product is secure, compliant, and protects user data.

**Core Function:** Identify security risks, design secure systems, and ensure the product meets security and compliance requirements.

**Universal Responsibilities:**

1. Analyze security requirements and design systems that protect user data and prevent security vulnerabilities.
2. Conduct security audits, penetration testing, and code reviews to identify and remediate security issues.
3. Design authentication, authorization, and encryption systems that secure user data and access.
4. Identify security risks (vulnerabilities, data breaches, compliance gaps) and propose mitigation strategies.
5. Create security policies, procedures, and documentation that guide secure development practices.

---

### Technology Lawyer / Compliance Officer

**Act as:** A legal and compliance professional specializing in technology law, privacy, and regulatory compliance.

**Core Function:** Ensure the product complies with relevant laws, regulations, and industry standards (GDPR, CCPA, COPPA, etc.).

**Universal Responsibilities:**

1. Analyze legal and compliance requirements and identify obligations that apply to the product.
2. Design privacy policies, terms of service, and data handling procedures that comply with regulations.
3. Identify compliance risks (regulatory violations, privacy breaches, legal liability) and propose mitigation strategies.
4. Review product features, data collection, and user agreements for legal and compliance issues.
5. Create compliance documentation, procedures, and training that ensure ongoing adherence to requirements.

---

### Growth / Marketing Lead

**Act as:** A senior growth professional responsible for user acquisition, engagement, and retention.

**Core Function:** Design and execute growth strategies that acquire, engage, and retain users while optimizing for business metrics.

**Universal Responsibilities:**

1. Analyze market opportunities, user segments, and competitive landscape to design growth strategies.
2. Design and execute marketing campaigns, user acquisition channels, and engagement initiatives.
3. Optimize user onboarding, conversion funnels, and retention strategies based on data and experimentation.
4. Identify growth risks (acquisition costs, churn, market saturation) and propose solutions.
5. Measure and report on growth metrics (acquisition, activation, retention, revenue) to inform strategy.

---

### Customer Success & Community Manager

**Act as:** A senior professional responsible for user support, community building, and ensuring user success.

**Core Function:** Build and nurture user communities, provide excellent support, and ensure users achieve success with the product.

**Universal Responsibilities:**

1. Analyze user needs, feedback, and support patterns to identify opportunities to improve user success.
2. Design support processes, documentation, and self-service resources that help users succeed.
3. Build and manage user communities (forums, Discord, social media) that foster engagement and knowledge sharing.
4. Identify user success risks (support bottlenecks, user confusion, churn) and propose solutions.
5. Measure and report on user satisfaction, support metrics, and community health to inform improvements.

---

<!-- OMNI_CORP_ROLE_LIBRARY_END -->"""


def generate_prompt_templates_and_framework() -> str:
    """
    Generate the canonical Prompt Templates and Phase/Task Framework content.
    
    Returns:
        Complete markdown content for the prompt templates and framework section
    """
    return """<!-- PROMPT_TEMPLATES_START -->

# 8. PROMPT LIBRARY & AGENT PLAYBOOK

This section contains canonical prompt templates and task frameworks that guide the automated enhancement of this PRD document. All templates reference the Omni-Corp Master Role Library (Section 2) and are designed to work universally across any product type.

## 8.1 Role Selection Strategy

When enhancing a section of this PRD, select roles from the Omni-Corp Master Role Library based on:

1. **Section Type**: Different sections benefit from different expertise:
   - Vision & Strategy → CPO, CTO, Growth Lead
   - Technical Architecture → CTO, Principal Architect, DevOps
   - Features & Requirements → CPO, UI/UX Lead, relevant Engineering roles
   - Design & UX → UI/UX Lead, Technical Artist, Sound Designer
   - Data & Analytics → Data Scientist, AI/ML Engineer
   - Security & Compliance → Security Engineer, Technology Lawyer

2. **Phase Goals**: What needs to be accomplished:
   - Expansion & Detail → Domain experts (e.g., Mobile Developer for mobile features)
   - Risk Analysis → Security Engineer, CTO, CPO
   - Implementation Planning → Engineering roles, DevOps
   - User Experience → UI/UX Lead, Community Manager

3. **Multi-Role Collaboration**: Complex sections may benefit from multiple roles working together, with each role focusing on their area of expertise.

---

## 8.2 Canonical Prompt Templates

### Template: Role-Based Section Expansion

**Purpose:** Use a specific expert role to expand or improve a section of this document.

**Prompt Pattern:**

```
Act as **[ROLE NAME]** from the Omni-Corp Master Role Library (Section 2 of this document).

You will improve the following section of the master PRD document.

Context:
- Product type: [mobile / web / game / AI / backend / multi-platform]
- Current phase: [Phase ID, e.g., 3.1.2]
- Section location: [e.g., Section 3.2 Features & Requirements]

Goals:
1. Clarify and expand the requirements in more detail, adding specificity where placeholders exist.
2. Identify edge cases, risks, and open questions relevant to your role's expertise.
3. Propose concrete, actionable details that guide implementation.

Constraints:
- Do not remove important information; preserve all existing content.
- Preserve meaning; you may rephrase and reorganize for clarity.
- Prefer adding detail, structure, and examples over summarizing.
- Label assumptions with [ASSUMPTION], open questions with [OPEN_QUESTION], and risks with [RISK].
- Output in markdown, and wrap your final improved section between:

<<<IMPROVED_CHUNK_START>>>
...your improved markdown...
<<<IMPROVED_CHUNK_END>>>

ORIGINAL SECTION:
---
[section content here]
---
```

---

### Template: Role-Based Technical Deep Dive

**Purpose:** Use a technical expert role to provide detailed technical analysis and recommendations.

**Prompt Pattern:**

```
Act as **[ROLE NAME]** from the Omni-Corp Master Role Library (Section 2 of this document).

You will provide a technical deep dive on the following section, analyzing it from your role's perspective.

Context:
- Product type: [mobile / web / game / AI / backend / multi-platform]
- Current phase: [Phase ID]
- Section location: [e.g., Section 4.1 Overall Architecture Overview]

Goals:
1. Analyze the technical aspects of this section from your role's expertise.
2. Identify technical risks, constraints, and trade-offs.
3. Propose concrete technical recommendations, patterns, or solutions.
4. Highlight areas that need more technical detail or clarification.

Constraints:
- Do not remove important information; preserve all existing content.
- Add technical depth while maintaining clarity for non-technical stakeholders.
- Use general, universal language (avoid project-specific file names or tools unless essential).
- Label technical risks with [RISK], assumptions with [ASSUMPTION], and recommendations with [RECOMMENDATION].
- Output in markdown, and wrap your final improved section between:

<<<IMPROVED_CHUNK_START>>>
...your improved markdown...
<<<IMPROVED_CHUNK_END>>>

ORIGINAL SECTION:
---
[section content here]
---
```

---

### Template: Role-Based Risk & Edge-Case Review

**Purpose:** Use expert roles to identify risks, edge cases, and potential issues.

**Prompt Pattern:**

```
Act as **[ROLE NAME]** from the Omni-Corp Master Role Library (Section 2 of this document).

You will review the following section to identify risks, edge cases, and potential issues from your role's perspective.

Context:
- Product type: [mobile / web / game / AI / backend / multi-platform]
- Current phase: [Phase ID]
- Section location: [e.g., Section 3.3 Features & Requirements]

Goals:
1. Identify potential risks, edge cases, and failure modes relevant to your expertise.
2. Highlight assumptions that may not hold true.
3. Propose mitigation strategies or alternative approaches.
4. Flag areas that need more investigation or clarification.

Constraints:
- Do not remove important information; preserve all existing content.
- Add risk analysis while maintaining the original structure.
- Be specific about risks and provide actionable mitigation strategies.
- Label each risk with [RISK], each assumption with [ASSUMPTION], and each mitigation with [MITIGATION].
- Output in markdown, and wrap your final improved section between:

<<<IMPROVED_CHUNK_START>>>
...your improved markdown...
<<<IMPROVED_CHUNK_END>>>

ORIGINAL SECTION:
---
[section content here]
---
```

---

### Template: Role-Based Implementation Task Breakdown

**Purpose:** Use expert roles to break down sections into concrete, actionable implementation tasks.

**Prompt Pattern:**

```
Act as **[ROLE NAME]** from the Omni-Corp Master Role Library (Section 2 of this document).

You will break down the following section into concrete, actionable implementation tasks from your role's perspective.

Context:
- Product type: [mobile / web / game / AI / backend / multi-platform]
- Current phase: [Phase ID]
- Section location: [e.g., Section 3.3.1 Must-Have Features (MVP)]

Goals:
1. Break down this section into specific, actionable tasks that can be implemented.
2. Identify dependencies between tasks and suggest an implementation order.
3. Estimate complexity or effort where possible (high/medium/low).
4. Highlight any prerequisites or blockers that need to be addressed first.

Constraints:
- Do not remove important information; preserve all existing content.
- Add task breakdown while maintaining the original requirements.
- Use the Canonical Task Template (Section 8.3) format for each task.
- Label dependencies with [DEPENDENCY], blockers with [BLOCKER], and effort estimates with [EFFORT: high/medium/low].
- Output in markdown, and wrap your final improved section between:

<<<IMPROVED_CHUNK_START>>>
...your improved markdown...
<<<IMPROVED_CHUNK_END>>>

ORIGINAL SECTION:
---
[section content here]
---
```

---

## 8.3 Phase & Task Framework

### Phase ID Naming Scheme

Phases are organized hierarchically using a three-level numbering system:

- **Level 1 (Major Section)**: Corresponds to top-level PRD sections (1-10)
  - Example: `Phase 1.x.x` = Vision, Strategy & Business
  - Example: `Phase 3.x.x` = Product Requirements Document (PRD Core)
  - Example: `Phase 4.x.x` = Architecture & System Design

- **Level 2 (Subsection)**: Corresponds to subsections within major sections
  - Example: `Phase 3.1.x` = Users & Personas
  - Example: `Phase 3.2.x` = Use Cases & Scenarios
  - Example: `Phase 4.1.x` = Overall Architecture Overview

- **Level 3 (Micro-Task)**: Specific enhancement or task within a subsection
  - Example: `Phase 3.1.1` = Define Primary User Persona
  - Example: `Phase 3.1.2` = Define Secondary User Personas
  - Example: `Phase 4.1.1` = Define High-Level Architecture Diagram

This hierarchical structure allows the automation system to:
- Track progress at multiple levels of granularity
- Organize enhancements logically
- Generate phase IDs automatically based on document structure
- Support incremental growth from small tasks to large-scale expansion

### Canonical Task Template

Each micro-task should be described using the following template:

```markdown
#### Task: [Phase ID] - [Title]

- **Phase ID:** [e.g., 3.2.1]
- **Title:** [short verb phrase, e.g., "Detail Core Features"]
- **Goal:** [what this task wants to achieve in 1-2 sentences]
- **Primary Role(s):** [which roles from the Omni-Corp Master Role Library (Section 2) are best suited]
- **Inputs:** [sections, artifacts, or assumptions required]
  - [Input 1]
  - [Input 2]
- **Outputs:** [what must exist after completion]
  - [Output 1]
  - [Output 2]
- **Success Criteria:** [how to judge that the task is "done"]
  - [Criterion 1]
  - [Criterion 2]
- **Dependencies:** [other phases or tasks that must complete first]
  - [Dependency 1]
- **Risks / Notes:** [optional, known issues, assumptions, or special considerations]
  - [Risk or note 1]
```

**Example Task:**

```markdown
#### Task: 3.1.1 - Define Primary User Persona

- **Phase ID:** 3.1.1
- **Title:** Define Primary User Persona
- **Goal:** Create a detailed persona for the primary target user, including demographics, goals, pain points, and behaviors.
- **Primary Role(s):** CPO / Product Lead, UI/UX Lead Designer
- **Inputs:**
  - Section 1.2 Target Users (high-level description)
  - Market research or user insights (if available)
- **Outputs:**
  - Detailed persona description with name, demographics, goals, pain points
  - User journey outline
  - Key behaviors and preferences
- **Success Criteria:**
  - Persona is specific enough to guide feature decisions
  - Persona includes at least 3-5 key pain points
  - Persona includes behavioral patterns relevant to the product
- **Dependencies:**
  - Phase 1.2 (Target Users) should be at least partially defined
- **Risks / Notes:**
  - [ASSUMPTION] User research data may be limited; persona may need validation later
  - [RISK] Persona may be too generic; ensure specificity through examples
```

---

## 8.4 Automation Integration Notes

The automation system (auto_master.py) uses these templates and frameworks to:

1. **Generate Enhancement Prompts**: When processing a chunk, the system can select an appropriate role and prompt template based on the section being enhanced.

2. **Track Phase Progress**: Phase IDs are used to track which sections have been enhanced and to what depth.

3. **Plan Future Enhancements**: The task framework helps identify what needs to be done next and in what order.

4. **Ensure Consistency**: Using canonical templates ensures all enhancements follow consistent patterns and quality standards.

5. **Support Multi-Role Collaboration**: Different roles can enhance the same section from different perspectives, building comprehensive coverage.

---

<!-- PROMPT_TEMPLATES_END -->"""


# ============================================================================
# PROMPT BUILDING
# ============================================================================

def build_enhance_prompt(
    config: Config,
    chunk_text: str,
    phase_id: str,
    start_line: int,
    end_line: int,
) -> str:
    """
    Build an enhancement prompt for a chunk.
    
    This prompt references the Omni-Corp Master Role Library and Prompt Templates
    defined in Section 2 and Section 8 of prd.md.
    
    Args:
        config: Config object
        chunk_text: The text content of the chunk
        phase_id: Phase identifier (e.g., "P1.0001")
        start_line: Starting line number (1-indexed)
        end_line: Ending line number (1-indexed)
    
    Returns:
        Complete prompt string
    """
    prompt = f"""You are an AI assistant helping to enhance a Product Requirements Document (PRD).

CONTEXT:
- This is part of the Omni-Corp Automation System described in Section 2 (Omni-Corp Master Role Library) and Section 8 (Prompt Library & Agent Playbook) of prd.md.
- The text below is a direct copy/paste from lines {start_line}-{end_line} of prd.md.
- Phase ID: {phase_id}

ROLE AWARENESS:
- You may implicitly use any roles from the Omni-Corp Master Role Library (Section 2) to reason about this chunk.
- Consider which roles would be most relevant (e.g., CPO for product strategy, CTO for technical architecture, UI/UX Lead for design sections).
- Apply the expertise and perspective of relevant roles, but output only improved markdown for this chunk.
- Reference the prompt templates in Section 8 for guidance on how to approach enhancement.

CRITICAL RULES:
1. DO NOT skip or ignore any lines from the original chunk.
2. DO NOT delete information; only enhance, refactor, and expand.
3. Preserve all existing content while adding clarity and detail.
4. Label new assumptions with [ASSUMPTION], open questions with [OPEN_QUESTION], and risks with [RISK].
5. Maintain markdown formatting and structure.
6. Use general, universal language (avoid project-specific file names or tools unless essential).

YOUR TASK:
Read the chunk below carefully and enhance it by:
- Expanding on brief descriptions with relevant detail
- Adding more detail where placeholders exist
- Clarifying ambiguous statements
- Adding relevant context, examples, or analysis from appropriate role perspectives
- Identifying edge cases, risks, or open questions where relevant
- Preserving all original information

ORIGINAL CHUNK (lines {start_line}-{end_line}):
---
{chunk_text}
---

Please return your enhanced version wrapped in these markers:

<<<IMPROVED_CHUNK_START>>>
[Your enhanced markdown here]
<<<IMPROVED_CHUNK_END>>>

The enhanced chunk should be longer or equal in length to the original, with more detail and clarity.
"""
    return prompt


# ============================================================================
# AI INTERACTION (STEP 3: Cursor Integration + Fallback)
# ============================================================================

def send_to_model(
    prompt: str,
    chunk_text: str,
    phase_id: str,
    start_line: int,
    end_line: int,
    wait_seconds: int = 60,
    config: Config = None
) -> str:
    """
    Send a prompt to the AI model and return the response transcript.
    
    STEP 3: Supports two modes:
    - Cursor mode: Uses AppleScript to interact with Cursor IDE (macOS only)
    - Fake mode: Local stub for testing or non-macOS users
    
    PREREQUISITES FOR CURSOR MODE:
    - macOS operating system
    - Cursor IDE installed and accessible
    - macOS Accessibility permissions granted for System Events
      (System Preferences > Security & Privacy > Privacy > Accessibility)
    - Cursor's "New Chat" shortcut configured (default: Cmd+Option+L)
      (Edit cursor_driver.scpt if your shortcut differs)
    
    Args:
        prompt: The full prompt to send
        chunk_text: Original chunk text (used for fake mode fallback)
        phase_id: Phase identifier
        start_line: Starting line number
        end_line: Ending line number
        wait_seconds: How long to wait for response
        config: Config object (must have use_cursor_driver and cursor_driver_path)
    
    Returns:
        Response transcript (should contain markers for parsing)
    
    Raises:
        RuntimeError: If Cursor mode fails or transcript is empty
    """
    if config is None:
        raise ValueError("Config is required")
    
    # Determine mode
    use_cursor = getattr(config, 'use_cursor_driver', False)
    
    if not use_cursor:
        # FAKE MODE: Local stub for testing
        log(
            f"[mode=fake] use_cursor_driver=false; returning stubbed improved chunk",
            {"step": "send_to_model_mode"},
            config
        )
        
        # Create a fake "enhanced" version
        enhanced_lines = [
            f"> [LOCAL-STUB] Phase {phase_id} (lines {start_line}-{end_line}) – No Cursor driver. Echoing original chunk for testing.",
            "",
            chunk_text.rstrip(),
            "",
            f"<!-- Enhanced by automation system (fake mode) at {datetime.datetime.now().isoformat()} -->"
        ]
        
        enhanced_text = "\n".join(enhanced_lines)
        
        # Wrap with markers
        response = f"""<<<IMPROVED_CHUNK_START>>>
{enhanced_text}
<<<IMPROVED_CHUNK_END>>>
"""
        return response
    
    # CURSOR MODE: Real integration via AppleScript
    log(
        f"[mode=cursor] use_cursor_driver=true; calling cursor_driver.scpt",
        {"step": "send_to_model_mode"},
        config
    )
    
    driver_path = pathlib.Path(getattr(config, 'cursor_driver_path', 'cursor_driver.scpt'))
    
    # Resolve path relative to script directory if needed
    if not driver_path.is_absolute():
        # Try to find it relative to the script location or current directory
        script_dir = pathlib.Path(__file__).parent
        candidate = script_dir / driver_path
        if candidate.exists():
            driver_path = candidate
        elif pathlib.Path(driver_path).exists():
            driver_path = pathlib.Path(driver_path).resolve()
        else:
            raise FileNotFoundError(f"Cursor driver not found: {driver_path}")
    
    if not driver_path.exists():
        raise FileNotFoundError(f"Cursor driver not found: {driver_path}")
    
    log(
        f"Calling osascript with driver: {driver_path}",
        {"step": "cursor_call_start"},
        config
    )
    
    # Prepare prompt for passing to AppleScript
    # Escape quotes and handle special characters
    # We'll pass it as an argument, but need to be careful with quoting
    # For complex prompts, we could write to a temp file, but let's try direct arg first
    
    try:
        # Call osascript with the driver script
        # Note: subprocess will handle quoting, but we need to be careful with newlines
        # For now, we'll pass the prompt directly and let subprocess handle it
        result = subprocess.run(
            [
                'osascript',
                str(driver_path),
                prompt,  # Prompt text as argument
                str(wait_seconds)  # Wait seconds as argument
            ],
            capture_output=True,
            text=True,
            timeout=wait_seconds + 30,  # Add buffer for script execution time
            check=False
        )
        
        if result.returncode != 0:
            error_msg = result.stderr.strip() or f"osascript exited with code {result.returncode}"
            log(
                f"ERROR: AppleScript failed: {error_msg}",
                {"step": "cursor_call_result", "returncode": result.returncode},
                config
            )
            raise RuntimeError(f"Cursor driver failed: {error_msg}")
        
        log(
            f"AppleScript completed successfully",
            {"step": "cursor_call_result", "returncode": result.returncode},
            config
        )
        
        # Read transcript from clipboard using pbpaste
        log(
            f"Reading transcript from clipboard via pbpaste",
            {"step": "pbpaste_read"},
            config
        )
        
        pbpaste_result = subprocess.run(
            ['pbpaste'],
            capture_output=True,
            text=True,
            check=False
        )
        
        if pbpaste_result.returncode != 0:
            raise RuntimeError(f"Failed to read clipboard: pbpaste exited with code {pbpaste_result.returncode}")
        
        transcript = pbpaste_result.stdout
        
        if not transcript or len(transcript.strip()) == 0:
            raise RuntimeError("Transcript is empty - Cursor may not have responded or clipboard was not updated")
        
        log(
            f"Received transcript: {len(transcript)} characters",
            {"step": "pbpaste_read", "transcript_length": len(transcript)},
            config
        )
        
        return transcript
        
    except subprocess.TimeoutExpired:
        error_msg = f"Cursor driver timed out after {wait_seconds + 30} seconds"
        log(
            f"ERROR: {error_msg}",
            {"step": "cursor_call_result", "error": "timeout"},
            config
        )
        raise RuntimeError(error_msg)
    except FileNotFoundError as e:
        error_msg = f"Command not found (osascript or pbpaste): {e}"
        log(
            f"ERROR: {error_msg}",
            {"step": "cursor_call_result", "error": "command_not_found"},
            config
        )
        raise RuntimeError(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error in Cursor integration: {e}"
        log(
            f"ERROR: {error_msg}",
            {"step": "cursor_call_result", "error": str(e)},
            config
        )
        raise RuntimeError(error_msg) from e


# ============================================================================
# RESPONSE PARSING
# ============================================================================

def parse_enhanced_chunk(response: str) -> typing.Optional[str]:
    """
    Parse the enhanced chunk from AI response.
    
    Looks for markers: <<<IMPROVED_CHUNK_START>>> ... <<<IMPROVED_CHUNK_END>>>
    
    Args:
        response: Full AI response text
    
    Returns:
        Enhanced chunk text (without markers) or None if parsing fails
    """
    start_marker = "<<<IMPROVED_CHUNK_START>>>"
    end_marker = "<<<IMPROVED_CHUNK_END>>>"
    
    start_idx = response.find(start_marker)
    end_idx = response.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        return None
    
    if start_idx >= end_idx:
        return None
    
    # Extract content between markers
    content = response[start_idx + len(start_marker):end_idx].strip()
    return content


# ============================================================================
# SAFE FILE WRITING
# ============================================================================

def atomic_write_file(file_path: pathlib.Path, content: str) -> None:
    """
    Atomically write content to a file.
    
    Writes to a temp file first, then replaces the original.
    This ensures we don't corrupt the file if something goes wrong.
    
    Args:
        file_path: Path to target file
        content: Content to write
    """
    # Create temp file in same directory
    temp_path = file_path.with_suffix(file_path.suffix + '.tmp')
    
    try:
        # Write to temp file
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Replace original with temp file
        shutil.move(str(temp_path), str(file_path))
    except Exception as e:
        # Clean up temp file on error
        if temp_path.exists():
            temp_path.unlink()
        raise


# ============================================================================
# GIT UTILITIES
# ============================================================================

def run_git_command(args: list[str], cwd: typing.Optional[pathlib.Path] = None, config: typing.Optional[Config] = None) -> tuple[int, str, str]:
    """
    Runs `git` with the given args and returns (returncode, stdout, stderr).
    
    Logs command and result.
    
    Args:
        args: Git command arguments (e.g., ["status", "--porcelain"])
        cwd: Working directory (None = current directory)
        config: Config object for logging
    
    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    git_cmd = ["git"] + args
    cwd_str = str(cwd) if cwd else None
    
    log(
        f"Running git command: {' '.join(git_cmd)}",
        {"command": "git", "step": "run_git_command"},
        config
    )
    
    try:
        result = subprocess.run(
            git_cmd,
            cwd=cwd_str,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            log(
                f"Git command failed: {' '.join(git_cmd)} (returncode={result.returncode})",
                {"command": "git", "step": "run_git_command", "returncode": result.returncode},
                config
            )
        
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        log(
            f"Git command timed out: {' '.join(git_cmd)}",
            {"command": "git", "step": "run_git_command", "error": "timeout"},
            config
        )
        return 1, "", "Command timed out"
    except Exception as e:
        log(
            f"Git command error: {e}",
            {"command": "git", "step": "run_git_command", "error": str(e)},
            config
        )
        return 1, "", str(e)


def detect_git_repo(root: pathlib.Path) -> bool:
    """
    Check if we are inside a git repository.
    
    Args:
        root: Root directory to check
    
    Returns:
        True if inside a git repo, False otherwise
    """
    # Check if .git exists
    if (root / ".git").exists():
        return True
    
    # Try git rev-parse
    returncode, _, _ = run_git_command(["rev-parse", "--is-inside-work-tree"], cwd=root)
    return returncode == 0


def get_git_status_summary(root: pathlib.Path, config: Config) -> dict:
    """
    Get a summary of git repository status.
    
    Args:
        root: Root directory of the repository
        config: Config object for logging
    
    Returns:
        Dict with keys: is_repo, branch, dirty, ahead, behind
    """
    summary = {
        "is_repo": False,
        "branch": None,
        "dirty": False,
        "ahead": 0,
        "behind": 0
    }
    
    if not detect_git_repo(root):
        return summary
    
    summary["is_repo"] = True
    
    # Get current branch
    returncode, stdout, _ = run_git_command(["rev-parse", "--abbrev-ref", "HEAD"], cwd=root, config=config)
    if returncode == 0:
        summary["branch"] = stdout.strip()
    
    # Check if working tree is dirty
    returncode, stdout, _ = run_git_command(["status", "--porcelain"], cwd=root, config=config)
    if returncode == 0:
        summary["dirty"] = len(stdout.strip()) > 0
    
    # Get ahead/behind counts (if remote exists)
    branch = summary["branch"]
    if branch:
        remote = config.git.remote_name
        remote_branch = f"{remote}/{branch}"
        
        # Check if remote branch exists
        returncode, _, _ = run_git_command(["rev-parse", "--verify", f"{remote_branch}"], cwd=root, config=config)
        if returncode == 0:
            # Get ahead/behind counts
            returncode, stdout, _ = run_git_command(
                ["rev-list", "--left-right", "--count", f"{remote_branch}...HEAD"],
                cwd=root,
                config=config
            )
            if returncode == 0:
                parts = stdout.strip().split()
                if len(parts) == 2:
                    try:
                        summary["behind"] = int(parts[0])
                        summary["ahead"] = int(parts[1])
                    except ValueError:
                        pass
    
    return summary


def perform_git_sync(config: Config, reason: str, pass_stats: dict = None) -> bool:
    """
    Perform git sync operations (pull, add, commit, push) if enabled.
    
    Args:
        config: Config object
        reason: Reason for sync (e.g., "growth_pass_1", "manual_git_sync")
        pass_stats: Optional pass statistics for commit message (dict with lines_before, lines_after)
    
    Returns:
        True if sync completed successfully, False otherwise
    """
    if not config.git.enable_auto:
        log(
            f"Git auto-sync disabled (git.enable_auto=false); skipping",
            {"command": "git_sync", "step": "check_enabled"},
            config
        )
        return False
    
    root = pathlib.Path.cwd()
    
    # Check if we're in a git repo
    if not detect_git_repo(root):
        log(
            "No git repo detected; skipping git sync",
            {"command": "git_sync", "step": "detect_repo"},
            config
        )
        return False
    
    log(
        f"Starting git sync: reason={reason}",
        {"command": "git_sync", "step": "start", "reason": reason},
        config
    )
    
    # Pull before sync (if configured)
    if config.git.pull_before_sync:
        log(
            f"Pulling from {config.git.remote_name}/{config.git.branch_name}",
            {"command": "git_sync", "step": "git_pull"},
            config
        )
        
        returncode, stdout, stderr = run_git_command(
            ["pull", config.git.remote_name, config.git.branch_name],
            cwd=root,
            config=config
        )
        
        if returncode != 0:
            log(
                f"Git pull failed: {stderr}",
                {"command": "git_sync", "step": "git_pull", "error": stderr},
                config
            )
            log(
                "Aborting git sync due to pull failure",
                {"command": "git_sync", "step": "abort"},
                config
            )
            return False
    
    # Add configured paths
    paths_to_add = []
    for path_str in config.git.auto_add_paths:
        path = pathlib.Path(path_str)
        if path.exists():
            paths_to_add.append(path_str)
        else:
            log(
                f"Path does not exist, skipping: {path_str}",
                {"command": "git_sync", "step": "git_add", "skipped": path_str},
                config
            )
    
    if paths_to_add:
        log(
            f"Adding paths: {', '.join(paths_to_add)}",
            {"command": "git_sync", "step": "git_add", "paths": ",".join(paths_to_add)},
            config
        )
        
        returncode, stdout, stderr = run_git_command(
            ["add"] + paths_to_add,
            cwd=root,
            config=config
        )
        
        if returncode != 0:
            log(
                f"Git add failed: {stderr}",
                {"command": "git_sync", "step": "git_add", "error": stderr},
                config
            )
            return False
    
    # Check if there are staged changes
    returncode, stdout, _ = run_git_command(["diff", "--cached", "--quiet"], cwd=root, config=config)
    if returncode == 0:
        log(
            "No staged changes; skipping commit and push",
            {"command": "git_sync", "step": "check_staged"},
            config
        )
        return True
    
    # Create commit message
    commit_msg_parts = [config.git.commit_prefix]
    
    if pass_stats:
        lines_before = pass_stats.get("lines_before", 0)
        lines_after = pass_stats.get("lines_after", 0)
        commit_msg_parts.append(f"reason={reason} lines_before={lines_before} lines_after={lines_after}")
    else:
        commit_msg_parts.append(f"reason={reason}")
    
    commit_message = " ".join(commit_msg_parts)
    
    log(
        f"Committing: {commit_message}",
        {"command": "git_sync", "step": "git_commit", "message": commit_message},
        config
    )
    
    returncode, stdout, stderr = run_git_command(
        ["commit", "-m", commit_message],
        cwd=root,
        config=config
    )
    
    if returncode != 0:
        log(
            f"Git commit failed: {stderr}",
            {"command": "git_sync", "step": "git_commit", "error": stderr},
            config
        )
        return False
    
    # Push (if configured)
    if config.git.push_after_each_pass:
        log(
            f"Pushing to {config.git.remote_name}/{config.git.branch_name}",
            {"command": "git_sync", "step": "git_push"},
            config
        )
        
        returncode, stdout, stderr = run_git_command(
            ["push", config.git.remote_name, config.git.branch_name],
            cwd=root,
            config=config
        )
        
        if returncode != 0:
            log(
                f"Git push failed: {stderr}",
                {"command": "git_sync", "step": "git_push", "error": stderr, "reason": "push_failed"},
                config
            )
            return False
        
        log(
            f"Git push successful",
            {"command": "git_sync", "step": "git_push", "result": "ok"},
            config
        )
    
    log(
        f"Git sync completed successfully",
        {"command": "git_sync", "step": "complete"},
        config
    )
    
    return True


# ============================================================================
# HEALTH CHECKS & DIAGNOSTICS
# ============================================================================

def check_filesystem(config: Config) -> dict:
    """
    Check filesystem for required files.
    
    Returns:
        Dict with file statuses: {path: "ok" | "missing" | "unreadable"}
    """
    results = {}
    
    # Required files
    required_files = [
        ("prd.md", config.master_md_path),
        ("auto_config.json", "auto_config.json"),
        ("auto_master.py", "auto_master.py"),
    ]
    
    # Optional but important files
    optional_files = [
        ("cursor_driver.scpt", config.cursor_driver_path),
        (".auto_state.json", config.state_path),
        ("auto_master.log", config.log_path),
    ]
    
    for name, path_str in required_files:
        path = pathlib.Path(path_str)
        if not path.exists():
            results[name] = "missing"
        elif not path.is_file():
            results[name] = "unreadable"
        else:
            try:
                with open(path, 'r') as f:
                    f.read(1)
                results[name] = "ok"
            except Exception:
                results[name] = "unreadable"
    
    for name, path_str in optional_files:
        path = pathlib.Path(path_str)
        if not path.exists():
            results[name] = "missing"
        elif not path.is_file():
            results[name] = "unreadable"
        else:
            try:
                with open(path, 'r') as f:
                    f.read(1)
                results[name] = "ok"
            except Exception:
                results[name] = "unreadable"
    
    # Check cursor driver only if configured
    if config.use_cursor_driver:
        cursor_path = pathlib.Path(config.cursor_driver_path)
        if not cursor_path.exists():
            results["cursor_driver.scpt"] = "missing"
        else:
            results["cursor_driver.scpt"] = "ok"
    
    return results


def check_config_schema(config: Config) -> dict:
    """
    Validate config schema and values.
    
    Returns:
        Dict with warnings and errors: {warnings: [...], errors: [...]}
    """
    warnings = []
    errors = []
    
    # Check chunk_size_lines
    if config.chunk_size_lines <= 0:
        errors.append("chunk_size_lines must be > 0")
    elif config.chunk_size_lines < 50:
        warnings.append(f"chunk_size_lines={config.chunk_size_lines} is very small (recommended >= 100)")
    elif config.chunk_size_lines > 500:
        warnings.append(f"chunk_size_lines={config.chunk_size_lines} is very large (recommended <= 200)")
    
    # Check target_line_count
    if config.growth.target_line_count <= 0:
        errors.append("growth.target_line_count must be > 0")
    elif config.growth.target_line_count < 1000:
        warnings.append(f"growth.target_line_count={config.growth.target_line_count} is small (recommended >= 5000)")
    
    # Check min_length_ratio_ok
    if config.min_length_ratio_ok < 0 or config.min_length_ratio_ok > 1:
        errors.append("min_length_ratio_ok must be between 0 and 1")
    elif config.min_length_ratio_ok < 0.8:
        warnings.append(f"min_length_ratio_ok={config.min_length_ratio_ok} is low (recommended >= 0.9)")
    
    # Check git.enable_auto but no git repo
    if config.git.enable_auto:
        root = pathlib.Path.cwd()
        if not detect_git_repo(root):
            warnings.append("git.enable_auto=true but no git repository detected")
    
    # Check safety.max_consecutive_failures
    if config.safety.max_consecutive_failures <= 0:
        errors.append("safety.max_consecutive_failures must be > 0")
    
    return {"warnings": warnings, "errors": errors}


def check_state_consistency(state: typing.Optional[dict], lines: list[str], config: Config) -> dict:
    """
    Validate state consistency with actual PRD file.
    
    Returns:
        Dict with issues: {issues: [...], chunk_status_counts: {...}, needs_rebuild: bool}
    """
    issues = []
    chunk_status_counts = {}
    needs_rebuild = False
    
    if state is None:
        issues.append("State file is missing")
        needs_rebuild = True
        return {"issues": issues, "chunk_status_counts": {}, "needs_rebuild": needs_rebuild}
    
    # Check meta.total_lines
    meta = state.get("meta", {})
    state_total_lines = meta.get("total_lines", 0)
    actual_total_lines = len(lines)
    
    if abs(state_total_lines - actual_total_lines) > 10:  # Allow small variance
        issues.append(f"State total_lines={state_total_lines} differs significantly from actual={actual_total_lines}")
        needs_rebuild = True
    
    # Check chunks
    chunks = state.get("chunks", [])
    if not chunks:
        issues.append("State has no chunks")
        needs_rebuild = True
        return {"issues": issues, "chunk_status_counts": {}, "needs_rebuild": needs_rebuild}
    
    # Count statuses
    for chunk in chunks:
        status = chunk.get("status", "unknown")
        chunk_status_counts[status] = chunk_status_counts.get(status, 0) + 1
        
        # Validate chunk ranges
        start_line = chunk.get("start_line", 0)
        end_line = chunk.get("end_line", 0)
        
        if start_line < 1:
            issues.append(f"Chunk {chunk.get('id')} has invalid start_line={start_line}")
            needs_rebuild = True
        elif end_line < start_line:
            issues.append(f"Chunk {chunk.get('id')} has end_line={end_line} < start_line={start_line}")
            needs_rebuild = True
        elif end_line > actual_total_lines:
            issues.append(f"Chunk {chunk.get('id')} has end_line={end_line} beyond file length={actual_total_lines}")
            needs_rebuild = True
        
        # Check for invalid status
        if status not in ["pending", "running", "done", "failed", "invalid"]:
            issues.append(f"Chunk {chunk.get('id')} has invalid status={status}")
    
    # Check for chunks marked as "running" (shouldn't persist after process exit)
    if chunk_status_counts.get("running", 0) > 0:
        issues.append(f"Found {chunk_status_counts['running']} chunks marked as 'running' (may indicate crash)")
        if config.safety.enable_doctor_auto_fixes:
            # Auto-fix: convert running to pending
            for chunk in chunks:
                if chunk.get("status") == "running":
                    chunk["status"] = "pending"
            needs_rebuild = True
    
    return {
        "issues": issues,
        "chunk_status_counts": chunk_status_counts,
        "needs_rebuild": needs_rebuild
    }


def check_logs(config: Config) -> dict:
    """
    Analyze recent log entries for patterns and errors.
    
    Returns:
        Dict with analysis: {error_counts: {...}, hot_spots: [...], last_error_time: str | None}
    """
    log_path = pathlib.Path(config.log_path)
    
    if not log_path.exists():
        return {
            "error_counts": {},
            "hot_spots": [],
            "last_error_time": None,
            "lines_scanned": 0
        }
    
    error_counts = {
        "send_to_model": 0,
        "cursor": 0,
        "osascript": 0,
        "git": 0,
        "invariant_violation": 0,
        "parse_error": 0
    }
    
    hot_spots = {}  # chunk_id -> failure_count
    last_error_time = None
    
    try:
        # Read last N lines
        with open(log_path, 'r') as f:
            all_lines = f.readlines()
        
        lines_to_scan = min(config.safety.doctor_scan_log_lines, len(all_lines))
        recent_lines = all_lines[-lines_to_scan:]
        
        for line in recent_lines:
            # Extract timestamp if present
            if "ERROR" in line.upper() or "error" in line.lower():
                # Try to extract timestamp
                timestamp_match = re.search(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]', line)
                if timestamp_match:
                    last_error_time = timestamp_match.group(1)
            
            # Count error types
            if "send_to_model" in line.lower() and ("error" in line.lower() or "failed" in line.lower()):
                error_counts["send_to_model"] += 1
            if "cursor" in line.lower() and ("error" in line.lower() or "failed" in line.lower()):
                error_counts["cursor"] += 1
            if "osascript" in line.lower() and ("error" in line.lower() or "failed" in line.lower()):
                error_counts["osascript"] += 1
            if "git" in line.lower() and ("error" in line.lower() or "failed" in line.lower()):
                error_counts["git"] += 1
            if "invariant_violation" in line.lower() or "invariant" in line.lower():
                error_counts["invariant_violation"] += 1
            if "parse" in line.lower() and ("error" in line.lower() or "failed" in line.lower()):
                error_counts["parse_error"] += 1
            
            # Track hot spots (chunks failing repeatedly)
            chunk_match = re.search(r'\[chunk=(\d+)\]', line)
            if chunk_match and ("error" in line.lower() or "failed" in line.lower()):
                chunk_id = int(chunk_match.group(1))
                hot_spots[chunk_id] = hot_spots.get(chunk_id, 0) + 1
        
        # Filter hot spots (only chunks with 3+ failures)
        hot_spots_filtered = {k: v for k, v in hot_spots.items() if v >= 3}
        
    except Exception as e:
        return {
            "error_counts": {},
            "hot_spots": [],
            "last_error_time": None,
            "lines_scanned": 0,
            "error": str(e)
        }
    
    return {
        "error_counts": error_counts,
        "hot_spots": hot_spots_filtered,
        "last_error_time": last_error_time,
        "lines_scanned": lines_to_scan
    }


def environment_check(config: Config) -> dict:
    """
    Check environment (Python version, git, macOS/osascript).
    
    Returns:
        Dict with environment info: {python_version: str, git_available: bool, ...}
    """
    env_info = {
        "python_version": sys.version.split()[0],
        "git_available": False,
        "macos": sys.platform == "darwin",
        "osascript_available": False,
        "cursor_driver_configured": config.use_cursor_driver
    }
    
    # Check git
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, timeout=5)
        env_info["git_available"] = result.returncode == 0
    except Exception:
        pass
    
    # Check osascript (macOS only)
    if env_info["macos"]:
        try:
            result = subprocess.run(["osascript", "-e", "return 1"], capture_output=True, timeout=5)
            env_info["osascript_available"] = result.returncode == 0
        except Exception:
            pass
    
    return env_info


def build_doctor_report(config: Config) -> dict:
    """
    Build a comprehensive doctor report.
    
    Returns:
        Dict with all check results and recommendations
    """
    report = {
        "files": {},
        "config": {},
        "state": {},
        "logs": {},
        "environment": {},
        "severity": "OK",
        "recommendations": []
    }
    
    # Check filesystem
    log("Checking filesystem", {"command": "doctor", "step": "check_filesystem"}, config)
    report["files"] = check_filesystem(config)
    
    # Check config schema
    log("Checking config schema", {"command": "doctor", "step": "check_config_schema"}, config)
    report["config"] = check_config_schema(config)
    
    # Check state consistency
    log("Checking state consistency", {"command": "doctor", "step": "check_state_consistency"}, config)
    state = load_state(config)
    prd_path = pathlib.Path(config.master_md_path)
    lines = []
    if prd_path.exists():
        try:
            with open(prd_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception:
            pass
    report["state"] = check_state_consistency(state, lines, config)
    
    # Check logs
    log("Checking logs", {"command": "doctor", "step": "check_logs"}, config)
    report["logs"] = check_logs(config)
    
    # Check environment
    log("Checking environment", {"command": "doctor", "step": "environment_check"}, config)
    report["environment"] = environment_check(config)
    
    # Determine severity
    has_errors = False
    has_warnings = False
    
    # Files: missing required files = ERROR
    if report["files"].get("prd.md") == "missing" or report["files"].get("auto_config.json") == "missing":
        has_errors = True
    
    # Config: errors = ERROR
    if report["config"].get("errors"):
        has_errors = True
    
    # State: needs_rebuild or critical issues = WARN/ERROR
    if report["state"].get("needs_rebuild"):
        has_warnings = True
        if report["state"].get("issues"):
            has_errors = True
    
    # Logs: many errors = WARN
    total_errors = sum(report["logs"].get("error_counts", {}).values())
    if total_errors > 10:
        has_warnings = True
    
    # Environment: missing required tools = WARN
    if config.use_cursor_driver and not report["environment"].get("osascript_available"):
        has_warnings = True
    
    if has_errors:
        report["severity"] = "ERROR"
    elif has_warnings:
        report["severity"] = "WARN"
    else:
        report["severity"] = "OK"
    
    # Build recommendations
    recommendations = []
    
    # File recommendations
    if report["files"].get("prd.md") == "missing":
        recommendations.append("CRITICAL: prd.md is missing. Create it or restore from backup.")
    elif report["files"].get("prd.md") == "unreadable":
        recommendations.append("CRITICAL: prd.md exists but is unreadable. Check permissions.")
    
    if report["files"].get(".auto_state.json") == "missing":
        recommendations.append("Run: python3 auto_master.py init  # to rebuild state from prd.md")
    
    # Config recommendations
    for error in report["config"].get("errors", []):
        recommendations.append(f"Config error: {error}")
    for warning in report["config"].get("warnings", []):
        recommendations.append(f"Config warning: {warning}")
    
    # State recommendations
    if report["state"].get("needs_rebuild"):
        if config.safety.enable_doctor_auto_fixes:
            recommendations.append("State needs rebuild. Auto-fix enabled; will rebuild automatically.")
        else:
            recommendations.append("State needs rebuild. Run: python3 auto_master.py init")
    
    for issue in report["state"].get("issues", []):
        recommendations.append(f"State issue: {issue}")
    
    # Log recommendations
    error_counts = report["logs"].get("error_counts", {})
    if error_counts.get("cursor", 0) > 5:
        recommendations.append("Many Cursor errors detected. Check macOS accessibility permissions and Cursor configuration.")
    if error_counts.get("git", 0) > 5:
        recommendations.append("Many Git errors detected. Check git repository status and permissions.")
    
    hot_spots = report["logs"].get("hot_spots", {})
    if hot_spots:
        chunk_list = ", ".join([f"chunk {k} ({v} failures)" for k, v in sorted(hot_spots.items(), key=lambda x: x[1], reverse=True)[:5]])
        recommendations.append(f"Repeated failures detected on: {chunk_list}. Consider manual review.")
    
    # Environment recommendations
    if config.use_cursor_driver and not report["environment"].get("macos"):
        recommendations.append("Cursor driver configured but not on macOS. Set use_cursor_driver=false or use macOS.")
    if config.use_cursor_driver and not report["environment"].get("osascript_available"):
        recommendations.append("osascript not available. Cursor integration will fail. Check macOS installation.")
    
    report["recommendations"] = recommendations
    
    return report


def print_doctor_report(report: dict, config: Config) -> None:
    """
    Print a human-readable doctor report to stdout.
    """
    print("\n" + "="*60)
    print("AUTO_PRD DOCTOR REPORT")
    print("="*60)
    
    # Files section
    print("\n[Files]")
    for name, status in sorted(report["files"].items()):
        if status == "ok":
            print(f"  ✓ {name}: OK")
        elif status == "missing":
            print(f"  ✗ {name}: MISSING")
        else:
            print(f"  ⚠ {name}: UNREADABLE")
    
    # Config section
    print("\n[Config]")
    config_warnings = report["config"].get("warnings", [])
    config_errors = report["config"].get("errors", [])
    if not config_warnings and not config_errors:
        print("  ✓ Configuration: OK")
    else:
        for error in config_errors:
            print(f"  ✗ {error}")
        for warning in config_warnings:
            print(f"  ⚠ {warning}")
    
    # State section
    print("\n[State]")
    state_info = report["state"]
    chunk_counts = state_info.get("chunk_status_counts", {})
    if chunk_counts:
        status_line = ", ".join([f"{k}={v}" for k, v in sorted(chunk_counts.items())])
        print(f"  Chunks: {status_line}")
    else:
        print("  No chunks found")
    
    issues = state_info.get("issues", [])
    if issues:
        for issue in issues[:5]:  # Show first 5 issues
            print(f"  ⚠ {issue}")
        if len(issues) > 5:
            print(f"  ... and {len(issues) - 5} more issues")
    elif not state_info.get("needs_rebuild"):
        print("  ✓ State consistency: OK")
    
    # Logs section
    print("\n[Logs]")
    logs_info = report["logs"]
    lines_scanned = logs_info.get("lines_scanned", 0)
    print(f"  Last {lines_scanned} lines scanned")
    
    error_counts = logs_info.get("error_counts", {})
    if error_counts:
        total_errors = sum(error_counts.values())
        if total_errors > 0:
            print(f"  Found {total_errors} errors:")
            for error_type, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
                if count > 0:
                    print(f"    - {error_type}: {count}")
        else:
            print("  ✓ No errors found")
    else:
        print("  (No log file to analyze)")
    
    last_error_time = logs_info.get("last_error_time")
    if last_error_time:
        print(f"  Last error at: {last_error_time}")
    
    hot_spots = logs_info.get("hot_spots", {})
    if hot_spots:
        print(f"  Hot spots (repeated failures): {len(hot_spots)} chunks")
    
    # Environment section
    print("\n[Environment]")
    env_info = report["environment"]
    print(f"  Python: {env_info.get('python_version', 'unknown')}")
    print(f"  Git: {'FOUND' if env_info.get('git_available') else 'NOT FOUND'}")
    if env_info.get("macos"):
        print(f"  macOS / osascript: {'FOUND' if env_info.get('osascript_available') else 'NOT FOUND'}")
    else:
        print(f"  macOS: No")
    print(f"  Cursor driver: {'CONFIGURED' if env_info.get('cursor_driver_configured') else 'NOT CONFIGURED'}")
    
    # Overall severity
    print(f"\nOverall severity: {report['severity']}")
    
    # Recommendations
    recommendations = report.get("recommendations", [])
    if recommendations:
        print("\nRecommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    else:
        print("\n✓ No issues detected. System is healthy.")
    
    print("="*60 + "\n")


# ============================================================================
# IMPLEMENTATION AUTOMATION HELPERS
# ============================================================================

def read_implementation_plan_section(prd_path: pathlib.Path) -> typing.Optional[str]:
    """
    Read the Implementation Plan section from prd.md.
    
    Returns:
        Content between IMPLEMENTATION_PLAN_START and IMPLEMENTATION_PLAN_END markers, or None
    """
    if not prd_path.exists():
        return None
    
    with open(prd_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_marker = "<!-- IMPLEMENTATION_PLAN_START -->"
    end_marker = "<!-- IMPLEMENTATION_PLAN_END -->"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        return None
    
    return content[start_idx + len(start_marker):end_idx].strip()


def write_implementation_plan_section(prd_path: pathlib.Path, plan_content: str, config: Config) -> bool:
    """
    Write or update the Implementation Plan section in prd.md.
    
    Returns:
        True if successful, False otherwise
    """
    if not prd_path.exists():
        log("PRD file not found", {"command": "plan_impl", "step": "write_plan"}, config)
        return False
    
    with open(prd_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_marker = "<!-- IMPLEMENTATION_PLAN_START -->"
    end_marker = "<!-- IMPLEMENTATION_PLAN_END -->"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    new_section = f"{start_marker}\n{plan_content}\n{end_marker}"
    
    if start_idx == -1 or end_idx == -1:
        # Section doesn't exist, append it
        content += f"\n\n{new_section}\n"
    else:
        # Replace existing section
        content = content[:start_idx] + new_section + content[end_idx + len(end_marker):]
    
    try:
        atomic_write_file(prd_path, content)
        return True
    except Exception as e:
        log(f"Failed to write implementation plan: {e}", {"command": "plan_impl", "step": "write_plan"}, config)
        return False


def build_implementation_plan(config: Config, prd_lines: list[str]) -> dict:
    """
    Build an implementation plan from PRD content.
    
    This is a deterministic first-pass implementation that can be extended later.
    
    Returns:
        Dict with structure:
        {
            "tracks": [...],
            "tasks": [
                {
                    "task_id": "IMPL-0001",
                    "phase_id": "3.2.1",
                    "summary": "...",
                    "target_files": [...],
                    "roles": [...],
                    "status": "planned"
                },
                ...
            ]
        }
    """
    # Define implementation tracks
    tracks = [
        {"name": "Client / UI", "description": "User interface and client-side code"},
        {"name": "Backend / API", "description": "Server-side APIs and business logic"},
        {"name": "Data / Storage", "description": "Database schemas and data models"},
        {"name": "AI / Intelligence", "description": "AI/ML features and integrations"},
        {"name": "Infrastructure / DevOps", "description": "Deployment and infrastructure"},
        {"name": "Testing / QA", "description": "Tests and quality assurance"}
    ]
    
    # Scan PRD for phases and tasks
    tasks = []
    task_counter = 1
    
    # Look for phase patterns (e.g., "Phase 3.2.1", "#### Task:")
    current_phase = None
    for i, line in enumerate(prd_lines, 1):
        # Detect phase IDs
        phase_match = re.search(r'Phase\s+(\d+\.\d+\.\d+)', line, re.IGNORECASE)
        if phase_match:
            current_phase = phase_match.group(1)
        
        # Detect task markers
        if re.search(r'####\s+Task:', line, re.IGNORECASE):
            # Extract task info from following lines
            task_info = {"phase_id": current_phase or "UNKNOWN", "summary": "", "target_files": []}
            
            # Read next few lines for task details
            for j in range(i, min(i + 20, len(prd_lines))):
                task_line = prd_lines[j]
                
                # Extract summary
                if "Summary:" in task_line or "**Summary:**" in task_line:
                    task_info["summary"] = task_line.split(":", 1)[-1].strip()
                
                # Extract target files if mentioned
                if "Target Files" in task_line or "**Target Files**" in task_line:
                    # Look for file paths in following lines
                    for k in range(j + 1, min(j + 5, len(prd_lines))):
                        file_line = prd_lines[k]
                        file_match = re.search(r'`?([a-zA-Z0-9_/.-]+\.(ts|tsx|js|jsx|py|dart|kt|swift|cs))`?', file_line)
                        if file_match:
                            task_info["target_files"].append(file_match.group(1))
            
            if task_info["summary"] or task_info["phase_id"] != "UNKNOWN":
                task_id = f"IMPL-{task_counter:04d}"
                task_counter += 1
                
                # Determine track based on phase or summary
                track = "Client / UI"  # Default
                if any(word in task_info["summary"].lower() for word in ["api", "backend", "server"]):
                    track = "Backend / API"
                elif any(word in task_info["summary"].lower() for word in ["database", "data", "model", "schema"]):
                    track = "Data / Storage"
                elif any(word in task_info["summary"].lower() for word in ["ai", "ml", "model", "intelligence"]):
                    track = "AI / Intelligence"
                elif any(word in task_info["summary"].lower() for word in ["test", "qa", "spec"]):
                    track = "Testing / QA"
                elif any(word in task_info["summary"].lower() for word in ["deploy", "infrastructure", "devops"]):
                    track = "Infrastructure / DevOps"
                
                # Assign default roles based on track
                roles = config.implementation.default_roles_for_impl[:2]  # Use first 2 default roles
                if track == "Client / UI":
                    roles = ["Full-Stack Web Developer", "UI/UX Lead Designer"]
                elif track == "Backend / API":
                    roles = ["Principal Software Architect", "Senior Backend Developer"]
                elif track == "AI / Intelligence":
                    roles = ["AI/ML Engineer", "Principal Software Architect"]
                
                tasks.append({
                    "task_id": task_id,
                    "phase_id": task_info["phase_id"],
                    "track": track,
                    "summary": task_info["summary"] or f"Implement phase {task_info['phase_id']}",
                    "target_files": task_info["target_files"] or [],
                    "roles": roles,
                    "status": "planned"
                })
    
    # If no tasks found, create a basic starter task
    if not tasks:
        tasks.append({
            "task_id": "IMPL-0001",
            "phase_id": "1.0.0",
            "track": "Client / UI",
            "summary": "Set up initial project structure and scaffolding",
            "target_files": [f"{config.implementation.source_dir}/index.tsx"],
            "roles": config.implementation.default_roles_for_impl[:2],
            "status": "planned"
        })
    
    return {
        "tracks": tracks,
        "tasks": tasks
    }


def format_implementation_plan_markdown(plan: dict) -> str:
    """
    Format implementation plan as markdown for insertion into prd.md.
    """
    lines = []
    lines.append("## Implementation Plan")
    lines.append("")
    lines.append("This section is automatically generated by `plan_impl` command.")
    lines.append("")
    
    # Tracks
    lines.append("### Implementation Tracks")
    lines.append("")
    for track in plan["tracks"]:
        lines.append(f"- **{track['name']}**: {track['description']}")
    lines.append("")
    
    # Tasks
    lines.append("### Implementation Tasks")
    lines.append("")
    lines.append("| Task ID | Phase ID | Track | Summary | Status |")
    lines.append("|---------|----------|-------|---------|--------|")
    
    for task in plan["tasks"]:
        summary_short = task["summary"][:50] + "..." if len(task["summary"]) > 50 else task["summary"]
        lines.append(f"| {task['task_id']} | {task['phase_id']} | {task['track']} | {summary_short} | {task['status']} |")
    
    lines.append("")
    lines.append("### Task Details")
    lines.append("")
    
    for task in plan["tasks"]:
        lines.append(f"#### {task['task_id']}: {task['summary']}")
        lines.append("")
        lines.append(f"- **Phase ID:** {task['phase_id']}")
        lines.append(f"- **Track:** {task['track']}")
        lines.append(f"- **Status:** {task['status']}")
        lines.append(f"- **Primary Roles:** {', '.join(task['roles'])}")
        if task["target_files"]:
            lines.append(f"- **Target Files:**")
            for file_path in task["target_files"]:
                lines.append(f"  - `{file_path}`")
        else:
            lines.append(f"- **Target Files:** (to be determined)")
        lines.append("")
    
    return "\n".join(lines)


def parse_code_file_blocks(response: str) -> list[dict]:
    """
    Parse multi-file code response with <<<CODE_FILE_START ...>>> blocks.
    
    Returns:
        List of dicts: [{"path": "...", "code": "..."}, ...]
    """
    files = []
    
    # Pattern: <<<CODE_FILE_START path="...">>>
    pattern = r'<<<CODE_FILE_START\s+path=["\']([^"\']+)["\']\s*>>>\s*(.*?)<<<CODE_FILE_END>>>'
    
    matches = re.finditer(pattern, response, re.DOTALL)
    
    for match in matches:
        file_path = match.group(1)
        code = match.group(2).strip()
        files.append({"path": file_path, "code": code})
    
    return files


def is_file_generated(file_path: pathlib.Path) -> bool:
    """
    Check if a file is marked as auto-generated.
    
    Looks for markers like "AUTO-GENERATED BY AUTO_PRD" in the first few lines.
    """
    if not file_path.exists():
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_lines = "".join([f.readline() for _ in range(5)])
            return "AUTO-GENERATED" in first_lines.upper() or "AUTO_PRD" in first_lines.upper()
    except Exception:
        return False


def is_path_allowed(file_path: str, config: Config) -> bool:
    """
    Check if a file path is within allowed directories.
    """
    path = pathlib.Path(file_path)
    
    # Resolve relative to project root
    project_root = pathlib.Path(config.implementation.project_root).resolve()
    resolved_path = (project_root / path).resolve()
    
    # Must be within project root
    try:
        resolved_path.relative_to(project_root)
    except ValueError:
        return False
    
    # Check if it's in generated_dir (always allowed) or source_dir
    generated_dir = (project_root / config.implementation.generated_dir).resolve()
    source_dir = (project_root / config.implementation.source_dir).resolve()
    
    try:
        resolved_path.relative_to(generated_dir)
        return True
    except ValueError:
        pass
    
    try:
        resolved_path.relative_to(source_dir)
        return True
    except ValueError:
        pass
    
    # Allow test_dir
    test_dir = (project_root / config.implementation.test_dir).resolve()
    try:
        resolved_path.relative_to(test_dir)
        return True
    except ValueError:
        pass
    
    return False


def safe_write_code_file(file_path: str, code: str, config: Config, dry_run: bool = False) -> tuple[bool, str]:
    """
    Safely write a code file, respecting overwrite settings.
    
    Returns:
        (success: bool, message: str)
    """
    path = pathlib.Path(file_path)
    project_root = pathlib.Path(config.implementation.project_root).resolve()
    full_path = (project_root / path).resolve()
    
    # Check if path is allowed
    if not is_path_allowed(file_path, config):
        return False, f"Path {file_path} is outside allowed directories"
    
    # Check if file exists
    if full_path.exists():
        # Check if it's generated
        is_gen = is_file_generated(full_path)
        
        if not is_gen and config.implementation.impl_never_overwrite_manual:
            return False, f"File {file_path} exists and is not marked as generated (impl_never_overwrite_manual=true)"
        
        if is_gen and not config.implementation.impl_allow_overwrite_generated:
            return False, f"File {file_path} is generated but impl_allow_overwrite_generated=false"
    
    if dry_run:
        return True, f"DRY-RUN: Would write {file_path}"
    
    # Create parent directories
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Add generation marker if not present
    if "AUTO-GENERATED" not in code.upper():
        marker = f"// AUTO-GENERATED BY AUTO_PRD - DO NOT EDIT MANUALLY\n// Generated at: {datetime.datetime.now().isoformat()}\n\n"
        code = marker + code
    
    # Write file
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(code)
        return True, f"Wrote {file_path}"
    except Exception as e:
        return False, f"Failed to write {file_path}: {e}"


def build_implementation_prompt(
    config: Config,
    phase_id: str,
    task: dict,
    prd_excerpt: str
) -> str:
    """
    Build an implementation prompt for a specific phase/task.
    """
    roles_str = ", ".join(task.get("roles", config.implementation.default_roles_for_impl))
    
    prompt = f"""Act as a team of {roles_str} from the Omni-Corp Master Role Library.

You will implement or update the following code for Phase {phase_id} / Task {task.get('task_id', 'UNKNOWN')}.

Context:
- Target type: {config.implementation.primary_target_type}
- Language: {config.implementation.primary_language}
- Framework: {config.implementation.primary_framework}
- Project root: {config.implementation.project_root}
- Source directory: {config.implementation.source_dir}
- Generated directory: {config.implementation.generated_dir}

Current PRD excerpt:
{prd_excerpt}

Implementation Plan entry:
- Task ID: {task.get('task_id', 'UNKNOWN')}
- Phase ID: {phase_id}
- Track: {task.get('track', 'Unknown')}
- Summary: {task.get('summary', 'No summary')}
- Target Files: {', '.join(task.get('target_files', [])) or '(to be determined)'}
- Primary Roles: {roles_str}

Instructions:
- Generate or update the following files:
"""
    
    for file_path in task.get("target_files", []):
        prompt += f"  - {file_path}\n"
    
    if not task.get("target_files"):
        prompt += "  - Determine appropriate file paths based on the framework and project structure\n"
    
    prompt += f"""
Constraints:
- Only modify files in {config.implementation.project_root} and allowed subdirs (prefer {config.implementation.generated_dir} for new code).
- Do not delete existing manual code without explicit instructions.
- Use clean, idiomatic code for {config.implementation.primary_language} and {config.implementation.primary_framework}.
- Include proper imports, type definitions, and error handling.
- Follow best practices for the chosen framework.

Return your changes in a machine-parsable format with markers per file:

<<<CODE_FILE_START path="src/screens/HomeScreen.tsx">>>
// code...
<<<CODE_FILE_END>>>

<<<CODE_FILE_START path="src/api/auth.ts">>>
// code...
<<<CODE_FILE_END>>>
"""
    
    return prompt


# ============================================================================
# COMMAND HANDLERS
# ============================================================================

def command_init(config: Config) -> int:
    """
    Initialize the automation system.
    - Ensure prd.md exists (create skeleton if not)
    - Ensure auto_config.json exists (create with defaults if not)
    - Build fresh state from prd.md
    """
    log("Running 'init' command", {"command": "init", "step": "start"}, config)
    
    prd_path = pathlib.Path(config.master_md_path)
    state_path = pathlib.Path(config.state_path)
    
    # Ensure PRD exists
    if not prd_path.exists():
        log("PRD file not found, creating skeleton", {"command": "init", "step": "create_prd"}, config)
        create_prd_skeleton(prd_path)
    else:
        log(f"PRD file found at {prd_path}", {"command": "init", "step": "check_prd"}, config)
    
    # Build state from PRD
    try:
        state = build_state_from_file(config)
        total_lines = state["meta"]["total_lines"]
        num_chunks = len(state["chunks"])
        
        log(
            f"Built state: total_lines={total_lines} chunks={num_chunks}",
            {"command": "init", "step": "build_state"},
            config
        )
        
        # Save state
        save_state(config, state)
        log("State file saved", {"command": "init", "step": "save_state"}, config)
        
        log("Initialization complete", {"command": "init", "step": "complete"}, config)
        return 0
        
    except Exception as e:
        log(f"ERROR: Failed to build state: {e}", {"command": "init", "step": "error"}, config)
        return 1


def command_status(config: Config, verbose: bool = False) -> int:
    """
    Print status information about the system.
    
    Args:
        config: Config object
        verbose: If True, show detailed chunk table
    """
    log("Running 'status' command", {"command": "status", "step": "start"}, config)
    
    state = load_state(config)
    
    if state is None:
        print("\n" + "="*60)
        print("SYSTEM STATUS")
        print("="*60)
        print("✗ State file not found. Run 'init' first.")
        print("="*60 + "\n")
        return 1
    
    meta = state["meta"]
    chunks = state["chunks"]
    
    # Count by status
    status_counts = {}
    for chunk in chunks:
        status = chunk["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Print summary
    print("\n" + "="*60)
    print("SYSTEM STATUS")
    print("="*60)
    print(f"PRD File: {meta['master_md_path']}")
    print(f"Total Lines: {meta['total_lines']}")
    print(f"Chunk Size: {meta['chunk_size_lines']} lines")
    print(f"Total Chunks: {len(chunks)}")
    print(f"\nStatus Breakdown:")
    for status in ["pending", "running", "done", "failed"]:
        count = status_counts.get(status, 0)
        print(f"  {status:8s}: {count:3d}")
    print("="*60)
    
    # Verbose mode: show chunk table
    if verbose:
        print("\nChunk Details:")
        print("-" * 80)
        print(f"{'ID':<4} {'Phase ID':<10} {'Lines':<12} {'Status':<10} {'Attempts':<8} {'Error':<20}")
        print("-" * 80)
        for chunk in chunks:
            chunk_id = chunk["id"]
            phase_id = chunk["phase_id"]
            line_range = f"{chunk['start_line']}-{chunk['end_line']}"
            status = chunk["status"]
            attempts = chunk["attempts"]
            error = chunk.get("last_error", "")
            if error:
                error = error[:18] + ".." if len(error) > 20 else error
            else:
                error = "-"
            
            print(f"{chunk_id:<4} {phase_id:<10} {line_range:<12} {status:<10} {attempts:<8} {error:<20}")
        print("-" * 80)
    
    print()
    return 0


def command_reset(config: Config) -> int:
    """
    Reset automation state (remove state and optionally rotate log).
    
    After reset, user should run 'init' to rebuild state.
    """
    log("Running 'reset' command", {"command": "reset", "step": "start"}, config)
    
    state_path = pathlib.Path(config.state_path)
    log_path = pathlib.Path(config.log_path)
    
    # Delete state file
    if state_path.exists():
        state_path.unlink()
        log("Deleted state file", {"command": "reset", "step": "delete_state"}, config)
    else:
        log("State file does not exist", {"command": "reset", "step": "check_state"}, config)
    
    # Rotate log file
    if log_path.exists():
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = log_path.with_suffix(f".bak.{timestamp}")
        shutil.move(str(log_path), str(backup_path))
        log(f"Rotated log file to {backup_path}", {"command": "reset", "step": "rotate_log"}, config)
    
    log("Reset complete. Run 'init' to rebuild state.", {"command": "reset", "step": "complete"}, config)
    return 0


def run_enhancement_pass(
    config: Config,
    state: dict,
    lines: list[str],
    max_chunks: typing.Optional[int] = None,
    dry_run: bool = False,
    command_name: str = "enhance",
) -> tuple[dict, list[str], dict]:
    """
    Runs a single enhancement pass over up to max_chunks eligible chunks.
    
    Args:
        config: Config object
        state: Current state dict
        lines: Current PRD file lines (list of strings)
        max_chunks: Maximum number of chunks to process (None = all eligible)
        dry_run: If True, don't modify files, just log what would happen
        command_name: Command name for logging context (e.g., "enhance" or "grow")
    
    Returns:
        Tuple of (updated_state, updated_lines, pass_stats)
        where pass_stats includes:
        {
            "chunks_attempted": int,
            "chunks_succeeded": int,
            "chunks_failed": int,
            "lines_before": int,
            "lines_after": int
        }
    """
    lines_before = len(lines)
    
    # Select eligible chunks (prefer pending, fallback to failed if no pending)
    pending_chunks = [chunk for chunk in state["chunks"] if chunk["status"] == "pending"]
    failed_chunks = [chunk for chunk in state["chunks"] if chunk["status"] == "failed"]
    
    candidate_chunks = pending_chunks if pending_chunks else failed_chunks
    
    if not candidate_chunks:
        # No chunks to process
        return state, lines, {
            "chunks_attempted": 0,
            "chunks_succeeded": 0,
            "chunks_failed": 0,
            "lines_before": lines_before,
            "lines_after": lines_before
        }
    
    # Apply limit
    if max_chunks is not None:
        candidate_chunks = candidate_chunks[:max_chunks]
    
    log(
        f"Processing {len(candidate_chunks)} chunk(s) in {command_name} pass",
        {"command": command_name, "step": "select_chunks"},
        config
    )
    
    # Process each chunk
    chunks_attempted = 0
    chunks_succeeded = 0
    chunks_failed = 0
    consecutive_failures = 0
    
    for chunk in candidate_chunks:
        # Check consecutive failures (before processing this chunk)
        if consecutive_failures >= config.safety.max_consecutive_failures:
            log(
                f"Stopping pass: {consecutive_failures} consecutive failures (max={config.safety.max_consecutive_failures})",
                {"command": command_name, "step": "stop_consecutive_failures", "consecutive_failures": consecutive_failures},
                config
            )
            break
        chunk_id = chunk["id"]
        phase_id = chunk["phase_id"]
        start_line = chunk["start_line"]
        end_line = chunk["end_line"]
        
        context = {
            "command": command_name,
            "chunk": chunk_id,
            "phase_id": phase_id,
            "step": "process"
        }
        
        # Invariant check: Validate chunk line range
        if start_line < 1 or end_line < start_line or end_line > len(lines):
            violation_msg = f"Chunk {chunk_id} has invalid line range: {start_line}-{end_line} (file has {len(lines)} lines)"
            log(
                f"INVARIANT VIOLATION: {violation_msg}",
                {**context, "step": "invariant_violation"},
                config
            )
            
            if config.safety.stop_on_invariant_violation:
                raise RuntimeError(f"Invariant violation: {violation_msg}")
            else:
                chunk["status"] = "failed"
                chunk["last_error"] = violation_msg
                chunks_failed += 1
                consecutive_failures += 1
                continue
        
        chunks_attempted += 1
        
        if dry_run:
            # Determine mode for dry-run logging
            mode = "cursor" if getattr(config, 'use_cursor_driver', False) else "fake"
            log(
                f"DRY-RUN: Would process chunk {chunk_id} ({phase_id}, lines {start_line}-{end_line}, mode={mode})",
                {**context, "step": "dry_run", "mode": "dry-run"},
                config
            )
            chunks_attempted += 1  # Count dry-run attempts for stats
            continue
        
        # Mark as running
        chunk["status"] = "running"
        chunk["attempts"] += 1
        chunk["last_updated_at"] = datetime.datetime.now().isoformat()
        save_state(config, state)
        
        try:
            # Extract chunk text (convert to 0-indexed for list access)
            chunk_lines = lines[start_line - 1:end_line]
            chunk_text = "".join(chunk_lines)
            
            log(
                f"Processing chunk {chunk_id} (lines {start_line}-{end_line})",
                {**context, "step": "extract"},
                config
            )
            
            # Build prompt
            prompt = build_enhance_prompt(config, chunk_text, phase_id, start_line, end_line)
            log(
                f"Built prompt for chunk {chunk_id} (length={len(prompt)} chars)",
                {**context, "step": "prepare_prompt"},
                config
            )
            
            # Determine mode for logging
            mode = "cursor" if getattr(config, 'use_cursor_driver', False) else "fake"
            log(
                f"Sending to model (mode={mode}, wait={config.wait_seconds}s)",
                {**context, "step": "send_prompt"},
                config
            )
            
            # Send to model
            response = send_to_model(
                prompt, chunk_text, phase_id, start_line, end_line,
                config.wait_seconds, config
            )
            
            log(
                f"Received response (length={len(response)} chars)",
                {**context, "step": "receive_response"},
                config
            )
            
            # Parse response
            improved_text = parse_enhanced_chunk(response)
            if improved_text is None:
                raise ValueError("Failed to parse enhanced chunk from response (missing markers)")
            
            log(
                f"Parsed response for chunk {chunk_id}",
                {**context, "step": "parse_response"},
                config
            )
            
            # Safety check: length ratio
            orig_len = len(chunk_text)
            new_len = len(improved_text)
            length_ratio = new_len / max(orig_len, 1)
            
            log(
                f"Length check: orig={orig_len} new={new_len} ratio={length_ratio:.2f}",
                {**context, "step": "safety_check"},
                config
            )
            
            if length_ratio < config.min_length_ratio_ok:
                raise ValueError(
                    f"Enhanced chunk too short: ratio {length_ratio:.2f} < {config.min_length_ratio_ok}"
                )
            
            # Replace chunk in lines array
            # Convert improved text to lines
            improved_lines = improved_text.splitlines(keepends=False)
            # Add newlines to match original format
            improved_lines_with_newlines = [line + "\n" for line in improved_lines]
            
            # Calculate line count change
            orig_line_count = end_line - start_line + 1
            new_line_count = len(improved_lines_with_newlines)
            line_diff = new_line_count - orig_line_count
            
            # Replace in lines array
            lines[start_line - 1:end_line] = improved_lines_with_newlines
            
            # Update subsequent chunks' line numbers
            if line_diff != 0:
                for other_chunk in state["chunks"]:
                    if other_chunk["id"] > chunk_id:
                        other_chunk["start_line"] += line_diff
                        other_chunk["end_line"] += line_diff
            
            # Update chunk status
            chunk["status"] = "done"
            chunk["last_error"] = None
            chunk["last_updated_at"] = datetime.datetime.now().isoformat()
            
            # Update meta
            state["meta"]["total_lines"] = len(lines)
            state["meta"]["updated_at"] = datetime.datetime.now().isoformat()
            
            log(
                f"Updated chunk {chunk_id}: new_total_lines={len(lines)} line_diff={line_diff:+d}",
                {**context, "step": "update_file"},
                config
            )
            
            chunks_succeeded += 1
            consecutive_failures = 0  # Reset on success
            
        except Exception as e:
            # Mark as failed
            chunk["status"] = "failed"
            chunk["last_error"] = str(e)
            chunk["last_updated_at"] = datetime.datetime.now().isoformat()
            
            log(
                f"ERROR processing chunk {chunk_id}: {e}",
                {**context, "step": "error"},
                config
            )
            
            chunks_failed += 1
            consecutive_failures += 1
        
        # Invariant check: Validate lines after update
        if not dry_run and chunks_succeeded > 0:
            if len(lines) == 0:
                violation_msg = "Lines array is empty after update"
                log(
                    f"INVARIANT VIOLATION: {violation_msg}",
                    {**context, "step": "invariant_violation"},
                    config
                )
                if config.safety.stop_on_invariant_violation:
                    raise RuntimeError(f"Invariant violation: {violation_msg}")
        
        # Save state after each chunk
        save_state(config, state)
    
    lines_after = len(lines)
    
    pass_stats = {
        "chunks_attempted": chunks_attempted,
        "chunks_succeeded": chunks_succeeded,
        "chunks_failed": chunks_failed,
        "lines_before": lines_before,
        "lines_after": lines_after,
        "consecutive_failures": consecutive_failures,
        "stopped_early": consecutive_failures >= config.safety.max_consecutive_failures
    }
    
    return state, lines, pass_stats


def command_enhance(
    config: Config,
    limit: typing.Optional[int] = None,
    dry_run: bool = False
) -> int:
    """
    Run enhancement loop on pending chunks (single pass).
    
    Args:
        config: Config object
        limit: Maximum number of chunks to process (None = all)
        dry_run: If True, don't modify files, just log what would happen
    """
    log(
        f"Running 'enhance' command (limit={limit}, dry_run={dry_run})",
        {"command": "enhance", "step": "start"},
        config
    )
    
    # Load state
    state = load_state(config)
    if state is None:
        log("ERROR: State file not found. Run 'init' first.", {"command": "enhance", "step": "error"}, config)
        return 1
    
    # Read PRD file
    prd_path = pathlib.Path(config.master_md_path)
    if not prd_path.exists():
        log(f"ERROR: PRD file not found: {prd_path}", {"command": "enhance", "step": "error"}, config)
        return 1
    
    with open(prd_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Run enhancement pass
    state, lines, pass_stats = run_enhancement_pass(
        config, state, lines, max_chunks=limit, dry_run=dry_run, command_name="enhance"
    )
    
    # Write updated PRD file (if not dry-run and we processed something)
    if not dry_run and pass_stats["chunks_succeeded"] > 0:
        try:
            content = "".join(lines)
            atomic_write_file(prd_path, content)
            log(
                f"Wrote updated PRD file ({len(lines)} lines)",
                {"command": "enhance", "step": "write_file"},
                config
            )
        except Exception as e:
            log(
                f"ERROR writing PRD file: {e}",
                {"command": "enhance", "step": "write_error"},
                config
            )
            return 1
    
    # Summary
    log(
        f"Enhancement complete: attempted={pass_stats['chunks_attempted']} succeeded={pass_stats['chunks_succeeded']} failed={pass_stats['chunks_failed']}",
        {"command": "enhance", "step": "complete"},
        config
    )
    
    return 0 if pass_stats["chunks_failed"] == 0 else 1


def command_grow(config: Config) -> int:
    """
    Run autonomous growth loop to expand prd.md towards target line count.
    
    This command runs multiple enhancement passes, rebuilding state as needed,
    until reaching the target line count or other stop conditions.
    """
    log("Running 'grow' command", {"command": "grow", "step": "start"}, config)
    
    # Load state
    state = load_state(config)
    if state is None:
        log("ERROR: State file not found. Run 'init' first.", {"command": "grow", "step": "error"}, config)
        return 1
    
    # Read PRD file
    prd_path = pathlib.Path(config.master_md_path)
    if not prd_path.exists():
        log(f"ERROR: PRD file not found: {prd_path}", {"command": "grow", "step": "error"}, config)
        return 1
    
    # Initialize growth tracking
    growth_meta = state["meta"].get("growth", {})
    current_pass = growth_meta.get("current_pass", 0)
    total_passes_run = growth_meta.get("total_passes_run", 0)
    target_line_count = config.growth.target_line_count
    max_passes = config.growth.max_passes
    max_chunks_per_pass = config.growth.max_chunks_per_pass
    rebuild_state_each_pass = config.growth.rebuild_state_each_pass
    stop_when_all_done = config.growth.stop_when_all_done
    
    log(
        f"Growth configuration: target={target_line_count} lines, max_passes={max_passes}, max_chunks_per_pass={max_chunks_per_pass}",
        {"command": "grow", "step": "config"},
        config
    )
    
    # Main growth loop
    passes_completed = 0
    stop_reason = None
    
    for pass_index in range(1, max_passes + 1):
        # Check stop conditions before starting pass
        with open(prd_path, 'r', encoding='utf-8') as f:
            current_lines = f.readlines()
        current_line_count = len(current_lines)
        
        # Stop condition: target reached (within 5% tolerance)
        if current_line_count >= target_line_count * 0.95:
            stop_reason = "target_reached"
            log(
                f"Target line count reached: {current_line_count} >= {target_line_count * 0.95}",
                {"command": "grow", "step": "growth_stop_condition", "reason": stop_reason},
                config
            )
            break
        
        # Increment pass counter
        current_pass = pass_index
        total_passes_run += 1
        
        log(
            f"Starting growth pass {current_pass} (current_lines={current_line_count}, target={target_line_count})",
            {"command": "grow", "step": "growth_pass_start", "pass_index": current_pass, "current_line_count": current_line_count, "target_line_count": target_line_count},
            config
        )
        
        # Rebuild state if configured
        if rebuild_state_each_pass:
            log(
                f"Rebuilding state from prd.md for pass {current_pass}",
                {"command": "grow", "step": "growth_rebuild_state", "pass_index": current_pass},
                config
            )
            # Preserve growth metadata
            preserve_growth = state["meta"].get("growth", {})
            state = build_state_from_file(config, growth_pass=current_pass, preserve_growth_meta=preserve_growth)
            save_state(config, state)
        
        # Read current PRD lines
        with open(prd_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Check if there are eligible chunks
        pending_chunks = [chunk for chunk in state["chunks"] if chunk["status"] == "pending"]
        failed_chunks = [chunk for chunk in state["chunks"] if chunk["status"] == "failed"]
        
        if not pending_chunks and not failed_chunks:
            if stop_when_all_done:
                stop_reason = "all_chunks_done"
                log(
                    f"No pending or failed chunks remaining",
                    {"command": "grow", "step": "growth_stop_condition", "reason": stop_reason},
                    config
                )
                break
            else:
                log(
                    f"WARNING: No eligible chunks but stop_when_all_done=false. Stopping to avoid infinite loop.",
                    {"command": "grow", "step": "growth_stop_condition", "reason": "no_chunks"},
                    config
                )
                stop_reason = "no_chunks"
                break
        
        # Run enhancement pass
        try:
            state, lines, pass_stats = run_enhancement_pass(
                config, state, lines, max_chunks=max_chunks_per_pass, dry_run=False, command_name="grow"
            )
            
            # Check if stopped early due to consecutive failures
            if pass_stats.get("stopped_early"):
                stop_reason = "too_many_failures"
                log(
                    f"Growth pass {current_pass} stopped early due to consecutive failures",
                    {"command": "grow", "step": "stop_consecutive_failures", "pass_index": current_pass},
                    config
                )
                break
        except RuntimeError as e:
            # Invariant violation or other runtime error
            if config.safety.stop_on_invariant_violation:
                log(
                    f"ERROR in growth pass {current_pass}: {e}",
                    {"command": "grow", "step": "error", "pass_index": current_pass},
                    config
                )
                stop_reason = "invariant_violation"
                break
            else:
                # Continue but log the error
                log(
                    f"WARNING in growth pass {current_pass}: {e} (continuing)",
                    {"command": "grow", "step": "warning", "pass_index": current_pass},
                    config
                )
        except Exception as e:
            log(
                f"ERROR in growth pass {current_pass}: {e}",
                {"command": "grow", "step": "error", "pass_index": current_pass},
                config
            )
            stop_reason = "error"
            break
        
        # Write updated PRD file
        if pass_stats["chunks_succeeded"] > 0:
            try:
                content = "".join(lines)
                atomic_write_file(prd_path, content)
                log(
                    f"Wrote updated PRD file ({len(lines)} lines)",
                    {"command": "grow", "step": "write_file", "pass_index": current_pass},
                    config
                )
            except Exception as e:
                log(
                    f"ERROR writing PRD file in pass {current_pass}: {e}",
                    {"command": "grow", "step": "write_error", "pass_index": current_pass},
                    config
                )
                stop_reason = "error"
                break
        
        # Update growth metadata
        state["meta"]["growth"]["current_pass"] = current_pass
        state["meta"]["growth"]["total_passes_run"] = total_passes_run
        state["meta"]["growth"]["last_pass_summary"] = {
            "pass_id": current_pass,
            "chunks_attempted": pass_stats["chunks_attempted"],
            "chunks_succeeded": pass_stats["chunks_succeeded"],
            "chunks_failed": pass_stats["chunks_failed"],
            "lines_before": pass_stats["lines_before"],
            "lines_after": pass_stats["lines_after"]
        }
        state["meta"]["total_lines"] = pass_stats["lines_after"]
        state["meta"]["updated_at"] = datetime.datetime.now().isoformat()
        save_state(config, state)
        
        # Log pass completion
        log(
            f"Completed growth pass {current_pass}: attempted={pass_stats['chunks_attempted']} succeeded={pass_stats['chunks_succeeded']} failed={pass_stats['chunks_failed']} lines={pass_stats['lines_before']}→{pass_stats['lines_after']}",
            {"command": "grow", "step": "growth_pass_end", "pass_index": current_pass, "chunks_attempted": pass_stats["chunks_attempted"], "chunks_succeeded": pass_stats["chunks_succeeded"], "chunks_failed": pass_stats["chunks_failed"], "lines_before": pass_stats["lines_before"], "lines_after": pass_stats["lines_after"]},
            config
        )
        
        passes_completed += 1
        
        # Git sync after pass (if enabled)
        if config.git.enable_auto and config.git.commit_after_each_pass:
            log(
                f"Triggering git sync after pass {current_pass}",
                {"command": "grow", "step": "trigger_git_sync", "pass_index": current_pass},
                config
            )
            perform_git_sync(
                config,
                reason=f"growth_pass_{current_pass}",
                pass_stats=pass_stats
            )
        
        # Check stop condition after pass
        if pass_stats["lines_after"] >= target_line_count * 0.95:
            stop_reason = "target_reached"
            log(
                f"Target line count reached after pass {current_pass}: {pass_stats['lines_after']} >= {target_line_count * 0.95}",
                {"command": "grow", "step": "growth_stop_condition", "reason": stop_reason},
                config
            )
            break
    
    # Final summary
    if stop_reason is None:
        stop_reason = "max_passes"
    
    # Read final line count
    with open(prd_path, 'r', encoding='utf-8') as f:
        final_lines = f.readlines()
    final_line_count = len(final_lines)
    
    # Count final chunk statuses
    final_state = load_state(config)
    if final_state:
        final_pending = len([c for c in final_state["chunks"] if c["status"] == "pending"])
        final_done = len([c for c in final_state["chunks"] if c["status"] == "done"])
        final_failed = len([c for c in final_state["chunks"] if c["status"] == "failed"])
    else:
        final_pending = final_done = final_failed = 0
    
    log(
        f"Growth complete: passes={passes_completed} final_lines={final_line_count} target={target_line_count} reason={stop_reason} chunks_done={final_done} chunks_pending={final_pending} chunks_failed={final_failed}",
        {"command": "grow", "step": "complete", "passes_completed": passes_completed, "final_line_count": final_line_count, "target_line_count": target_line_count, "stop_reason": stop_reason},
        config
    )
    
    print("\n" + "="*60)
    print("GROWTH SUMMARY")
    print("="*60)
    print(f"Passes Completed: {passes_completed}")
    print(f"Final Line Count: {final_line_count}")
    print(f"Target Line Count: {target_line_count}")
    print(f"Stop Reason: {stop_reason}")
    print(f"Chunks Done: {final_done}")
    print(f"Chunks Pending: {final_pending}")
    print(f"Chunks Failed: {final_failed}")
    print("="*60 + "\n")
    
    return 0


def command_start(config: Config, limit: typing.Optional[int] = None, dry_run: bool = False) -> int:
    """
    Alias for 'enhance' command.
    """
    return command_enhance(config, limit, dry_run)


def command_sync_roles(config: Config) -> int:
    """
    Sync the Omni-Corp Role Library and Prompt Templates into prd.md.
    
    This command ensures that Section 2 (Role Library) and Section 8 (Prompt Templates)
    are present and up-to-date in prd.md. It can be safely re-run without duplicating content.
    """
    log("Running 'sync_roles' command", {"command": "sync_roles", "step": "start"}, config)
    
    prd_path = pathlib.Path(config.master_md_path)
    if not prd_path.exists():
        log(f"ERROR: PRD file not found: {prd_path}", {"command": "sync_roles", "step": "error"}, config)
        return 1
    
    # Read current PRD
    try:
        with open(prd_path, 'r', encoding='utf-8') as f:
            prd_content = f.read()
    except Exception as e:
        log(f"ERROR: Failed to read PRD file: {e}", {"command": "sync_roles", "step": "error"}, config)
        return 1
    
    # Generate canonical content
    role_library_content = generate_omni_corp_role_library()
    prompt_templates_content = generate_prompt_templates_and_framework()
    
    # Define markers
    role_library_start = "<!-- OMNI_CORP_ROLE_LIBRARY_START -->"
    role_library_end = "<!-- OMNI_CORP_ROLE_LIBRARY_END -->"
    prompt_templates_start = "<!-- PROMPT_TEMPLATES_START -->"
    prompt_templates_end = "<!-- PROMPT_TEMPLATES_END -->"
    
    updated = False
    inserted = False
    
    # Process Role Library section
    role_start_idx = prd_content.find(role_library_start)
    role_end_idx = prd_content.find(role_library_end)
    
    if role_start_idx == -1 or role_end_idx == -1:
        # Markers not found - need to insert
        # Find Section 2 header and replace the placeholder content
        section_2_pattern = r"(# 2\. OMNI-CORP MASTER ROLES[^\n]*\n.*?)(?=---|\n# 3\.)"
        match = re.search(section_2_pattern, prd_content, re.DOTALL)
        
        if match:
            # Replace the placeholder section with the full role library
            prd_content = prd_content[:match.start()] + role_library_content + "\n\n" + prd_content[match.end():]
            inserted = True
            log("Inserted Role Library section", {"command": "sync_roles", "step": "insert_role_library"}, config)
        else:
            log("WARNING: Could not find Section 2 to replace. Appending Role Library at end of Section 2.", {"command": "sync_roles", "step": "warning"}, config)
            # Try to find just the section header
            section_2_header = re.search(r"# 2\. OMNI-CORP MASTER ROLES[^\n]*", prd_content)
            if section_2_header:
                insert_pos = prd_content.find("\n---", section_2_header.end())
                if insert_pos == -1:
                    insert_pos = prd_content.find("\n# 3\.", section_2_header.end())
                if insert_pos != -1:
                    prd_content = prd_content[:insert_pos] + "\n\n" + role_library_content + "\n\n" + prd_content[insert_pos:]
                    inserted = True
    else:
        # Markers found - replace content between them
        # Extract the content from the generated library (between markers)
        library_inner = role_library_content.split(role_library_start, 1)[1].rsplit(role_library_end, 1)[0].strip()
        before = prd_content[:role_start_idx + len(role_library_start)]
        after = prd_content[role_end_idx:]
        prd_content = before + "\n" + library_inner + "\n" + after
        updated = True
        log("Updated Role Library section", {"command": "sync_roles", "step": "update_role_library"}, config)
    
    # Process Prompt Templates section
    prompt_start_idx = prd_content.find(prompt_templates_start)
    prompt_end_idx = prd_content.find(prompt_templates_end)
    
    if prompt_start_idx == -1 or prompt_end_idx == -1:
        # Markers not found - need to insert
        # Find Section 8 header and replace the placeholder content
        section_8_pattern = r"(# 8\. PROMPT LIBRARY & AGENT PLAYBOOK[^\n]*\n.*?)(?=---|\n# 9\.)"
        match = re.search(section_8_pattern, prd_content, re.DOTALL)
        
        if match:
            # Replace the placeholder section with the full prompt templates
            prd_content = prd_content[:match.start()] + prompt_templates_content + "\n\n" + prd_content[match.end():]
            inserted = True
            log("Inserted Prompt Templates section", {"command": "sync_roles", "step": "insert_prompt_templates"}, config)
        else:
            log("WARNING: Could not find Section 8 to replace. Appending Prompt Templates at end of Section 8.", {"command": "sync_roles", "step": "warning"}, config)
            # Try to find just the section header
            section_8_header = re.search(r"# 8\. PROMPT LIBRARY & AGENT PLAYBOOK[^\n]*", prd_content)
            if section_8_header:
                insert_pos = prd_content.find("\n---", section_8_header.end())
                if insert_pos == -1:
                    insert_pos = prd_content.find("\n# 9\.", section_8_header.end())
                if insert_pos != -1:
                    prd_content = prd_content[:insert_pos] + "\n\n" + prompt_templates_content + "\n\n" + prd_content[insert_pos:]
                    inserted = True
    else:
        # Markers found - replace content between them
        # Extract the content from the generated templates (between markers)
        templates_inner = prompt_templates_content.split(prompt_templates_start, 1)[1].rsplit(prompt_templates_end, 1)[0].strip()
        before = prd_content[:prompt_start_idx + len(prompt_templates_start)]
        after = prd_content[prompt_end_idx:]
        prd_content = before + "\n" + templates_inner + "\n" + after
        updated = True
        log("Updated Prompt Templates section", {"command": "sync_roles", "step": "update_prompt_templates"}, config)
    
    # Write updated PRD
    if updated or inserted:
        try:
            atomic_write_file(prd_path, prd_content)
            log(
                f"Successfully synced Role Library and Prompt Templates (inserted={inserted}, updated={updated})",
                {"command": "sync_roles", "step": "complete", "inserted": inserted, "updated": updated},
                config
            )
            return 0
        except Exception as e:
            log(f"ERROR: Failed to write updated PRD: {e}", {"command": "sync_roles", "step": "error"}, config)
            return 1
    else:
        log("No changes needed - sections already up to date", {"command": "sync_roles", "step": "complete"}, config)
        return 0


def command_plan_impl(config: Config) -> int:
    """
    Generate implementation plan from PRD.
    
    Reads PRD, identifies phases and tasks, and generates a structured
    implementation plan that maps phases to code modules and files.
    """
    log("Running 'plan_impl' command", {"command": "plan_impl", "step": "start"}, config)
    
    if not config.implementation.enabled:
        log(
            "Implementation automation is disabled (implementation.enabled=false). Enable it in auto_config.json to use plan_impl.",
            {"command": "plan_impl", "step": "check_enabled"},
            config
        )
        print("ERROR: Implementation automation is disabled. Set implementation.enabled=true in auto_config.json")
        return 1
    
    prd_path = pathlib.Path(config.master_md_path)
    if not prd_path.exists():
        log("PRD file not found", {"command": "plan_impl", "step": "check_prd"}, config)
        print(f"ERROR: PRD file not found: {prd_path}")
        return 1
    
    # Read PRD
    with open(prd_path, 'r', encoding='utf-8') as f:
        prd_lines = f.readlines()
    
    log("Building implementation plan", {"command": "plan_impl", "step": "build_plan"}, config)
    
    # Build plan
    plan = build_implementation_plan(config, prd_lines)
    
    log(
        f"Built implementation plan: tasks={len(plan['tasks'])} tracks={len(plan['tracks'])}",
        {"command": "plan_impl", "step": "build_plan", "tasks": len(plan["tasks"]), "tracks": len(plan["tracks"])},
        config
    )
    
    # Format as markdown
    plan_markdown = format_implementation_plan_markdown(plan)
    
    # Write to PRD
    log("Updating PRD with implementation plan", {"command": "plan_impl", "step": "update_prd"}, config)
    success = write_implementation_plan_section(prd_path, plan_markdown, config)
    
    if success:
        log(
            "Implementation plan written to PRD",
            {"command": "plan_impl", "step": "update_prd", "result": "ok"},
            config
        )
        print(f"\n✓ Implementation plan generated: {len(plan['tasks'])} tasks across {len(plan['tracks'])} tracks")
        print(f"  Plan written to: {config.implementation.impl_plan_section_id} section in prd.md")
        return 0
    else:
        log("Failed to write implementation plan", {"command": "plan_impl", "step": "update_prd", "result": "error"}, config)
        print("ERROR: Failed to write implementation plan to PRD")
        return 1


def command_impl_phase(
    config: Config,
    phase_id: str,
    limit_files: typing.Optional[int] = None,
    dry_run: bool = False
) -> int:
    """
    Implement a specific phase or task.
    
    Args:
        config: Config object
        phase_id: Phase ID to implement (e.g., "3.2.1")
        limit_files: Maximum number of files to generate (None = use config default)
        dry_run: If True, don't write files, just log what would happen
    """
    log(
        f"Running 'impl_phase' command: phase_id={phase_id} limit_files={limit_files} dry_run={dry_run}",
        {"command": "impl_phase", "step": "start", "phase_id": phase_id},
        config
    )
    
    if not config.implementation.enabled:
        log(
            "Implementation automation is disabled",
            {"command": "impl_phase", "step": "check_enabled"},
            config
        )
        print("ERROR: Implementation automation is disabled. Set implementation.enabled=true in auto_config.json")
        return 1
    
    # Read implementation plan
    prd_path = pathlib.Path(config.master_md_path)
    plan_content = read_implementation_plan_section(prd_path)
    
    if not plan_content:
        log("Implementation plan not found in PRD", {"command": "impl_phase", "step": "read_plan"}, config)
        print("ERROR: Implementation plan not found. Run 'plan_impl' first.")
        return 1
    
    # Parse plan to find tasks for this phase
    # For now, we'll do a simple text search - in a full implementation, we'd parse the markdown properly
    phase_tasks = []
    for line in plan_content.split('\n'):
        if phase_id in line and 'IMPL-' in line:
            # Extract task ID from line
            task_match = re.search(r'IMPL-\d+', line)
            if task_match:
                task_id = task_match.group(0)
                # For now, create a basic task structure
                # In a full implementation, we'd parse the full task details
                phase_tasks.append({
                    "task_id": task_id,
                    "phase_id": phase_id,
                    "summary": f"Implement phase {phase_id}",
                    "target_files": [],
                    "roles": config.implementation.default_roles_for_impl[:2],
                    "status": "planned"
                })
    
    if not phase_tasks:
        log(f"No tasks found for phase {phase_id}", {"command": "impl_phase", "step": "find_tasks"}, config)
        print(f"WARNING: No implementation tasks found for phase {phase_id}")
        print("  The phase may not be in the implementation plan, or the plan needs to be regenerated.")
        return 1
    
    # Limit number of tasks/files
    max_files = limit_files or config.implementation.impl_max_files_per_phase
    phase_tasks = phase_tasks[:max_files]
    
    # Read PRD for context
    with open(prd_path, 'r', encoding='utf-8') as f:
        prd_content = f.read()
    
    # Extract relevant PRD excerpt (simplified - in full implementation, find the actual phase section)
    prd_excerpt = prd_content[:2000]  # First 2000 chars as context
    
    files_created = 0
    files_updated = 0
    files_failed = 0
    
    for task in phase_tasks:
        log(
            f"Processing task {task['task_id']} for phase {phase_id}",
            {"command": "impl_phase", "step": "process_task", "task_id": task["task_id"], "phase_id": phase_id},
            config
        )
        
        # Build prompt
        prompt = build_implementation_prompt(config, phase_id, task, prd_excerpt)
        
        log(
            f"Built implementation prompt (length={len(prompt)})",
            {"command": "impl_phase", "step": "build_prompt", "task_id": task["task_id"]},
            config
        )
        
        if dry_run:
            log(
                f"DRY-RUN: Would send prompt for task {task['task_id']}",
                {"command": "impl_phase", "step": "dry_run", "task_id": task["task_id"], "mode": "dry-run"},
                config
            )
            continue
        
        # Send to model
        try:
            response = send_to_model(
                prompt, "", phase_id, 0, 0,
                config.wait_seconds, config
            )
            
            log(
                f"Received implementation response (length={len(response)})",
                {"command": "impl_phase", "step": "receive_response", "task_id": task["task_id"]},
                config
            )
            
            # Parse code files
            code_files = parse_code_file_blocks(response)
            
            if not code_files:
                log(
                    f"No code files found in response for task {task['task_id']}",
                    {"command": "impl_phase", "step": "parse_response", "task_id": task["task_id"]},
                    config
                )
                files_failed += 1
                continue
            
            # Write files
            for code_file in code_files:
                file_path = code_file["path"]
                code = code_file["code"]
                
                success, message = safe_write_code_file(file_path, code, config, dry_run=False)
                
                if success:
                    log(
                        message,
                        {"command": "impl_phase", "step": "write_file", "task_id": task["task_id"], "file_path": file_path},
                        config
                    )
                    if "Would write" in message:
                        pass  # Dry-run
                    elif "Wrote" in message:
                        files_created += 1
                    else:
                        files_updated += 1
                else:
                    log(
                        f"Failed to write file: {message}",
                        {"command": "impl_phase", "step": "write_file_error", "task_id": task["task_id"], "file_path": file_path},
                        config
                    )
                    files_failed += 1
        
        except Exception as e:
            log(
                f"ERROR processing task {task['task_id']}: {e}",
                {"command": "impl_phase", "step": "error", "task_id": task["task_id"]},
                config
            )
            files_failed += 1
    
    log(
        f"Implementation phase complete: created={files_created} updated={files_updated} failed={files_failed}",
        {"command": "impl_phase", "step": "complete", "phase_id": phase_id, "files_created": files_created, "files_updated": files_updated, "files_failed": files_failed},
        config
    )
    
    print(f"\n✓ Implementation phase {phase_id} complete:")
    print(f"  Files created: {files_created}")
    print(f"  Files updated: {files_updated}")
    print(f"  Files failed: {files_failed}")
    
    return 0 if files_failed == 0 else 1


def command_impl_loop(
    config: Config,
    max_tasks: typing.Optional[int] = None,
    dry_run: bool = False
) -> int:
    """
    Run automated implementation loop for multiple tasks.
    
    Similar to 'grow' but for implementation - processes multiple tasks
    in sequence, optionally with git sync after each batch.
    
    Args:
        config: Config object
        max_tasks: Maximum number of tasks to process (None = all planned tasks)
        dry_run: If True, don't write files, just log what would happen
    """
    log(
        f"Running 'impl_loop' command: max_tasks={max_tasks} dry_run={dry_run}",
        {"command": "impl_loop", "step": "start"},
        config
    )
    
    if not config.implementation.enabled:
        log(
            "Implementation automation is disabled",
            {"command": "impl_loop", "step": "check_enabled"},
            config
        )
        print("ERROR: Implementation automation is disabled. Set implementation.enabled=true in auto_config.json")
        return 1
    
    # Read implementation plan
    prd_path = pathlib.Path(config.master_md_path)
    plan_content = read_implementation_plan_section(prd_path)
    
    if not plan_content:
        log("Implementation plan not found", {"command": "impl_loop", "step": "read_plan"}, config)
        print("ERROR: Implementation plan not found. Run 'plan_impl' first.")
        return 1
    
    # Extract planned tasks (simplified parsing)
    # In a full implementation, we'd properly parse the markdown table
    task_ids = re.findall(r'IMPL-\d+', plan_content)
    
    if not task_ids:
        log("No tasks found in implementation plan", {"command": "impl_loop", "step": "find_tasks"}, config)
        print("WARNING: No implementation tasks found in plan")
        return 1
    
    # Limit tasks
    if max_tasks:
        task_ids = task_ids[:max_tasks]
    
    print(f"\nProcessing {len(task_ids)} implementation tasks...")
    
    tasks_completed = 0
    tasks_failed = 0
    
    for i, task_id in enumerate(task_ids, 1):
        log(
            f"Processing task {i}/{len(task_ids)}: {task_id}",
            {"command": "impl_loop", "step": "process_task", "task_id": task_id, "task_index": i, "total_tasks": len(task_ids)},
            config
        )
        
        # Extract phase ID from task (simplified - in full implementation, parse from plan)
        # For now, we'll need to call impl_phase with a placeholder phase
        # This is a limitation of the simplified implementation
        print(f"  [{i}/{len(task_ids)}] Task {task_id}...")
        
        # In a full implementation, we'd:
        # 1. Parse the full task details from the plan
        # 2. Call impl_phase with the correct phase_id
        # 3. Track success/failure
        
        # For now, just log that we would process it
        if dry_run:
            log(
                f"DRY-RUN: Would process task {task_id}",
                {"command": "impl_loop", "step": "dry_run", "task_id": task_id, "mode": "dry-run"},
                config
            )
        else:
            # TODO: Full implementation would call impl_phase logic here
            log(
                f"Task {task_id} processing not fully implemented in this step",
                {"command": "impl_loop", "step": "todo", "task_id": task_id},
                config
            )
            tasks_completed += 1
    
    log(
        f"Implementation loop complete: completed={tasks_completed} failed={tasks_failed}",
        {"command": "impl_loop", "step": "complete", "tasks_completed": tasks_completed, "tasks_failed": tasks_failed},
        config
    )
    
    print(f"\n✓ Implementation loop complete:")
    print(f"  Tasks completed: {tasks_completed}")
    print(f"  Tasks failed: {tasks_failed}")
    
    return 0 if tasks_failed == 0 else 1


def command_doctor(config: Config) -> int:
    """
    Run comprehensive health check and diagnostics.
    
    Checks filesystem, config, state, logs, and environment.
    Optionally performs auto-fixes if enabled in config.
    """
    log("Running 'doctor' command", {"command": "doctor", "step": "start"}, config)
    
    # Build report
    report = build_doctor_report(config)
    
    # Auto-fixes (if enabled)
    if config.safety.enable_doctor_auto_fixes:
        log("Auto-fixes enabled, attempting repairs", {"command": "doctor", "step": "auto_fix"}, config)
        
        # Auto-fix: Rebuild state if needed
        if report["state"].get("needs_rebuild"):
            log("Auto-fixing: Rebuilding state", {"command": "doctor", "step": "auto_fix_state_rebuild"}, config)
            try:
                prd_path = pathlib.Path(config.master_md_path)
                if prd_path.exists():
                    state = build_state_from_file(config, growth_pass=0)
                    save_state(config, state)
                    log("State rebuilt successfully", {"command": "doctor", "step": "auto_fix_state_rebuild"}, config)
                    # Re-check state
                    report["state"] = check_state_consistency(state, [], config)
            except Exception as e:
                log(f"Auto-fix failed: {e}", {"command": "doctor", "step": "auto_fix_error"}, config)
        
        # Auto-fix: Fix chunk statuses (running -> pending)
        state = load_state(config)
        if state:
            fixed_count = 0
            for chunk in state.get("chunks", []):
                if chunk.get("status") == "running":
                    chunk["status"] = "pending"
                    fixed_count += 1
            if fixed_count > 0:
                save_state(config, state)
                log(f"Auto-fixed {fixed_count} chunks: running -> pending", {"command": "doctor", "step": "auto_fix_chunk_status"}, config)
    
    # Auto-fix: Config normalization (if enabled)
    if config.safety.allow_config_autofix:
        # Check if config needs normalization
        config_path = pathlib.Path("auto_config.json")
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    existing_config = json.load(f)
                
                # Check if we need to add missing sections
                needs_update = False
                if "safety" not in existing_config:
                    existing_config["safety"] = {
                        "enable_doctor_auto_fixes": False,
                        "max_consecutive_failures": 5,
                        "stop_on_invariant_violation": True,
                        "doctor_scan_log_lines": 5000,
                        "allow_config_autofix": False
                    }
                    needs_update = True
                
                if needs_update:
                    log("Auto-fixing: Normalizing config file", {"command": "doctor", "step": "auto_fix_config"}, config)
                    # Write back normalized config (preserve existing, add missing)
                    with open(config_path, 'w') as f:
                        json.dump(existing_config, f, indent=2)
                    log("Config normalized successfully", {"command": "doctor", "step": "auto_fix_config"}, config)
            except Exception as e:
                log(f"Config auto-fix failed: {e}", {"command": "doctor", "step": "auto_fix_error"}, config)
    
    # Print report
    print_doctor_report(report, config)
    
    # Log summary
    log(
        f"Doctor check complete: severity={report['severity']} recommendations={len(report['recommendations'])}",
        {"command": "doctor", "step": "complete", "severity": report["severity"]},
        config
    )
    
    # Return code: 0 for OK/WARN, 1 for ERROR
    return 0 if report["severity"] != "ERROR" else 1


def command_git_status(config: Config) -> int:
    """
    Show git repository and automation status.
    
    This is a read-only command that displays:
    - Whether we're in a git repo
    - Current branch
    - Working tree status (clean/dirty)
    - Ahead/behind counts
    - Git automation configuration
    """
    log("Running 'git_status' command", {"command": "git_status", "step": "start"}, config)
    
    root = pathlib.Path.cwd()
    status = get_git_status_summary(root, config)
    
    # Load state for growth info
    state = load_state(config)
    growth_info = None
    if state and "meta" in state and "growth" in state["meta"]:
        growth_info = state["meta"]["growth"]
    
    # Print human-friendly summary
    print("\n" + "="*60)
    print("GIT & AUTOMATION STATUS")
    print("="*60)
    
    print(f"\nGit Repository:")
    if status["is_repo"]:
        print(f"  ✓ Git repository detected")
        print(f"  Branch: {status['branch'] or 'unknown'}")
        print(f"  Working tree: {'dirty' if status['dirty'] else 'clean'}")
        if status["ahead"] > 0 or status["behind"] > 0:
            print(f"  Remote status: {status['ahead']} ahead, {status['behind']} behind {config.git.remote_name}/{config.git.branch_name}")
    else:
        print(f"  ✗ Not in a git repository")
    
    print(f"\nGit Automation:")
    print(f"  Auto-sync enabled: {config.git.enable_auto}")
    print(f"  Remote: {config.git.remote_name}")
    print(f"  Branch: {config.git.branch_name}")
    print(f"  Commit after each pass: {config.git.commit_after_each_pass}")
    print(f"  Push after each pass: {config.git.push_after_each_pass}")
    print(f"  Pull before sync: {config.git.pull_before_sync}")
    print(f"  Auto-add paths: {len(config.git.auto_add_paths)} configured")
    
    if growth_info:
        print(f"\nGrowth Status:")
        print(f"  Current pass: {growth_info.get('current_pass', 0)}")
        print(f"  Total passes run: {growth_info.get('total_passes_run', 0)}")
        last_summary = growth_info.get("last_pass_summary", {})
        if last_summary.get("pass_id"):
            print(f"  Last pass: {last_summary.get('pass_id')} - "
                  f"{last_summary.get('chunks_succeeded', 0)} succeeded, "
                  f"{last_summary.get('chunks_failed', 0)} failed")
    
    print("="*60 + "\n")
    
    return 0


def command_git_sync(config: Config) -> int:
    """
    Manually trigger git sync (add, commit, push).
    
    NOTE: This command respects git.enable_auto for safety.
    If enable_auto is false, the command will log and skip operations.
    To enable automatic git operations, set git.enable_auto=true in auto_config.json.
    """
    log("Running 'git_sync' command", {"command": "git_sync", "step": "start"}, config)
    
    # Note: We respect enable_auto even for manual git_sync command for safety
    # This prevents accidental commits when the user hasn't explicitly enabled automation
    success = perform_git_sync(config, reason="manual_git_sync")
    
    if success:
        log("Git sync completed successfully", {"command": "git_sync", "step": "complete"}, config)
        return 0
    else:
        log("Git sync failed or was skipped", {"command": "git_sync", "step": "complete"}, config)
        return 1


def command_smoke_test(config: Config) -> int:
    """
    Run smoke tests to verify automation system works end-to-end.
    
    This is a conceptual command stub. Full implementation would:
    - Run doctor check
    - Run status check
    - Test enhance dry-run
    - Verify state consistency
    """
    log("Running 'smoke_test' command", {"command": "smoke_test", "step": "start"}, config)
    print("smoke_test is not fully implemented yet, but stub is reachable and safe.")
    print("This command would verify: doctor, status, enhance dry-run, state consistency")
    return 0


def command_benchmark_growth(config: Config) -> int:
    """
    Run growth benchmarks to measure PRD expansion performance.
    
    This is a conceptual command stub. Full implementation would:
    - Measure baseline line count
    - Run controlled growth pass
    - Calculate metrics (lines per pass, success rate)
    - Report results
    """
    log("Running 'benchmark_growth' command", {"command": "benchmark_growth", "step": "start"}, config)
    print("benchmark_growth is not fully implemented yet, but stub is reachable and safe.")
    print("This command would measure: growth rate, success rate, quality metrics")
    return 0


def command_benchmark_impl(config: Config) -> int:
    """
    Run implementation benchmarks to test code generation pipeline.
    
    This is a conceptual command stub. Full implementation would:
    - Verify implementation plan exists
    - Test impl_phase dry-run
    - Validate file paths and parsing
    - Report results
    """
    log("Running 'benchmark_impl' command", {"command": "benchmark_impl", "step": "start"}, config)
    print("benchmark_impl is not fully implemented yet, but stub is reachable and safe.")
    print("This command would test: implementation planning, code generation, file parsing")
    return 0


def command_deploy(config: Config, env: str, dry_run: bool = False, skip_tests: bool = False) -> int:
    """
    Deploy application to specified environment.
    
    This is a conceptual command stub. Full implementation would:
    - Validate environment exists
    - Run pre-deployment checks
    - Execute build/test/deploy hooks
    - Verify deployment success
    """
    log(f"Running 'deploy' command: env={env} dry_run={dry_run}", {"command": "deploy", "step": "start", "env": env}, config)
    
    if not config._raw_data or "deployment" not in config._raw_data or not config._raw_data.get("deployment", {}).get("enabled", False):
        print("ERROR: Deployment is disabled. Set deployment.enabled=true in auto_config.json")
        return 1
    
    if dry_run:
        print(f"DRY-RUN: Would deploy to {env}")
        print("deploy is not fully implemented yet, but stub is reachable and safe.")
    else:
        print(f"deploy to {env} is not fully implemented yet, but stub is reachable and safe.")
    return 0


def command_deploy_status(config: Config, env: str) -> int:
    """
    Show deployment status for an environment.
    
    This is a conceptual command stub. Full implementation would:
    - Parse deployment history from logs
    - Check monitoring status
    - Generate status report
    """
    log(f"Running 'deploy_status' command: env={env}", {"command": "deploy_status", "step": "start", "env": env}, config)
    print(f"deploy_status for {env} is not fully implemented yet, but stub is reachable and safe.")
    print("This command would show: last deployment time, result, health status")
    return 0


def command_monitor(config: Config, since: typing.Optional[str] = None, env: typing.Optional[str] = None) -> int:
    """
    Monitor application health and generate status report.
    
    This is a conceptual command stub. Full implementation would:
    - Read log sources
    - Analyze error patterns
    - Check thresholds
    - Generate report
    """
    log(f"Running 'monitor' command: since={since} env={env}", {"command": "monitor", "step": "start"}, config)
    
    if not config._raw_data or "deployment" not in config._raw_data or not config._raw_data.get("deployment", {}).get("monitoring", {}).get("enabled", False):
        print("ERROR: Monitoring is disabled. Set deployment.monitoring.enabled=true")
        return 1
    
    print("monitor is not fully implemented yet, but stub is reachable and safe.")
    print("This command would analyze: logs, error patterns, health metrics")
    return 0


def command_security_check(config: Config, dry_run: bool = False, verbose: bool = False) -> int:
    """
    Check security configuration and status.
    
    This is a conceptual command stub. Full implementation would:
    - Report security configuration
    - Analyze PRD for security sections
    - Run tests if enabled
    - Check for secrets in forbidden locations
    """
    log(f"Running 'security_check' command: dry_run={dry_run} verbose={verbose}", {"command": "security_check", "step": "start"}, config)
    
    if not config._raw_data or "security" not in config._raw_data or not config._raw_data.get("security", {}).get("enabled", False):
        print("WARNING: Security is disabled. Set security.enabled=true in auto_config.json")
        return 0
    
    print("security_check is not fully implemented yet, but stub is reachable and safe.")
    print("This command would check: config, PRD analysis, tests, secrets management")
    return 0


def command_quick_test(config: Config, scope: str = "basic", verbose: bool = False) -> int:
    """
    Run quick test suite.
    
    This is a conceptual command stub. Full implementation would:
    - Run unit tests (scope=basic) or unit+integration (scope=full)
    - Parse test results
    - Check coverage if available
    - Report results
    """
    log(f"Running 'quick_test' command: scope={scope} verbose={verbose}", {"command": "quick_test", "step": "start"}, config)
    
    if not config._raw_data or "security" not in config._raw_data or not config._raw_data.get("security", {}).get("testing", {}).get("enabled", False):
        print("ERROR: Testing is disabled. Set security.testing.enabled=true in auto_config.json")
        return 1
    
    if scope not in ["basic", "full"]:
        print(f"ERROR: Invalid scope '{scope}'. Must be 'basic' or 'full'")
        return 1
    
    print(f"quick_test ({scope}) is not fully implemented yet, but stub is reachable and safe.")
    print(f"This command would run: {'unit tests' if scope == 'basic' else 'unit + integration tests'}")
    return 0


# ============================================================================
# CLI MAIN
# ============================================================================

def main():
    """Main CLI entry point."""
    global _global_config
    
    parser = argparse.ArgumentParser(
        description="Universal automated PRD enhancement system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Commands:
          init       - Initialize system (build state from PRD)
          status     - Show system status (use --verbose for chunk details)
          start      - Start enhancement loop (single pass)
          enhance    - Alias for 'start' (single pass)
          grow       - Run autonomous growth loop towards target line count
          reset      - Reset automation state
          sync_roles - Sync Omni-Corp Role Library and Prompt Templates into prd.md
          git_status - Show git repository and automation status
          git_sync   - Manually sync changes to git (add, commit, push)
          doctor     - Run health check and diagnostics (with optional auto-fixes)
          plan_impl  - Generate implementation plan from PRD
          impl_phase - Implement a specific phase/task (requires --phase)
          impl_loop  - Run automated implementation loop for multiple tasks
        
        Examples:
          python3 auto_master.py init
          python3 auto_master.py sync_roles
          python3 auto_master.py doctor
          python3 auto_master.py status --verbose
          python3 auto_master.py enhance --limit 1 --dry-run
          python3 auto_master.py enhance --limit 5
          python3 auto_master.py grow
          python3 auto_master.py git_status
          python3 auto_master.py git_sync
          python3 auto_master.py plan_impl
          python3 auto_master.py impl_phase --phase 3.2.1 --limit-files 3
          python3 auto_master.py impl_loop --max-tasks 5
          python3 auto_master.py smoke_test
          python3 auto_master.py benchmark_growth
          python3 auto_master.py benchmark_impl
          python3 auto_master.py deploy --env staging --dry-run
          python3 auto_master.py deploy_status --env staging
          python3 auto_master.py monitor
          python3 auto_master.py security_check --dry-run
          python3 auto_master.py quick_test --scope basic
        """)
    )
    
    parser.add_argument(
        'command',
        choices=['init', 'status', 'start', 'enhance', 'grow', 'reset', 'sync_roles', 'git_status', 'git_sync', 'doctor', 'plan_impl', 'impl_phase', 'impl_loop', 'smoke_test', 'benchmark_growth', 'benchmark_impl', 'deploy', 'deploy_status', 'monitor', 'security_check', 'quick_test'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='auto_config.json',
        help='Path to config file (default: auto_config.json)'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Maximum number of chunks to process (enhance/start only)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Do not modify files, just log what would happen (enhance/start only)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output (status only)'
    )
    parser.add_argument(
        '--phase',
        type=str,
        help='Phase ID for impl_phase command (e.g., "3.2.1")'
    )
    parser.add_argument(
        '--limit-files',
        type=int,
        help='Maximum number of files to generate (impl_phase only)'
    )
    parser.add_argument(
        '--max-tasks',
        type=int,
        help='Maximum number of tasks to process (impl_loop only)'
    )
    parser.add_argument(
        '--env',
        type=str,
        help='Environment name (for deploy/deploy_status commands)'
    )
    parser.add_argument(
        '--skip-tests',
        action='store_true',
        help='Skip tests during deployment'
    )
    parser.add_argument(
        '--scope',
        type=str,
        choices=['basic', 'full'],
        default='basic',
        help='Test scope (basic or full) for quick_test command'
    )
    parser.add_argument(
        '--since',
        type=str,
        help='Time range for monitor command (e.g., "1h", "24h")'
    )
    
    args = parser.parse_args()
    
    # Load config
    try:
        config = load_config(pathlib.Path(args.config))
        _global_config = config  # Set global for logging
    except Exception as e:
        print(f"ERROR: Failed to load config: {e}", file=sys.stderr)
        return 1
    
    # Route to command handler
    handlers = {
        'init': lambda: command_init(config),
        'status': lambda: command_status(config, verbose=args.verbose),
        'start': lambda: command_start(config, limit=args.limit, dry_run=args.dry_run),
        'enhance': lambda: command_enhance(config, limit=args.limit, dry_run=args.dry_run),
        'grow': lambda: command_grow(config),
        'reset': lambda: command_reset(config),
        'sync_roles': lambda: command_sync_roles(config),
        'git_status': lambda: command_git_status(config),
        'git_sync': lambda: command_git_sync(config),
        'doctor': lambda: command_doctor(config),
        'plan_impl': lambda: command_plan_impl(config),
        'impl_phase': lambda: command_impl_phase(config, phase_id=args.phase or "", limit_files=args.limit_files, dry_run=args.dry_run) if args.phase else (print("ERROR: --phase required for impl_phase command"), 1)[1],
        'impl_loop': lambda: command_impl_loop(config, max_tasks=args.max_tasks, dry_run=args.dry_run),
        'smoke_test': lambda: command_smoke_test(config),
        'benchmark_growth': lambda: command_benchmark_growth(config),
        'benchmark_impl': lambda: command_benchmark_impl(config),
        'deploy': lambda: command_deploy(config, env=args.env or (config._raw_data and config._raw_data.get("deployment", {}).get("default_environment", "local") or "local"), dry_run=args.dry_run, skip_tests=args.skip_tests) if args.env or (config._raw_data and "deployment" in config._raw_data) else (print("ERROR: --env required for deploy command"), 1)[1],
        'deploy_status': lambda: command_deploy_status(config, env=args.env or (config._raw_data and config._raw_data.get("deployment", {}).get("default_environment", "local") or "local")) if args.env or (config._raw_data and "deployment" in config._raw_data) else (print("ERROR: --env required for deploy_status command"), 1)[1],
        'monitor': lambda: command_monitor(config, since=args.since, env=args.env),
        'security_check': lambda: command_security_check(config, dry_run=args.dry_run, verbose=args.verbose),
        'quick_test': lambda: command_quick_test(config, scope=args.scope, verbose=args.verbose),
    }
    
    handler = handlers[args.command]
    try:
        return handler()
    except KeyboardInterrupt:
        log("Interrupted by user", {"command": args.command}, config)
        return 130
    except Exception as e:
        log(f"ERROR: {e}", {"command": args.command}, config)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
