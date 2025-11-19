# Sample Productivity Companion – Product Requirements Document

> This is a demonstrative “single-source-of-truth” PRD that merges product requirements, prompt definitions, and automation guidance. Replace placeholder content with your project’s specifics, but keep the numbering to preserve compatibility with automation workflows.

---

## 0. Metadata & Index

- **Project Name:** FocusFlow – Productivity Companion  
- **Version:** v0.4 draft  
- **Last Updated:** 2025-11-19  
- **Owner:** Product Systems Team  
- **Related Repos / Services:** web-app, automation-kit  
- **Prompt Library Index:**  
  - `global_app_brain_v1` – core reasoning engine  
  - `support_chat_onboarding_v1` – onboarding assistant  
  - `feature_planner_session_v1` – focus session planner  

---

## 1. Project Overview

### 1.1 Vision
Help independent knowledge workers convert goals into achievable focus sessions while capturing insights that compound over time.

### 1.2 Problem Statement
Most lightweight productivity tools either overwhelm users with tasks or fail to close the reflection loop. Users need a calm companion that guides planning, execution, and retrospection without heavy setup.

### 1.3 Goals and Non-Goals
- **Goals:**  
  1. Turn vague goals into concrete sessions.  
  2. Capture blockers to improve future plans.  
  3. Provide gentle habit nudges tied to focus cadence.
- **Non-Goals:**  
  - Real-time team collaboration (tracked as `[OPEN_QUESTION] team_collab_future`).  
  - Deep analytics dashboards.  
  - Offline parity in MVP.

### 1.4 Target Users & Personas
1. **Focused Freelancer** – manages multiple client deliverables.  
2. **Graduate Researcher** – balances reading, experiments, and writing.  
3. **Productive Parent** – slots deep work between family commitments.

---

## 2. Product Scope

### 2.1 In-Scope
- Daily planning canvas with quick presets.  
- Session timer with mid-session reflection hooks.  
- Lightweight habit nudges between sessions.

### 2.2 Out-of-Scope
- Calendar syncing, calendar-based auto scheduling.  
- Team workspaces or shared boards.

### 2.3 Constraints & Assumptions
- Works best in modern browsers and mobile web views.  
- `[ASSUMPTION]` We can store anonymized telemetry for insights.  
- MVP will run only in English.

---

## 3. Core Use Cases

### 3.1 Use Case A – Daily Planning
- **User Story:** “As a freelancer, I want to plan my day in focused blocks so I can track commitments.”  
- **Scenario:** Morning plan → select up to three goals → define success criteria per session.  
- **Success Criteria:** Plan submitted, sessions scheduled, nudges enabled.

### 3.2 Use Case B – Focus Execution
- **User Story:** “As a graduate researcher, I want mid-session prompts to capture blockers.”  
- **Scenario:** Start timer, note blockers, log completion.  
- **Success Criteria:** Session logged with blocker list and energy score.

### 3.3 Use Case C – Reflection & Insights
- **Story:** “As a productive parent, I want EOD reflections to adjust tomorrow’s plan.”  
- **Success Criteria:** Reflection saved, next-day suggestions queued.

---

## 4. Features

### 4.1 Feature Group A – Planning Canvas

#### 4.1.1 Feature A1 – Session Planner
- **Business Rationale:** Planning commitment improves completion rates by 35%.  
- **User Stories:**  
  - “As a user, I can create up to three focus sessions with goals.”  
  - “As a user, I can tag sessions with energy levels.”
- **Functional Requirements:**  
  1. Create/edit/delete sessions.  
  2. Validate overlapping schedules.  
  3. Save to local storage and cloud profile.
- **Non-functional Requirements:**  
  - Load in < 1.5s on mobile 4G.  
  - Auto-save drafts every 5 seconds.
- **Edge Cases:**  
  - User adds zero sessions (prompt to add at least one).  
  - Overlapping sessions – show conflict banner.
- **Analytics / Events:**  
  - `session_planned` (session_count, duration_sum).  
  - `session_conflict_shown`.
- **Related Prompts:** [`feature_planner_session_v1`]

#### 4.1.2 Feature A2 – Habit Nudges
- **Rationale:** Encourage micro-habits that support focus longevity.  
- **Requirements:** Provide default nudges (hydrate, stretch) and allow custom short text.  
- **Analytics:** `nudge_completed`.
- **Related Prompts:** `[ASSUMPTION]` `nudge_microcopy_v1`.

### 4.2 Feature Group B – Focus & Reflection
- Add timer controls, mid-session blocker capture, EOD reflection summaries.  
- `[OPEN_QUESTION]` Should EOD reflection include mood tracking?

---

## 5. UX & Flows

### 5.1 Screens and States
1. Planning dashboard  
2. Active session view (with mid-session prompts)  
3. Reflection summary page

### 5.2 Navigation & IA
Bottom navigation: Plan | Focus | Reflect | Insights.

### 5.3 Example Flow
Plan → Start Session → Mid-session prompt → Complete → Reflect → View suggestion for tomorrow.

---

## 6. Technical Architecture

### 6.1 High-Level Architecture
- React/TypeScript frontend, serverless backend (Supabase or similar), automation scripts for PRD upkeep.

### 6.2 Backend / APIs
- REST endpoints for sessions, reflections, nudges.  
- `[ASSUMPTION]` Webhooks for future integrations.

### 6.3 Data Model & Storage
- Tables: `sessions`, `reflections`, `nudges`, `prompts`.

### 6.4 Integrations
- Future: Google Calendar read-only import `[DEPRECATED] old-calendar-sync-approach`.

### 6.5 Performance & Reliability
- 99.5% uptime target, graceful degradation if automation system offline.

---

## 7. AI & Behaviour

### 7.1 Role of AI
- Suggest session durations, generate reflection prompts, craft habit encouragement copy.

### 7.2 Safety, Ethics, Guardrails
- Avoid medical/clinical advice.  
- Offer help resources if user expresses distress.

### 7.3 Personalization / Adaptation Logic
- Use previous session performance to adjust future suggestions.  
- `[ASSUMPTION]` Use embedding similarity for blocker suggestions.

---

## 8. Analytics & Experiments

### 8.1 KPIs
- Daily Active Planners, Completed Sessions per DAU, Reflection Completion Rate.

### 8.2 Event Schema
- `session_planned`, `session_started`, `session_completed`, `reflection_logged`.

### 8.3 Experiment Ideas
- Test nudges vs no nudges for retention.  
- Experiment with AI-generated encouragement copy.

---

## 9. Prompt Library

### 9.1 Global System Prompts

#### PROMPT: Global App Brain
- **ID:** `global_app_brain_v1`  
- **Scope:** Overall reasoning for FocusFlow  
- **Type:** system

```prompt
You are the core reasoning engine of FocusFlow. Keep users calm, focused, and supported. Never claim medical expertise. When unsure, ask clarifying questions and log blockers for later insights.
```

#### PROMPT: Onboarding Support Chat
- **ID:** `support_chat_onboarding_v1`  
- **Scope:** First-time chat onboarding  
- **Type:** system

```prompt
You are a warm, concise onboarding assistant for FocusFlow. Welcome the user, explain the planning canvas, and invite them to create their first focus session.
```

### 9.2 Feature-Specific Prompts

#### PROMPT: Planner Session Helper
- **ID:** `feature_planner_session_v1`  
- **Scope:** Session planner suggestions  
- **Type:** system + few-shot

```prompt
You help users break large goals into at most three focus sessions. Suggest realistic durations, ask for blockers, and remind them to note success criteria.
```

#### PROMPT: Reflection Insight Generator
- **ID:** `feature_reflection_insights_v1`  
- **Scope:** Post-session reflection summary  
- **Type:** tool

```prompt
Summarize the reflection in three bullet points: what worked, blocker pattern, suggested tweak. Recommend one habit nudge for the next day.
```

---

## 10. Automation Hints (for `prd_auto.py`)

1. This file is intentionally long and chunked via Markdown headings.  
2. Preserve `[ASSUMPTION]`, `[OPEN_QUESTION]`, `[DEPRECATED]`, and `PROMPT` blocks verbatim.  
3. Section 9 contains the authoritative prompt library; automation outputs may propose new “PROMPT CANDIDATE” blocks that must later migrate here.  
4. When adding new features, always update Sections 4 and 9 in tandem.  
5. Chunk size guidance: Sections 4 and 9 are expected to grow fastest.

---

## 11. Risks, Open Questions, Future Work

- `[OPEN_QUESTION] team_collab_future` – Should FocusFlow support shared team boards in v2?  
- `[OPEN_QUESTION] reflection_mood_tracking` – Do we capture mood/energy in reflections?  
- `[ASSUMPTION] telemetry_usage` – Telemetry consent covers anonymized analytics events.  
- Future Work:  
  - Introduce AI-generated daily recap emails.  
  - Build script to auto-ingest `PROMPT CANDIDATE` entries into Section 9.

