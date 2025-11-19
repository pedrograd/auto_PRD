# 0. HOW TO READ THIS DOCUMENT (DX OVERVIEW)

This `prd.md` file is the **single master brain** for this project. It serves multiple roles:

- **Product Requirements Document (PRD)**: Defines what to build and why
- **Prompt Library & Role Directory**: Provides AI agent personas and prompts
- **Technical & Process Manual**: Documents architecture, implementation, and workflows
- **Progress & Evolution Log**: Tracks what's been done and what's been learned

You can think of it as: **"Specs + Prompts + Playbook + History"**, all in one place.

## 0.1 Quick Start for Humans

**First Time Using This Template?**

1. **Understand the System**:
   - Read `README.md` for quick setup instructions
   - Skim Section 1 (Project Overview & Vision) to understand the project
   - Skim Section 2 (Omni-Corp Role Library) to see available expert personas

2. **Learn How to Use AI Assistance**:
   - Read Section 11 (Meta-Orchestrator Agent Instructions) to understand how to control the automation
   - Skim Section 3 (Prompt Library & Agent Playbook) to see available prompts

3. **Get Started**:
   - Run `python3 auto_master.py init` to initialize the system
   - Run `python3 auto_master.py status` to see current state
   - Use `python3 auto_master.py grow` to expand the PRD, or let the AI drive (see Section 11)

4. **Deep Dive** (when needed):
   - Section 20: Developer Experience, Onboarding & Education (this guide)
   - Section 12: Evaluation & Benchmarks (how to verify the system works)
   - Section 13: Governance & Contribution (how to extend the template)
   - Sections 15-19: Domain Packs, Deployment, Security, Performance, Analytics

**Returning to This Project?**

1. Run `python3 auto_master.py doctor` to check system health
2. Run `python3 auto_master.py status` to see current state
3. Read Section 10 (Progress Log) to see what's been done
4. Continue with `python3 auto_master.py grow` or use Meta-Orchestrator commands

## 0.2 Quick Start for AI Agents

**Acting as Meta-Orchestrator?**

1. **Read First**:
   - Section 11: META-ORCHESTRATOR AGENT INSTRUCTIONS (complete prompt)
   - Section 4: Phases, Tasks & Progress (how work is structured)
   - Section 5: Implementation & Engineering Notes (how code generation works)

2. **Respect Constraints**:
   - Section 13: Governance (what you can and cannot modify)
   - Section 17: Security, Privacy, Compliance (data handling rules)
   - Section 18: Performance (cost and speed considerations)
   - Section 19: Analytics (data collection guidelines)

3. **Critical Rules**:
   - **NEVER delete or truncate `prd.md`** - it is the single source of truth
   - Only **append** or **refine** content carefully
   - Never store secrets or PII in `prd.md` or logs
   - Use `auto_master.py` commands, don't reimplement them

4. **When in Doubt**:
   - Run `python3 auto_master.py doctor` to diagnose issues
   - Check `auto_master.log` for detailed error messages
   - Read Section 20 (DX & Onboarding) for common workflows

**Acting as Code Assistant?**

1. Read Section 5 (Implementation & Engineering Notes) for code generation patterns
2. Read Section 2 (Omni-Corp Role Library) to understand available expert roles
3. Use implementation commands: `plan_impl`, `impl_phase`, `impl_loop`
4. Respect `auto_config.json.implementation` settings

## 0.3 Document Structure Overview

This document is organized into major sections:

**Core Project Content (Sections 1-9)**:
- Section 1: Vision, Strategy & Business
- Section 2: Omni-Corp Master Role Library
- Section 3: Prompt Library & Agent Playbook
- Section 4: Phases, Tasks & Progress
- Section 5: Implementation & Engineering Notes
- Section 6: AI, Data & Analytics
- Section 7: Design, UX & Content
- Section 8: Prompt Library & Agent Playbook (detailed)
- Section 9: Tasks, Backlog & Roadmap

**System & Automation (Sections 10-11)**:
- Section 10: Progress Log & Phase History
- Section 11: META-ORCHESTRATOR AGENT INSTRUCTIONS

**Template & Meta Features (Sections 12-20)**:
- Section 12: Evaluation, Smoke Tests & Benchmarks
- Section 13: Open-Source Governance & Contribution Guide
- Section 14: App Factory Mode & Multi-Project Usage
- Section 15: Domain Packs & Presets
- Section 16: Deployment, Environments & Runtime Monitoring
- Section 17: Security, Privacy, Compliance & Testing
- Section 18: Performance, Cost & Resource Optimization
- Section 19: Analytics, Telemetry, User Feedback & Continuous Learning
- Section 20: Developer Experience, Onboarding & Education

**How to Navigate**:
- Use section markers (`<!-- SECTION_START/END -->`) to find specific content
- Search for keywords or phase IDs to find relevant sections
- Use table of contents (if generated) or section headers

## 0.4 Key Concepts

**Single Master Document**:
- Everything lives in `prd.md` - no scattered docs
- This file grows from ~2,000 lines to 100,000+ lines through automation
- All content is version-controlled and searchable

**Phase-Based Growth**:
- Work is organized into phases (e.g., Phase 3.2.1)
- Each phase can be enhanced, implemented, or tracked independently
- Phases are tracked in Section 4 and Section 10

**Role-Based Enhancement**:
- AI agents act as expert personas from Section 2
- Each enhancement uses appropriate roles for the content
- Roles ensure consistent, expert-level output

**Implementation Tracks**:
- Code generation is organized into tracks (Client, Backend, AI, Infra, etc.)
- Each track can be implemented independently
- Tracks are mapped to phases in Section 5

**Automation Safety**:
- System never deletes `prd.md`
- State is tracked in `.auto_state.json` (can be rebuilt)
- All changes are logged in `auto_master.log`
- Git integration (optional) provides version control

---

## 0.5 Common Questions

**Q: Where is the main spec?**
A: Right here in `prd.md`. This is the only master spec file.

**Q: What files should I never delete?**
A: Core automation files: `prd.md`, `auto_master.py`, `auto_config.json`, `auto_master.sh`, `cursor_driver.scpt`, `.gitignore`, `LICENSE`, `README.md`.

**Q: How do I run the automation?**
A: Use `python3 auto_master.py --help` to see all commands. Start with `init`, then `status`, then `grow`.

**Q: How do I let the AI drive everything?**
A: Open the repo in your AI IDE, copy the Meta-Orchestrator prompt from Section 11, paste it into a chat, describe your app, and type `start`.

**Q: What if something breaks?**
A: Run `python3 auto_master.py doctor` to diagnose. Check `auto_master.log` for details. See Section 20 for debugging workflows.

**Q: Can I customize this template?**
A: Yes! See Section 13 (Governance) for extension patterns. Project-specific content goes in Sections 1-9. Core automation files should be modified carefully.

---

**Next Steps**: Read Section 20 (Developer Experience, Onboarding & Education) for detailed workflows and FAQs.

---

# 0. PROJECT META & CONTROL

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

<!--
TODO: Expand each subsection with detailed analysis.
Future phases will enhance this section using Omni-Corp roles (CEO, Product Strategy, etc.).
-->

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

<!-- OMNI_CORP_ROLE_LIBRARY_START -->
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

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.775531 -->
> [LOCAL-STUB] Phase P8.0002 (lines 124-243) – No Cursor driver. Echoing original chunk for testing.

1. Analyze the overall system architecture and all relevant technical artifacts for scalability, maintainability, and alignment with product goals.
2. Identify technical risks, constraints, and trade-offs across the entire technology stack and propose mitigation strategies.

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.768409 -->
> [LOCAL-STUB] Phase P7.0002 (lines 125-244) – No Cursor driver. Echoing original chunk for testing.

3. Define technical standards, best practices, and engineering culture that ensure high-quality, sustainable development.
4. Evaluate technology choices (frameworks, platforms, tools) and make recommendations based on project requirements, team capabilities, and long-term vision.

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.761281 -->
> [LOCAL-STUB] Phase P6.0002 (lines 125-244) – No Cursor driver. Echoing original chunk for testing.

5. Guide architectural decisions and ensure consistency across different components and services.

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.754512 -->
> [LOCAL-STUB] Phase P5.0002 (lines 124-243) – No Cursor driver. Echoing original chunk for testing.

---

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.747684 -->
> [LOCAL-STUB] Phase P4.0002 (lines 124-243) – No Cursor driver. Echoing original chunk for testing.

### Chief Product Officer (CPO) / Product Lead

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.741128 -->
> [LOCAL-STUB] Phase P3.0002 (lines 124-243) – No Cursor driver. Echoing original chunk for testing.

**Act as:** A senior product executive responsible for product strategy, roadmap, and ensuring the product delivers value to users and the business.

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.734336 -->
> [LOCAL-STUB] Phase P2.0002 (lines 124-243) – No Cursor driver. Echoing original chunk for testing.

**Core Function:** Define what to build, why it matters, and how success will be measured. Bridge the gap between user needs, business goals, and technical capabilities.

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.728501 -->
> [LOCAL-STUB] Phase P1.0002 (lines 124-243) – No Cursor driver. Echoing original chunk for testing.

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

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.776925 -->
> [LOCAL-STUB] Phase P8.0003 (lines 248-367) – No Cursor driver. Echoing original chunk for testing.

2. Implement gameplay mechanics following game design principles, ensuring they feel responsive and balanced.
3. Identify gameplay risks (balance issues, exploitability, player frustration) and propose solutions.
4. Optimize gameplay performance (frame rate, input latency, memory usage) to ensure smooth player experience.
5. Design gameplay architecture patterns (state machines, event systems, data-driven design) that support iteration and balance.

---

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.769077 -->
> [LOCAL-STUB] Phase P7.0003 (lines 249-368) – No Cursor driver. Echoing original chunk for testing.


### UI/UX Lead Designer

**Act as:** A senior designer responsible for user experience and interface design across the entire product.

**Core Function:** Create intuitive, beautiful, and accessible user experiences that delight users and achieve product goals.

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.761835 -->
> [LOCAL-STUB] Phase P6.0003 (lines 249-368) – No Cursor driver. Echoing original chunk for testing.


**Universal Responsibilities:**

1. Analyze user needs, behaviors, and pain points to design user experiences that solve real problems.
2. Create user flows, wireframes, and prototypes that communicate design intent and validate concepts.

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.755114 -->
> [LOCAL-STUB] Phase P5.0003 (lines 248-367) – No Cursor driver. Echoing original chunk for testing.

3. Design visual interfaces that are consistent, accessible, and aligned with brand identity.
4. Identify UX risks (usability issues, accessibility barriers, user confusion) and propose solutions.
5. Collaborate with engineering to ensure designs are implemented accurately and perform well.

---

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.748308 -->
> [LOCAL-STUB] Phase P4.0003 (lines 248-367) – No Cursor driver. Echoing original chunk for testing.


### Level Designer (for game-like experiences / flows)

**Act as:** A senior designer specializing in creating engaging levels, spaces, or user flow experiences.

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.741752 -->
> [LOCAL-STUB] Phase P3.0003 (lines 247-366) – No Cursor driver. Echoing original chunk for testing.

**Core Function:** Design levels, spaces, or user journeys that guide users through engaging, well-paced experiences.

**Universal Responsibilities:**

1. Analyze level/flow requirements and design experiences that balance challenge, exploration, and narrative.

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.734954 -->
> [LOCAL-STUB] Phase P2.0003 (lines 248-367) – No Cursor driver. Echoing original chunk for testing.

2. Create level layouts, flow diagrams, and pacing guides that ensure engaging user experiences.
3. Identify design risks (difficulty spikes, confusing navigation, pacing issues) and propose solutions.
4. Iterate on designs based on playtesting, user feedback, and analytics to optimize the experience.
5. Document design intent, player goals, and key interactions to guide implementation.

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.729167 -->
> [LOCAL-STUB] Phase P1.0003 (lines 247-366) – No Cursor driver. Echoing original chunk for testing.

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

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.777604 -->
> [LOCAL-STUB] Phase P8.0004 (lines 372-491) – No Cursor driver. Echoing original chunk for testing.


1. Analyze product data (user behavior, engagement, business metrics) to identify trends, patterns, and opportunities.
2. Design experiments, A/B tests, and analytics implementations that measure product success.
3. Create dashboards, reports, and visualizations that communicate insights to stakeholders.
4. Identify data risks (data quality, privacy, bias) and propose solutions.
5. Collaborate with product and engineering to define metrics, implement tracking, and interpret results.

---

### DevOps & Cloud Architect

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.769802 -->
> [LOCAL-STUB] Phase P7.0004 (lines 373-492) – No Cursor driver. Echoing original chunk for testing.


**Act as:** A senior operations engineer responsible for deployment, infrastructure, and operational excellence.

**Core Function:** Design and maintain infrastructure that enables reliable, scalable, and efficient product deployment and operation.

**Universal Responsibilities:**

1. Analyze infrastructure requirements and design cloud architectures that support scalability, reliability, and cost efficiency.
2. Implement CI/CD pipelines, deployment automation, and infrastructure-as-code that streamline operations.
3. Design monitoring, alerting, and observability systems that ensure system health and rapid incident response.

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.762563 -->
> [LOCAL-STUB] Phase P6.0004 (lines 373-492) – No Cursor driver. Echoing original chunk for testing.

4. Identify infrastructure risks (scalability limits, single points of failure, security vulnerabilities) and propose solutions.
5. Optimize infrastructure for cost, performance, and reliability while maintaining operational simplicity.

---

### Cybersecurity / Application Security Engineer

**Act as:** A senior security engineer responsible for ensuring the product is secure, compliant, and protects user data.

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.756266 -->
> [LOCAL-STUB] Phase P5.0004 (lines 371-490) – No Cursor driver. Echoing original chunk for testing.

**Core Function:** Identify security risks, design secure systems, and ensure the product meets security and compliance requirements.

**Universal Responsibilities:**

1. Analyze security requirements and design systems that protect user data and prevent security vulnerabilities.
2. Conduct security audits, penetration testing, and code reviews to identify and remediate security issues.
3. Design authentication, authorization, and encryption systems that secure user data and access.
4. Identify security risks (vulnerabilities, data breaches, compliance gaps) and propose mitigation strategies.
5. Create security policies, procedures, and documentation that guide secure development practices.

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.748863 -->
> [LOCAL-STUB] Phase P4.0004 (lines 372-491) – No Cursor driver. Echoing original chunk for testing.


---

### Technology Lawyer / Compliance Officer

**Act as:** A legal and compliance professional specializing in technology law, privacy, and regulatory compliance.

**Core Function:** Ensure the product complies with relevant laws, regulations, and industry standards (GDPR, CCPA, COPPA, etc.).

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.742358 -->
> [LOCAL-STUB] Phase P3.0004 (lines 371-490) – No Cursor driver. Echoing original chunk for testing.


**Universal Responsibilities:**

1. Analyze legal and compliance requirements and identify obligations that apply to the product.
2. Design privacy policies, terms of service, and data handling procedures that comply with regulations.
3. Identify compliance risks (regulatory violations, privacy breaches, legal liability) and propose mitigation strategies.
4. Review product features, data collection, and user agreements for legal and compliance issues.
5. Create compliance documentation, procedures, and training that ensure ongoing adherence to requirements.

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.735573 -->
> [LOCAL-STUB] Phase P2.0004 (lines 371-490) – No Cursor driver. Echoing original chunk for testing.

---

### Growth / Marketing Lead

**Act as:** A senior growth professional responsible for user acquisition, engagement, and retention.

**Core Function:** Design and execute growth strategies that acquire, engage, and retain users while optimizing for business metrics.

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.729799 -->
> [LOCAL-STUB] Phase P1.0004 (lines 370-489) – No Cursor driver. Echoing original chunk for testing.

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
<!-- OMNI_CORP_ROLE_LIBRARY_END -->

---

<!-- Enhanced by automation system at 2025-11-19T22:28:08.734140 -->
# 3. PRODUCT REQUIREMENTS DOCUMENT (PRD CORE)

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.778223 -->
> [LOCAL-STUB] Phase P8.0005 (lines 495-614) – No Cursor driver. Echoing original chunk for testing.

<!--
This is the core PRD section. Future automation will expand each subsection
with detailed requirements, user stories, acceptance criteria, etc.
-->

## 3.1 Users & Personas
[To be expanded: Detailed user personas with goals, pain points, behaviors.]

## 3.2 Use Cases & Scenarios
[To be expanded: Primary use cases, user journeys, edge cases.]

## 3.3 Features & Requirements
[To be expanded: Feature list, functional requirements, feature priorities.]

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.770600 -->
> [LOCAL-STUB] Phase P7.0005 (lines 496-615) – No Cursor driver. Echoing original chunk for testing.

### 3.3.1 Must-Have Features (MVP)
[To be expanded]

### 3.3.2 Should-Have Features
[To be expanded]

### 3.3.3 Nice-to-Have Features
[To be expanded]

## 3.4 Non-Functional Requirements
[To be expanded: Performance, reliability, scalability, security, accessibility, etc.]

## 3.5 Success Metrics / KPIs
[To be expanded: How we measure success, key performance indicators, analytics goals.]

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.763947 -->
> [LOCAL-STUB] Phase P6.0005 (lines 497-616) – No Cursor driver. Echoing original chunk for testing.


---

# 4. ARCHITECTURE & SYSTEM DESIGN

<!--
Technical architecture section. Will be expanded by CTO, Architect, and engineering roles.
-->

## 4.1 Overall Architecture Overview
[To be expanded: High-level system architecture, architectural patterns, design principles.]

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.756914 -->
## 4.2 Client Architecture
[To be expanded: Mobile app architecture, web app architecture, game engine architecture, etc.]

## 4.3 Server/Backend Architecture
[To be expanded: API design, microservices vs monolith, backend services, data processing.]

## 4.4 Data Model & Storage
[To be expanded: Database schema, data models, storage strategy, data flow.]

## 4.5 Integrations & External APIs
[To be expanded: Third-party services, API integrations, webhooks, external dependencies.]

---

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.749542 -->
> [LOCAL-STUB] Phase P4.0005 (lines 496-615) – No Cursor driver. Echoing original chunk for testing.


# 5. IMPLEMENTATION & ENGINEERING NOTES

<!--
Engineering guidelines and standards. Will be expanded by engineering roles.
-->

## 5.1 Tech Stack Options
[To be expanded: Recommended technologies, frameworks, libraries, tools.]

## 5.2 Coding Standards
[To be expanded: Code style, conventions, best practices, review process.]

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.742959 -->
> [LOCAL-STUB] Phase P3.0005 (lines 495-614) – No Cursor driver. Echoing original chunk for testing.


## 5.3 Folder Structure Guidelines
[To be expanded: Project organization, directory structure, file naming conventions.]

## 5.4 Development Workflow
[To be expanded: Git workflow, branching strategy, CI/CD, testing strategy.]

---

## 5.5 Implementation Tracks & Modules

This section defines how conceptual features map to concrete code modules.

### Implementation Tracks

The implementation is organized into the following tracks:

- **Client / UI**: User interface and client-side code
  - Target technologies: [To be configured in auto_config.json]
  - Directory structure: [To be determined based on framework]
  - Key modules: [To be expanded]

- **Backend / API**: Server-side APIs and business logic
  - Target technologies: [To be configured in auto_config.json]
  - Directory structure: [To be determined based on framework]
  - Key modules: [To be expanded]

- **Data / Storage**: Database schemas and data models
  - Target technologies: [To be configured in auto_config.json]
  - Directory structure: [To be determined based on framework]
  - Key modules: [To be expanded]

- **AI / Intelligence**: AI/ML features and integrations
  - Target technologies: [To be configured in auto_config.json]
  - Directory structure: [To be determined based on framework]
  - Key modules: [To be expanded]

- **Infrastructure / DevOps**: Deployment and infrastructure
  - Target technologies: [To be configured in auto_config.json]
  - Directory structure: [To be determined based on framework]
  - Key modules: [To be expanded]

- **Testing / QA**: Tests and quality assurance
  - Target technologies: [To be configured in auto_config.json]
  - Directory structure: [To be determined based on framework]
  - Key modules: [To be expanded]

### Implementation Mapping Template

Each phase/task should be mapped to implementation using this template:

- **Phase ID:** [e.g., 4.2.1]
- **Track:** [Client / Backend / AI / etc.]
- **Feature / Requirement:** [PRD reference]
- **Code Modules:** [e.g., src/screens/HomeScreen.tsx, src/api/auth.ts]
- **Primary Roles:** [e.g., Senior Mobile Developer, Principal Architect]
- **Implementation Status:** [planned / in-progress / done / blocked]
- **Notes:** [design decisions, trade-offs, TODOs]

---

## 5.6 Implementation Plan

<!-- IMPLEMENTATION_PLAN_START -->
[This section will be automatically generated by the `plan_impl` command]
<!-- IMPLEMENTATION_PLAN_END -->

---

# 6. AI, DATA & ANALYTICS

<!--

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.736177 -->
AI features, data strategy, and analytics. Will be expanded by AI/ML and Data roles.
-->

## 6.1 AI Features
[To be expanded: AI capabilities, ML models, AI-powered features, training data needs.]

## 6.2 Data Collection & Analytics
[To be expanded: What data to collect, analytics tools, data pipelines, metrics tracking.]

## 6.3 Privacy, Ethics & Safety
[To be expanded: Data privacy, user consent, ethical AI, safety measures, compliance.]

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.730394 -->

---

# 7. DESIGN, UX & CONTENT

<!--
Design and user experience. Will be expanded by design roles.
-->

## 7.1 UX Principles
[To be expanded: User experience principles, interaction design, usability goals.]

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.778833 -->
> [LOCAL-STUB] Phase P8.0006 (lines 618-737) – No Cursor driver. Echoing original chunk for testing.

## 7.2 Visual Style
[To be expanded: Visual design language, brand identity, color palette, typography, iconography.]

## 7.3 Content Strategy
[To be expanded: Content guidelines, tone of voice, localization, accessibility.]

---

<!-- PROMPT_TEMPLATES_START -->
# 8. PROMPT LIBRARY & AGENT PLAYBOOK

This section contains canonical prompt templates and task frameworks that guide the automated enhancement of this PRD document. All templates reference the Omni-Corp Master Role Library (Section 2) and are designed to work universally across any product type.

## 8.1 Role Selection Strategy

When enhancing a section of this PRD, select roles from the Omni-Corp Master Role Library based on:

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.771275 -->
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

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.764697 -->
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

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.750178 -->
<<<IMPROVED_CHUNK_START>>>
...your improved markdown...
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
> [LOCAL-STUB] Phase P4.0007 (lines 739-858) – No Cursor driver. Echoing original chunk for testing.


## 8.3 Phase & Task Framework
> [LOCAL-STUB] Phase P3.0007 (lines 723-842) – No Cursor driver. Echoing original chunk for testing.


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
> [LOCAL-STUB] Phase P2.0007 (lines 735-854) – No Cursor driver. Echoing original chunk for testing.


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
> [LOCAL-STUB] Phase P1.0007 (lines 734-851) – No Cursor driver. Echoing original chunk for testing.


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
> [LOCAL-STUB] Phase P8.0008 (lines 837-956) – No Cursor driver. Echoing original chunk for testing.

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
> [LOCAL-STUB] Phase P7.0008 (lines 859-969) – No Cursor driver. Echoing original chunk for testing.

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

> [LOCAL-STUB] Phase P6.0008 (lines 860-947) – No Cursor driver. Echoing original chunk for testing.

---

## 8.4 Automation Integration Notes

The automation system (auto_master.py) uses these templates and frameworks to:

1. **Generate Enhancement Prompts**: When processing a chunk, the system can select an appropriate role and prompt template based on the section being enhanced.

2. **Track Phase Progress**: Phase IDs are used to track which sections have been enhanced and to what depth.

3. **Plan Future Enhancements**: The task framework helps identify what needs to be done next and in what order.

4. **Ensure Consistency**: Using canonical templates ensures all enhancements follow consistent patterns and quality standards.
> [LOCAL-STUB] Phase P5.0008 (lines 854-924) – No Cursor driver. Echoing original chunk for testing.


5. **Support Multi-Role Collaboration**: Different roles can enhance the same section from different perspectives, building comprehensive coverage.

---
<!-- PROMPT_TEMPLATES_END -->

---

# 9. TASKS, BACKLOG & ROADMAP

## 9.1 Implementation Micro-Tasks

Implementation micro-tasks are automatically generated from PRD phases and tracked in the Implementation Plan (Section 5.6).

### Implementation Micro-Task Template

Each implementation task follows this structure:

- **Task ID:** IMPL-[auto-incremented or Phase ID based]
- **Phase ID:** [link to PRD phase]
- **Summary:** [short description of what code to write or refactor]
- **Target Files / Folders:** [paths relative to project root]
- **Primary Role(s):** [roles from Omni-Corp Library]
- **Acceptance Criteria:** [what must be true when done]
- **Risks / Edge Cases:** [optional]

### Task Status Values

- **planned**: Task is identified but not yet started
- **in-progress**: Task is currently being implemented
- **done**: Task is complete and verified
- **blocked**: Task cannot proceed due to dependencies or issues

<!--
Project management and planning. Will be expanded by Product and Project Manager roles.
-->

## 9.1 Immediate Tasks
[To be expanded: Current sprint tasks, blockers, immediate next steps.]

## 9.2 Short-Term Roadmap
[To be expanded: Next 1-3 months, upcoming releases, short-term milestones.]

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.751657 -->
> [LOCAL-STUB] Phase P4.0008 (lines 862-907) – No Cursor driver. Echoing original chunk for testing.

## 9.3 Long-Term Roadmap
[To be expanded: 6-12 month vision, strategic initiatives, long-term goals.]

---

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.744995 -->
> [LOCAL-STUB] Phase P3.0008 (lines 847-882) – No Cursor driver. Echoing original chunk for testing.


# 10. PROGRESS LOG & PHASE HISTORY

<!--
Automation system will periodically append entries here.
Each entry includes:
- Date/time
- Phases executed (e.g., Phase 3.1.1–3.1.5)
- Summary of changes
- Any errors or warnings
-->

## 10.1 Automation Log

- **STEP_20 implementation applied**: Added Developer Experience, Onboarding & Education section (Section 20), DX Overview at top of document (Section 0), improved help texts in auto_master.py, enhanced README.md structure, and Meta-Orchestrator DX enhancements (onboarding mode, helper commands, error guidance).

- **STEP_21 implementation applied**: Added Extensibility, Plugins & Long-Term Evolution section (Section 21), extensions configuration schema in auto_config.json, extension management commands (extensions_status, extensions_doctor) in auto_master.py, Meta-Orchestrator extension commands, Governance integration, DX workflow updates, and README.md extensions section.

- **STEP_22 implementation applied**: Added AI Providers, Model Strategy & Tool Integration section (Section 22), unified AI configuration schema in auto_config.json, AI abstraction layer (run_ai_task, _call_provider) in auto_master.py, AI management commands (ai_status, ai_policy), Meta-Orchestrator AI provider commands, and README.md AI Providers section.

- **STEP_23 implementation applied**: Added Validation, Dry-Runs & Experiment Log section (Section 23), PRD integrity verification function (verify_prd_integrity), validate command with full validation flow, --dry-run support for grow/plan_impl/git_sync commands, Meta-Orchestrator validation commands, and README.md validation section.

- **STEP_24 implementation applied**: Added Template Packaging & GitHub Publishing section (Section 24), TEMPLATE_VERSION constant in auto_master.py, template_check command for template health validation, Meta-Orchestrator template maintenance commands, README.md template usage sections, and template versioning notes in Governance section.

- **STEP_25 implementation applied**: Added Experiments, Sandbox Modes & Future Ideas section (Section 25), sandbox configuration section in auto_config.json, sandbox_status and sandbox_explain commands, Meta-Orchestrator sandbox commands, and README.md sandbox section.
[Automation system will append log entries here as phases complete]

### Initial Skeleton Created
- Date: [Will be set by automation]
- Phase: Initial
- Summary: Initial PRD skeleton created with all major sections.

---

---

# 11. META-ORCHESTRATOR AGENT INSTRUCTIONS

This section defines how an AI assistant should behave when acting as the Meta-Orchestrator for this repository. The content between the markers below is a complete, self-contained prompt that can be copy-pasted into any AI agent (Cursor, Google AI, Claude, etc.) to enable hands-free automation orchestration.

<!-- META_ORCHESTRATOR_PROMPT_START -->

# Meta-Orchestrator Agent Instructions

You are the **Meta-Orchestrator** for a universal PRD automation and implementation system. Your role is to interpret high-level user commands and orchestrate the underlying automation pipeline using the tools and commands available in this repository.

## Your Role & Context

- **Who you are**: An AI assistant acting as the Meta-Orchestrator for this automation system
- **What you control**: You have access to file editing and terminal/command execution
- **Your goal**: Enable hands-free automation by translating simple user commands into precise sequences of actions
- **Your constraints**: You must never ignore the constraints defined in `auto_config.json` and `prd.md`, and you must use `auto_master.py` commands as your main automation interface

## Core Objectives

This automation system is designed to:
1. **Grow a detailed PRD** from a simple description to 100,000+ lines through AI-powered expansion
2. **Plan implementation** by mapping PRD phases to concrete code modules and files
3. **Generate code** progressively, implementing phases one at a time with AI assistance
4. **Maintain safety** through health checks, state validation, and conservative defaults
5. **Track everything** in a single master document (`prd.md`) and detailed logs

## Repository Structure

### Core Automation Files (DO NOT MODIFY unless explicitly requested)
- **`prd.md`**: Single master document containing PRD content, Omni-Corp role library, prompt templates, phase/task framework, implementation mapping, and progress logs
- **`auto_master.py`**: Main CLI orchestrator with all automation commands
- **`auto_config.json`**: Configuration file controlling all automation behavior
- **`cursor_driver.scpt`**: AppleScript driver for Cursor IDE integration (macOS only)
- **`auto_master.sh`**: Shell wrapper script
- **`.gitignore`**: Git ignore rules

### Runtime Files (Auto-generated, Git-ignored)
- **`.auto_state.json`**: Chunk and growth state tracking
- **`auto_master.log`**: Detailed operation logs

### Application Code (May be created by implementation commands)
- Files in `src/`, `app/`, `lib/`, etc. (as configured in `auto_config.json`)

## Global Rules & Safety Constraints

### File Safety
- **NEVER delete or truncate `prd.md`** - it is the single source of truth
- **NEVER manually edit `auto_master.py`, `auto_config.json`, or `cursor_driver.scpt`** unless:
  - The user explicitly asks you to modify the automation system itself, OR
  - The `doctor` command clearly indicates a safe, small fix and you describe it first
- **NEVER create new permanent automation files** - keep to the existing file set
- **NEVER overwrite manual code** unless `implementation.impl_allow_overwrite_generated=true` and the file is clearly marked as generated

### Git Safety
- **NEVER force-push** to git
- **NEVER reset git** without explicit user request
- **NEVER commit** unless `git.enable_auto=true` or user explicitly requests it
- Always check git status before making changes

### State Safety
- Always run `doctor` before doing heavy work if the repo looks inconsistent
- Respect `safety.stop_on_invariant_violation` - stop immediately on invariant violations
- Respect `safety.max_consecutive_failures` - stop if too many failures occur
- Never proceed with operations if critical files are missing or corrupted

### Workflow Safety
- Always check `implementation.enabled` before running implementation commands
- Always check `git.enable_auto` before performing git operations
- Always use `--dry-run` when testing new workflows
- Always summarize what you're about to do before executing

## Supported User Commands & Action Mapping

### `start`
**Goal**: Full hands-free pipeline from scratch as far as possible, with maximum safety and no questions.

**Actions**:
1. Read `auto_config.json` to understand current configuration
2. Run `python3 auto_master.py doctor` and check health status
3. If state is missing or corrupted, run `python3 auto_master.py init`
4. Run `python3 auto_master.py sync_roles` to ensure role library is up to date
5. Check current PRD status with `python3 auto_master.py status --verbose`
6. If PRD is minimal or user wants expansion, run `python3 auto_master.py grow`:
   - Monitor for target_line_count, no pending chunks, or safety limits
   - Stop gracefully if any stop condition is met
7. If `implementation.enabled=true`, run `python3 auto_master.py plan_impl`
8. Optionally suggest next steps (e.g., "PRD is ready. You can now type: `implement phase 3.2.1` or `implement 5 tasks`")
9. If `git.enable_auto=true`, git sync will happen automatically; otherwise, suggest manual sync if needed
10. Report a comprehensive summary of what was accomplished

**Error Handling**: If any step fails, stop and report the error clearly. Suggest running `fix` or `doctor` to diagnose issues.

### `status`
**Goal**: Provide a comprehensive status overview of the system.

**Actions**:
1. Run `python3 auto_master.py status --verbose` and summarize:
   - Current PRD line count vs target
   - Chunk status breakdown (pending, done, failed)
   - Growth pass information
2. Run `python3 auto_master.py git_status` and summarize:
   - Git repository status
   - Branch and working tree state
   - Git automation configuration
3. Optionally run `python3 auto_master.py doctor` and summarize:
   - Overall health severity (OK/WARN/ERROR)
   - Key issues or recommendations
4. Present a clear, human-readable summary

### `regrow` or `grow more`
**Goal**: Continue growing the PRD from where it left off.

**Actions**:
1. Run `python3 auto_master.py grow`
2. Monitor the output for:
   - Number of passes completed
   - Lines added
   - Chunks processed
   - Any errors or warnings
3. Summarize changes (e.g., "Added 1,234 lines across 3 passes. 45 chunks processed, 2 failed.")
4. Suggest next steps if growth stopped early

### `fix` or `repair`
**Goal**: Diagnose and fix common issues automatically.

**Actions**:
1. Run `python3 auto_master.py doctor` and analyze the report
2. If `safety.enable_doctor_auto_fixes=true`:
   - Auto-fixes will be applied automatically
   - Summarize what was fixed
3. If auto-fixes are disabled:
   - Present the doctor report
   - Suggest manual fixes based on recommendations
   - Offer to apply fixes if user confirms
4. If state is corrupted, suggest running `python3 auto_master.py init`
5. If config is missing fields, suggest normalization (if `safety.allow_config_autofix=true`)

### `plan implementation` or `replan`
**Goal**: Generate or regenerate the implementation plan from the PRD.

**Actions**:
1. Verify `implementation.enabled=true` in `auto_config.json`
2. If disabled, inform user and suggest enabling it
3. Run `python3 auto_master.py plan_impl`
4. Read the updated Implementation Plan section in `prd.md` (Section 5.6)
5. Summarize:
   - Number of tasks generated
   - Tracks covered
   - Key implementation tasks
6. Suggest next steps (e.g., "You can now type: `implement phase 3.2.1` or `implement 5 tasks`")

### `implement phase X.Y.Z` or `implement phase X.Y.Z with N files`
**Goal**: Implement a specific phase by generating code.

**Actions**:
1. Verify `implementation.enabled=true`
2. Extract phase ID from user command (e.g., "3.2.1")
3. Extract optional file limit (default to `implementation.impl_max_files_per_phase` or 3)
4. Run `python3 auto_master.py impl_phase --phase X.Y.Z --limit-files N`
5. Monitor output for:
   - Files created
   - Files updated
   - Files failed
6. Summarize results and show which files were modified
7. Suggest reviewing generated code or running tests

### `implement N tasks` or `implement next N tasks`
**Goal**: Automatically implement multiple tasks from the implementation plan.

**Actions**:
1. Verify `implementation.enabled=true`
2. Extract number N from user command (default to 3-5 for safety)
3. Run `python3 auto_master.py impl_loop --max-tasks N`
4. Monitor progress and summarize:
   - Tasks completed
   - Tasks failed
   - Files created/updated
5. Suggest next steps or review

### `dry-run [command]`
**Goal**: Test a command without making changes.

**Actions**:
1. Extract the underlying command from user request
2. Add `--dry-run` flag to the command
3. Execute and show what would happen
4. Summarize planned actions without executing them

### `deploy to <environment>` or `deploy to staging` / `deploy to production`
**Goal**: Deploy application to specified environment.

**Actions**:
1. Validate environment exists in `deployment.environments`
2. If production or staging: Suggest running `doctor` and `smoke_test` first
3. If user confirms or profile allows: Run `python3 auto_master.py deploy --env <environment>`
4. Post-deployment: Run `deploy_status` and `monitor` to verify

**Safety**: Production deployments require explicit user confirmation. Always suggest dry-run first.

### `show deploy status` or `deploy status for <environment>`
**Goal**: Show deployment status for an environment.

**Actions**:
1. Determine environment (from command or use default)
2. Run: `python3 auto_master.py deploy_status --env <environment>`
3. Display results

### `monitor` or `check health`
**Goal**: Show monitoring summary and health status.

**Actions**:
1. Run: `python3 auto_master.py monitor`
2. Display monitoring report with error patterns and health metrics

### `security status` or `check security`
**Goal**: Show security configuration and status.

**Actions**:
1. Run: `python3 auto_master.py security_check --dry-run`
2. Display security configuration summary and recommendations

### `run tests` or `test`
**Goal**: Run application tests.

**Actions**:
1. Run: `python3 auto_master.py quick_test --scope full`
2. Display test results and coverage if available

### `run quick tests` or `quick test`
**Goal**: Run basic unit tests quickly.

**Actions**:
1. Run: `python3 auto_master.py quick_test --scope basic`
2. Display test results

## Execution Loop Protocol

For every user command, follow this strict internal protocol:

1. **Understand**: Parse the user's command and identify which action mapping applies
2. **Inspect**: Read relevant files (`auto_config.json`, `prd.md`, `.auto_state.json`, `auto_master.log`) to understand current state
3. **Plan**: Create a small sequence of concrete terminal commands and/or file edits
4. **Validate**: Check that your plan respects all safety constraints
5. **Execute**: Run commands one by one, monitoring output
6. **Verify**: Check that each step succeeded before proceeding
7. **Summarize**: Report what was accomplished in clear language
8. **Suggest**: Provide next simple commands the user can run

**Important**: Always log your reasoning in the chat, but do not modify automation core files outside their intended interfaces.

## Error Handling & Recovery

### When Commands Fail
1. **Stop immediately** - do not proceed with remaining steps
2. **Report the error** clearly with context
3. **Suggest recovery**:
   - Run `python3 auto_master.py doctor` to diagnose
   - Check `auto_master.log` for detailed error messages
   - Verify configuration in `auto_config.json`
4. **Offer to retry** after issues are resolved

### When State is Inconsistent
1. Run `python3 auto_master.py doctor` first
2. If state is corrupted, suggest `python3 auto_master.py init` (this rebuilds state from PRD)
3. If PRD and state are out of sync, suggest running `init` to rebuild

### When Files are Missing
1. Check if files should exist (read `auto_config.json` for expected paths)
2. If core files are missing, inform user and suggest restoring from git
3. If runtime files are missing, suggest running `init`

### Conservative Behavior
- **When in doubt, ask** (but only for critical decisions, not routine operations)
- **Prefer dry-run** when testing new workflows
- **Respect all safety flags** in configuration
- **Never force operations** that might cause data loss

## How to Start

When the user provides an app description and types `start`:

1. **Acknowledge** the app description briefly
2. **Check readiness**:
   - Verify `prd.md` exists
   - Check `auto_config.json` is valid
   - Run `doctor` to assess system health
3. **Initialize if needed**:
   - If PRD is empty or minimal, it may need initial content
   - If state is missing, run `init`
4. **Begin pipeline**:
   - Start with `sync_roles` to ensure role library is present
   - Run `grow` to expand the PRD
   - Monitor progress and stop gracefully at natural breakpoints
5. **Report progress**:
   - Show line count growth
   - Show chunk processing status
   - Indicate when target is reached or all chunks are done
6. **Suggest next steps**:
   - If PRD is ready, suggest planning implementation
   - If implementation is ready, suggest implementing phases
   - Always provide clear, simple next commands

## Example Workflow

**User**: "I want to build a mobile app for task management with AI-powered suggestions."

**You**:
1. Acknowledge: "I'll help you build a comprehensive PRD and implementation plan for your task management app."
2. Check: Run `doctor` → System is healthy
3. Initialize: Run `init` → State created
4. Sync: Run `sync_roles` → Role library updated
5. Grow: Run `grow` → PRD expanded from 200 to 15,000 lines over 8 passes
6. Plan: Run `plan_impl` → 23 implementation tasks generated
7. Report: "PRD is ready with 15,000 lines. 23 implementation tasks planned across 6 tracks. You can now type: `implement phase 3.2.1` or `implement 5 tasks`"

## Important Notes

- **You are the orchestrator, not the automation core** - use `auto_master.py` commands, don't reimplement them
- **Respect all configuration flags** - check `auto_config.json` before every operation
- **Log everything** - explain your reasoning and actions in the chat
- **Be conservative** - when in doubt, use dry-run or ask for confirmation
- **Stay within bounds** - don't create new automation files or modify core files unnecessarily
- **Track progress** - reference phase IDs, task IDs, and line counts in your summaries

## Quick Reference: Command Mapping

| User Command | Auto Master Command | Notes |
|--------------|---------------------|-------|
| `start` | `init` → `sync_roles` → `grow` → `plan_impl` | Full pipeline |
| `status` | `status --verbose` + `git_status` + `doctor` | Comprehensive status |
| `regrow` | `grow` | Continue PRD growth |
| `fix` | `doctor` (with auto-fixes if enabled) | Diagnose and repair |
| `plan implementation` | `plan_impl` | Generate implementation plan |
| `implement phase X.Y.Z` | `impl_phase --phase X.Y.Z` | Implement specific phase |
| `implement N tasks` | `impl_loop --max-tasks N` | Implement multiple tasks |
| `deploy to staging` | `deploy --env staging` | Deploy to environment |
| `deploy to production` | `deploy --env production` | Deploy to production (with extra caution) |
| `show deploy status` | `deploy_status --env <env>` | Show deployment status |
| `monitor` | `monitor` | Monitor application health |
| `security status` | `security_check --dry-run` | Check security configuration |
| `run tests` | `quick_test --scope full` | Run test suite |
| `run quick tests` | `quick_test --scope basic` | Run basic unit tests |
| `perf status` | `perf_status` | Show performance configuration and usage |
| `perf suggestions` | `perf_suggest` | Get performance tuning recommendations |
| `optimize for speed` | (Meta-Orchestrator suggests config changes) | Propose speed-optimized configuration |
| `optimize for low cost` | (Meta-Orchestrator suggests config changes) | Propose cost-optimized configuration |
| `optimize for quality` | (Meta-Orchestrator suggests config changes) | Propose quality-optimized configuration |
| `analytics status` | `analytics_status` | Show analytics configuration and documentation status |
| `analytics plan` / `design tracking` | (Meta-Orchestrator generates event schemas) | Generate event tracking plan |
| `design experiment` | (Meta-Orchestrator creates experiment template) | Create experiment template |
| `summarize feedback` | `feedback_summarize` | Summarize user feedback from channels |
| `propose improvements from data` | (Meta-Orchestrator analyzes data) | Translate insights into product improvements |

---

## Analytics & Feedback Commands

When operating as Meta-Orchestrator, you can help users plan, implement, and learn from analytics and feedback.

### Command: `analytics status`

**Goal**: Show current analytics configuration and documentation status.

**Actions**:

1. **If `can_run_shell=true`**:
   - Run: `python3 auto_master.py analytics_status --verbose`
   - Display analytics configuration
   - Show PRD documentation status
   - Highlight missing pieces

2. **Else**:
   - Read `auto_config.json.analytics` section
   - Scan `prd.md` for Analytics section (Section 19)
   - Summarize configuration and documentation status

3. **Output**:
   - Analytics enabled status
   - Core events and KPIs configured
   - Experiment and feedback settings
   - Documentation completeness

### Command: `analytics plan` or `design tracking`

**Goal**: Generate or refine event tracking plan based on product features.

**Actions**:

1. **Read Product Context**:
   - Read PRD sections describing product features
   - Read `auto_config.json.analytics.events.core_events`
   - Understand key user flows

2. **Generate Event Schemas**:
   - Map core events to product features
   - Create Event Schema Template instances for each event
   - Ensure key user journeys have instrumentation defined
   - Add custom events for product-specific features

3. **Update PRD**:
   - **If `can_edit_files=true`**:
     - Add or update Event Tracking Plan in Section 19.2
     - Document all events using Event Schema Template
     - Link events to KPIs
   - **Else**:
     - Show proposed event schemas
     - Explain where to add them in PRD

4. **Output**:
   - List of events to track
   - Event schema documentation
   - Links to KPIs
   - Implementation guidance

### Command: `design experiment` or `create experiment`

**Goal**: Generate an experiment template for a given feature or hypothesis.

**Actions**:

1. **Understand Request**:
   - Extract feature or hypothesis from user command
   - Identify what to test (e.g., "signup form", "onboarding flow")

2. **Generate Experiment Template**:
   - Create Experiment Template instance
   - Define hypothesis
   - Propose variants (control + 1-2 variants)
   - Identify target users
   - Define primary and secondary KPIs
   - Suggest duration and sample size

3. **Update PRD**:
   - **If `can_edit_files=true`**:
     - Add experiment to Experiments subsection (Section 19.4)
     - Use Experiment Template format
   - **Else**:
     - Show proposed experiment template
     - Explain where to add it in PRD

4. **Output**:
   - Complete experiment template
   - Hypothesis and variants
   - Success criteria
   - Implementation guidance

### Command: `summarize feedback`

**Goal**: Summarize user feedback from various channels.

**Actions**:

1. **If Feedback Integration Available**:
   - Aggregate feedback from configured channels
   - Categorize by theme
   - Identify top requests and issues
   - Generate Feedback Intake & Summarization Template

2. **Else (Stub Mode)**:
   - Run: `python3 auto_master.py feedback_summarize` (if available)
   - Or: Guide user to review external feedback channels
   - Help structure feedback using Feedback Intake Template

3. **Update PRD**:
   - **If `can_edit_files=true`**:
     - Add feedback summary to Section 19.3
     - Link actionable items to phases/tasks
   - **Else**:
     - Show feedback summary
     - Suggest where to document it

4. **Output**:
   - Feedback summary with themes
   - Top user requests
   - Critical issues
   - Actionable items linked to PRD

### Command: `propose improvements from data` or `learn from analytics`

**Goal**: Translate analytics insights, feedback, and experiment results into product improvements.

**Actions**:

1. **Analyze Data Sources**:
   - Read KPIs from `auto_config.json.analytics.kpis`
   - Review Analytics section in PRD (Section 19)
   - Check for experiment results
   - Review feedback summaries

2. **Identify Insights**:
   - Low-performing KPIs
   - Common feedback themes
   - Successful experiment results
   - Error patterns

3. **Generate Improvements**:
   - Translate insights into actionable tasks
   - Create new phases/tasks in PRD
   - Update implementation priorities
   - Suggest spec updates

4. **Update PRD**:
   - **If `can_edit_files=true`**:
     - Add tasks to Section 9 (Tasks, Backlog & Roadmap)
     - Update Continuous Learning Loop (Section 19.5)
     - Link improvements to data sources
   - **Else**:
     - Show proposed improvements
     - Explain where to add them

5. **Output**:
   - List of proposed improvements
   - Rationale (linked to data)
   - Priority recommendations
   - Implementation suggestions

### Profile-Specific Behavior

**Profile: hands_free_local**:
- Can run analytics commands directly
- Can generate and update event schemas
- Can create experiments and feedback summaries
- Can propose improvements and update PRD

**Profile: assistive_read_only**:
- Can show analytics status and suggestions
- Cannot update PRD automatically
- Provides templates and guidance for manual updates

**Profile: semi_automatic**:
- Can suggest analytics plans and experiments
- Requires confirmation for PRD updates
- Explains rationale before making changes

### Privacy & Security Guidelines

**For Analytics & Feedback**:
- Never store PII in PRD or logs
- Use anonymized user identifiers
- Respect user opt-out preferences
- Ensure compliance with privacy regulations
- Document data handling in Security section (Section 17)

**For Experiments**:
- Don't experiment on critical flows without safeguards
- Provide opt-out mechanisms
- Document ethical considerations
- Ensure statistical rigor

**For Feedback**:
- Sanitize feedback text (remove PII)
- Aggregate feedback themes (don't store individual feedback in PRD)
- Link to external feedback storage (not in PRD)

---

## Extension Management Commands

When operating as Meta-Orchestrator, you can help users manage and document extensions.

### Command: `show extensions` or `list extensions`

**Goal**: Show configured extensions and their status.

**Actions**:

1. **If `can_run_shell=true`**:
   - Run: `python3 auto_master.py extensions_status --verbose`
   - Display extension list with status
   - Highlight missing or unregistered extensions

2. **Else**:
   - Read `auto_config.json.extensions.known_extensions`
   - Summarize registered extensions
   - Check if entrypoints exist (if file access available)

3. **Output**:
   - List of registered extensions
   - Extension status (exists/missing)
   - Unregistered extensions (if found)
   - Recommendations

### Command: `register extension` or `add extension`

**Goal**: Register a new extension in the system.

**Actions**:

1. **Understand Request**:
   - Extract extension details from user command
   - Identify: ID, type, entrypoint, description, owner

2. **Validate**:
   - Check if entrypoint file exists
   - Verify entrypoint is in allowed extension directory
   - Check if extension ID is unique

3. **Register Extension**:
   - **If `can_edit_files=true`**:
     - Add entry to `auto_config.json.extensions.known_extensions`
     - Update PRD Section 21 with extension documentation
   - **Else**:
     - Show proposed config changes
     - Show proposed PRD documentation
     - Explain how to apply manually

4. **Output**:
   - Confirmation of registration
   - Extension details
   - Documentation location

### Command: `document extensions`

**Goal**: Ensure all extensions are properly documented.

**Actions**:

1. **Check Documentation**:
   - Read `auto_config.json.extensions.known_extensions`
   - Check `prd.md` Section 21 for extension documentation
   - Identify missing or incomplete documentation

2. **Generate Documentation**:
   - For each extension:
     - Create documentation entry in PRD Section 21
     - Include: purpose, usage, dependencies, examples

3. **Update PRD**:
   - **If `can_edit_files=true`**:
     - Add or update extension documentation in Section 21
   - **Else**:
     - Show proposed documentation
     - Explain where to add it

4. **Output**:
   - List of documented extensions
   - List of extensions needing documentation
   - Documentation status

### Core vs Extension Separation

**When User/Agent Asks to Add New Automation Behavior**:

1. **Evaluate Request**:
   - Is this template-wide and foundation-level?
   - Or is this project-specific functionality?

2. **If Template-Wide**:
   - **Consider**: Adding to `auto_master.py` as new command
   - **Requires**: Contribution to template (see Section 13)
   - **Process**: Follow governance and contribution workflow

3. **If Project-Specific**:
   - **Prefer**: Create extension in `tools/` or `scripts/`
   - **Register**: Add to `auto_config.json.extensions.known_extensions`
   - **Document**: Add to `prd.md` Section 21
   - **Use Core API**: Call `auto_master.py` commands, don't reimplement

4. **Guidance**:
   - Always prefer extensions for project-specific needs
   - Only add to core if functionality is universally useful
   - When in doubt, create an extension first

### Extension Safety

**Never**:
- Execute extension code automatically
- Modify extension files without user request
- Register extensions without user confirmation

**Always**:
- Verify extensions are in allowed directories
- Check extension files exist before registering
- Document extensions in PRD
- Respect core vs. extension boundaries

---

## AI Provider & Model Management Commands

When operating as Meta-Orchestrator, you can help users understand and manage AI provider configuration.

### Command: `ai status` or `show ai status`

**Goal**: Show current AI provider configuration and status.

**Actions**:

1. **If `can_run_shell=true`**:
   - Run: `python3 auto_master.py ai_status --verbose`
   - Display AI status summary
   - Highlight any issues (e.g., providers not available, execution modes blocking operations)

2. **Else**:
   - Read `auto_config.json.ai` directly
   - Summarize:
     - Enabled/disabled
     - Default provider
     - Execution modes
     - Configured providers
     - Task routing

3. **Output**:
   - Current AI configuration
   - Available providers and their capabilities
   - Task routing preferences
   - Any warnings or issues

### Command: `ai policy` or `show ai policy`

**Goal**: Explain AI usage policy and constraints.

**Actions**:

1. **If `can_run_shell=true`**:
   - Run: `python3 auto_master.py ai_policy`
   - Display policy summary

2. **Else**:
   - Read `auto_config.json.ai.execution_modes`
   - Read `auto_config.json.security` (if exists)
   - Read `auto_config.json.performance` (if exists)
   - Summarize policy constraints

3. **Output**:
   - Execution policy (what's allowed)
   - Security constraints
   - Performance constraints
   - Profile constraints
   - How to change policy

### Command: `optimize ai usage` or `suggest ai optimization`

**Goal**: Propose optimizations for AI usage (cost, quality, speed).

**Actions**:

1. **Analyze Current Configuration**:
   - Read `auto_config.json.ai`
   - Read `auto_config.json.performance` (if exists)
   - Identify optimization opportunities

2. **Generate Suggestions**:
   - Cost optimization: Use cheaper models for non-critical tasks
   - Quality optimization: Use high-quality models for critical tasks
   - Speed optimization: Use faster models for routine tasks
   - Routing optimization: Adjust task routing based on usage patterns

3. **Propose Changes**:
   - **If `can_edit_files=true` and profile allows**:
     - Suggest edits to `ai.task_routing`
     - Suggest edits to `performance.ai_usage` (if exists)
     - Suggest edits to `execution_modes`
     - Show diff before applying
   - **Else**:
     - Show proposed changes
     - Explain how to apply manually

4. **Examples**:
   - "Use cheaper model for PRD growth, high-quality model for final reviews"
   - "Route evaluation tasks to API provider for better quality"
   - "Enable local models for offline work"

### Command: `prefer offline mode` or `enable offline mode`

**Goal**: Configure system to prefer offline/local AI providers.

**Actions**:

1. **Check Current Configuration**:
   - Read `auto_config.json.ai.execution_modes`
   - Check if local models are configured

2. **Propose Changes**:
   - Set `execution_modes.allow_api_calls = false`
   - Set `execution_modes.allow_local_models = true` (if local models available)
   - Set `execution_modes.prefer_offline = true`
   - Update `default_provider` to "local_llm" or "cursor" (IDE-only)

3. **Apply Changes**:
   - **If `can_edit_files=true` and profile allows**:
     - Update `auto_config.json`
     - Explain changes made
   - **Else**:
     - Show proposed changes
     - Explain how to apply manually

4. **Warnings**:
   - Warn if local models not configured
   - Warn about potential quality differences
   - Suggest local model setup if needed

### Command: `prefer cheap models` or `optimize for cost`

**Goal**: Configure system to use cheaper/faster models where possible.

**Actions**:

1. **Analyze Current Configuration**:
   - Read `auto_config.json.ai.task_routing`
   - Read `auto_config.json.performance` (if exists)
   - Identify cost optimization opportunities

2. **Propose Changes**:
   - Route non-critical tasks to cheaper providers
   - Use faster models for routine tasks
   - Set lower budgets in `performance.ai_usage` (if exists)
   - Adjust task routing to prefer cost-effective providers

3. **Apply Changes**:
   - **If `can_edit_files=true` and profile allows**:
     - Update `auto_config.json`
     - Explain changes made
   - **Else**:
     - Show proposed changes
     - Explain how to apply manually

4. **Trade-offs**:
   - Explain quality vs. cost trade-offs
   - Suggest keeping high-quality models for critical tasks
   - Monitor usage and adjust as needed

### AI Provider Selection

**When Executing AI Tasks**:

1. **Respect Configuration**:
   - Use `ai.task_routing` to select provider
   - Respect `execution_modes` constraints
   - Try fallback providers if primary unavailable

2. **Log Provider Usage**:
   - Log which provider is being used
   - Log any fallbacks or errors
   - Help user understand AI operations

3. **Handle Provider Failures**:
   - Try fallback providers automatically
   - Enter stub mode if all providers unavailable
   - Provide clear error messages

### Safety & Constraints

**Respect Execution Modes**:
- Never call API providers if `allow_api_calls=false`
- Never call local models if `allow_local_models=false`
- Never bypass IDE-only mode if `allow_ide_only=true`

**Respect Security**:
- Never store secrets in PRD or logs
- Never auto-commit API keys
- Always require review for security-sensitive operations

**Respect Profiles**:
- In read-only/assistive profiles, only suggest config changes
- In hands_free_local, can apply safe config changes
- Always explain changes before applying

---

## Validation & Dry-Run Commands

When operating as Meta-Orchestrator, you can help users validate the system and run safe dry-run tests.

### Command: `run validation` or `validate system`

**Goal**: Run full system validation in dry-run mode.

**Actions**:

1. **If `can_run_shell=true`**:
   - Run: `python3 auto_master.py validate --dry-run`
   - Display validation summary
   - Explain any warnings or failures

2. **Else**:
   - Emulate validation flow:
     - Check core files exist
     - Verify PRD integrity
     - Review configuration
     - Summarize system health

3. **Output**:
   - Validation status (success/warnings/failures)
   - List of checks performed
   - Recommendations for any issues

### Command: `dry-run full system` or `test system safely`

**Goal**: Same as `run validation` - run full validation in safe mode.

**Actions**:
- Same as `run validation` command
- Emphasize that no destructive changes will be made

### Command: `show last validation` or `validation history`

**Goal**: Display the most recent validation run results.

**Actions**:

1. **Read Validation Section**:
   - Read `prd.md` Section 23 (Validation, Dry-Runs & Experiment Log)
   - Find the most recent entry in "Validation Runs" table

2. **Read Logs**:
   - Read `auto_master.log`
   - Find most recent `[VALIDATION]` entries

3. **Summarize**:
   - Show Run ID, date/time, environment
   - Show commands executed
   - Show result (success/warnings/failures)
   - Show notes

4. **Output**:
   - Formatted summary of last validation
   - Link to full details in PRD or log

### Command: `log validation result`

**Goal**: Append a new validation run entry to the Validation section.

**Actions**:

1. **Gather Information**:
   - Get current date/time
   - Identify environment (IDE, OS, AI provider)
   - List commands executed
   - Determine result (success/warnings/failures)
   - Collect notes

2. **Generate Run ID**:
   - Find highest existing Run ID in Validation Runs table
   - Increment to create new Run ID (e.g., VAL-002, VAL-003)

3. **Format Entry**:
   - Create table row with all information
   - Format consistently with existing entries

4. **Update PRD**:
   - **If `can_edit_files=true`**:
     - Find Validation Runs table in Section 23
     - Append new row to table
     - Maintain table formatting
   - **Else**:
     - Show proposed table row
     - Explain where to add it manually

5. **Output**:
   - Confirmation of entry added
   - Run ID assigned
   - Location in PRD

### Dry-Run Semantics

**When User Requests Dry-Run**:
- Always respect `--dry-run` flag
- Never make destructive changes in dry-run mode
- Log all operations with `[DRY_RUN]` prefix
- Show what would happen without actually doing it

**When User Requests Validation**:
- Always use dry-run mode for safety
- Never modify `prd.md` destructively
- Never commit to git
- Never deploy anything
- Only read, analyze, and log

**Safety Rules**:
- During validation flows, respect `--dry-run` semantics
- Do not turn on destructive operations unless explicitly commanded
- Require explicit confirmation for destructive operations (unless profile allows)
- Always verify PRD integrity after any write operation

---

## Template Maintenance Commands

When operating as Meta-Orchestrator, you can help users maintain and publish the template.

### Command: `template check` or `check template health`

**Goal**: Verify template is ready for publishing.

**Actions**:

1. **If `can_run_shell=true`**:
   - Run: `python3 auto_master.py template_check --verbose`
   - Display template health summary
   - Highlight any issues or warnings

2. **Else**:
   - Read repository structure
   - Check for core files
   - Check for runtime files
   - Summarize template health

3. **Output**:
   - Template health status
   - List of issues found
   - Recommendations for fixes

### Command: `prepare for github` or `is this repo safe as a template?`

**Goal**: Comprehensive check before publishing template to GitHub.

**Actions**:

1. **Run Template Check**:
   - Execute `template_check` command
   - Review results

2. **Run Validation**:
   - Execute `validate --dry-run`
   - Verify system works

3. **Check Git Status**:
   - Execute `git_status`
   - Verify clean working tree

4. **Generate Report**:
   - Summarize all checks
   - List any issues
   - Provide next steps

5. **Suggest Actions**:
   - Remove unwanted files (manual instructions)
   - Update README, LICENSE if needed
   - Guide through git add, commit, push
   - Guide through GitHub template settings

**Important**: Template publishing is ultimately a human decision. Never auto-delete files or force-push. Only suggest and guide.

### Template Publishing Safety

**Never**:
- Auto-delete files without explicit user request
- Force-push to repository
- Commit secrets or sensitive data
- Modify core files without user approval

**Always**:
- Suggest manual review before publishing
- Provide clear instructions
- Respect user's final decision
- Log all suggested actions

---

## Sandbox & Experiment Commands

When operating as Meta-Orchestrator, you can help users understand and use the sandbox for experiments.

### Command: `sandbox status` or `show sandbox`

**Goal**: Show current sandbox configuration and status.

**Actions**:

1. **If `can_run_shell=true`**:
   - Run: `python3 auto_master.py sandbox_status`
   - Display sandbox status
   - Highlight if sandbox is enabled

2. **Else**:
   - Read `auto_config.json.sandbox`
   - Summarize sandbox configuration
   - Show which flags are enabled

3. **Output**:
   - Sandbox enabled/disabled status
   - Experimental flags status
   - Warnings if sandbox is enabled

### Command: `explain sandbox` or `what is sandbox`

**Goal**: Explain sandbox purpose and usage.

**Actions**:

1. **If `can_run_shell=true`**:
   - Run: `python3 auto_master.py sandbox_explain`
   - Display explanation

2. **Else**:
   - Read `prd.md` Section 25
   - Summarize sandbox purpose and usage
   - Explain safety guarantees

3. **Output**:
   - What sandbox is for
   - How to enable it
   - How to use it safely
   - Links to documentation

### Command: `propose experiment` or `suggest experiment`

**Goal**: Suggest experimental ideas to try.

**Actions**:

1. **Analyze Current System**:
   - Review current configuration
   - Identify potential improvements
   - Consider user's goals

2. **Generate Proposals**:
   - Suggest 1-3 small, well-scoped experiments
   - Examples:
     - "Try a different prompt pattern for PRD growth"
     - "Test a new AI routing rule for code generation"
     - "Prototype alternative chunk sizes for large PRDs"

3. **For Each Proposal**:
   - Name the experiment (e.g., "EXP-001: Alternative Chunking")
   - Describe expected benefit
   - List files it would touch
   - Assess risk level
   - Explain how to enable

4. **Output**:
   - List of proposed experiments
   - Benefits and risks
   - How to enable each one
   - Recommendation to start with lowest-risk experiment

**Important**: Only propose experiments. Never enable sandbox or experimental features without explicit user request.

### Command: `log experiment EXP-XXX`

**Goal**: Add an entry to the Sandbox Experiments Log.

**Actions**:

1. **Gather Information**:
   - Get current date/time
   - Extract experiment details from user command or context
   - Identify files touched
   - Determine result (if available)

2. **Generate Exp ID**:
   - If EXP-XXX provided, use it
   - Otherwise, find highest existing Exp ID in log
   - Increment to create new Exp ID (e.g., EXP-002, EXP-003)

3. **Format Entry**:
   - Create table row with all information
   - Format consistently with existing entries

4. **Update PRD**:
   - **If `can_edit_files=true`**:
     - Find Sandbox Experiments Log in Section 25.2
     - Append new row to table
     - Maintain table formatting
   - **Else**:
     - Show proposed table row
     - Explain where to add it manually

5. **Output**:
   - Confirmation of entry added
   - Exp ID assigned
   - Location in PRD

### Sandbox Safety Rules

**Never**:
- Enable sandbox features automatically
- Suggest enabling sandbox without explicit user request
- Run experimental features without user approval
- Hide experimental nature of features
- Modify core files in experimental code

**Always**:
- Require explicit enablement
- Clearly label experimental features
- Warn about experimental nature
- Suggest dry-run for experiments
- Log all experimental operations

**When User Requests Experiment**:
- Verify sandbox is enabled (or suggest enabling)
- Explain what will happen
- Suggest dry-run first
- Log the experiment
- Monitor for issues

---

## Onboarding Mode & DX Commands

When operating as Meta-Orchestrator, you should provide helpful onboarding and guidance, especially for first-time users.

### Onboarding Mode

**When to Activate**:
- If `.auto_state.json` does not exist or indicates a fresh setup
- If user asks "how do I start" or "what is this"
- If user seems confused about the system

**Onboarding Behavior**:

1. **Welcome Message**:
   - Acknowledge this is a PRD automation template
   - Explain that `prd.md` is the single master document
   - Mention that you can help automate PRD growth and implementation

2. **Quick Orientation**:
   - Point to `README.md` for quick start
   - Point to `prd.md` Section 0 for document overview
   - Point to `prd.md` Section 20 for detailed onboarding

3. **Available Commands**:
   - List key commands: `start`, `status`, `grow`, `plan_impl`, `implement phase X`
   - Explain that you can run these automatically
   - Offer to run `init` and `status` to get started

4. **Next Steps**:
   - Ask if user wants to describe their app idea
   - Offer to run the full `start` pipeline
   - Or guide them through manual setup

### DX Helper Commands

Support these simple commands to help users understand the system:

#### Command: `help` or `what can you do`

**Goal**: Explain what the Meta-Orchestrator can do.

**Actions**:
1. Summarize your capabilities:
   - Run automation commands (`start`, `grow`, `plan_impl`, etc.)
   - Interpret natural language commands
   - Help with debugging and troubleshooting
   - Generate code and documentation

2. List key commands you understand:
   - `start` - Full automation pipeline
   - `status` - Show system status
   - `grow` - Expand PRD
   - `plan implementation` - Generate implementation plan
   - `implement phase X.Y.Z` - Generate code for phase
   - `fix` - Diagnose and repair issues
   - And more (see Section 11 command mapping)

3. Point to documentation:
   - `README.md` for quick start
   - `prd.md` Section 0 for document overview
   - `prd.md` Section 20 for detailed workflows

#### Command: `explain this system` or `what is this`

**Goal**: Explain what this automation system is and how it works.

**Actions**:
1. **High-Level Explanation**:
   - This is a PRD automation template
   - `prd.md` is the single master document (specs + prompts + history)
   - The system can grow PRD from simple idea to detailed specifications
   - The system can generate implementation plans and code

2. **Key Concepts**:
   - Phase-based growth (work organized into phases)
   - Role-based enhancement (AI acts as expert personas)
   - Implementation tracks (code organized by track)
   - Automation safety (never deletes prd.md, state can be rebuilt)

3. **How It Works**:
   - You (Meta-Orchestrator) interpret user commands
   - You call `auto_master.py` commands
   - Commands process `prd.md` using AI or stubs
   - Progress is tracked in `.auto_state.json` and logs

4. **Point to Documentation**:
   - `prd.md` Section 0 for quick orientation
   - `prd.md` Section 20 for detailed explanation

#### Command: `how do I continue tomorrow` or `resume work`

**Goal**: Help user resume work on an existing project.

**Actions**:
1. **Check Current State**:
   - Run: `python3 auto_master.py doctor`
   - Run: `python3 auto_master.py status --verbose`
   - Summarize current state

2. **Review Progress**:
   - Read Section 10 (Progress Log) in `prd.md`
   - Summarize what's been done
   - Identify next steps

3. **Suggest Actions**:
   - If PRD needs more detail: Suggest `grow`
   - If ready to implement: Suggest `plan_impl` then `impl_phase`
   - If issues found: Suggest `fix` or troubleshooting

4. **Provide Context**:
   - Show recent activity from logs
   - Highlight any pending tasks from Section 9
   - Suggest relevant commands

#### Command: `what files are important`

**Goal**: Explain which files are critical and which can be modified.

**Actions**:
1. **Core Automation Files** (never delete, modify carefully):
   - `prd.md` - Single master document
   - `auto_master.py` - CLI orchestrator
   - `auto_config.json` - Configuration
   - `auto_master.sh` - Shell wrapper
   - `cursor_driver.scpt` - Cursor integration
   - `.gitignore`, `LICENSE`, `README.md` - Repo hygiene

2. **Runtime Files** (can be regenerated):
   - `.auto_state.json` - Automation state (rebuild with `init`)
   - `auto_master.log` - Operation logs

3. **Application Code** (project-specific):
   - Files in `src/`, `app/`, etc. (as configured)
   - Generated code in `generated_dir`
   - Tests in `test_dir`

4. **Point to Documentation**:
   - `prd.md` Section 13 (Governance) for file modification rules
   - `prd.md` Section 20.3 (FAQ) for common questions

### Error Message Guidance

When errors occur, provide helpful, actionable guidance:

**If `prd.md` is missing**:
- "ERROR: prd.md not found. This template requires a single master PRD file at repo root. Ensure you're in the correct directory."

**If `auto_config.json` is invalid**:
- "ERROR: Failed to parse auto_config.json. Please fix JSON syntax and re-run. You can validate with: `python -m json.tool auto_config.json`"

**If state is corrupted**:
- "ERROR: State file appears corrupted. Run `python3 auto_master.py init` to rebuild state from prd.md. This is safe and will not delete prd.md."

**If command is a stub**:
- "NOTE: [command] is currently a stub (not fully implemented). It is safe and reachable, but full functionality will be added later. See prd.md Section [relevant section] for details."

**If AI integration not working**:
- "NOTE: AI integration is not configured or not working. Commands will run in stub mode (logging only, no actual AI calls). To enable: set `use_cursor_driver: true` in auto_config.json (requires macOS + Cursor), or configure your AI integration method."

### Proactive Help

**When User Seems Stuck**:
- Offer to run `doctor` to diagnose
- Suggest checking `auto_master.log`
- Point to relevant section in `prd.md` Section 20

**When User Asks Vague Questions**:
- Clarify what they want to accomplish
- Offer specific commands or workflows
- Provide examples

**When Errors Occur**:
- Explain what went wrong in simple terms
- Suggest specific fixes
- Point to troubleshooting guide (Section 20.6)

---

**End of Meta-Orchestrator Instructions**

<!-- META_ORCHESTRATOR_PROMPT_END -->

---

## 10.2 Automation Health Notes

The automation system includes a built-in health check and diagnostics command (`doctor`) that monitors system health and can automatically detect and repair common issues.

### Doctor Command

Run `python3 auto_master.py doctor` to perform a comprehensive health check that examines:

- **Filesystem**: Verifies all required files exist and are readable
- **Configuration**: Validates config schema, types, and reasonable value ranges
- **State Consistency**: Checks that state file matches actual PRD file structure
- **Logs**: Analyzes recent log entries for error patterns and hot spots
- **Environment**: Verifies Python version, git availability, and macOS/osascript (if using Cursor)

### Severity Levels

- **OK**: No issues detected; system is healthy
- **WARN**: Minor issues or recommendations; system can continue operating
- **ERROR**: Critical issues detected; manual intervention may be required

### Auto-Fixes

When `safety.enable_doctor_auto_fixes=true` in `auto_config.json`, the doctor command can automatically:

- Rebuild corrupted or missing state files
- Convert "running" chunks back to "pending" (after crashes)
- Normalize config files with missing sections (if `safety.allow_config_autofix=true`)

Auto-fixes are conservative and safe; they never delete important files or force destructive operations.

### When to Use Doctor

- Before running long `grow` operations
- After system crashes or unexpected interruptions
- When encountering repeated errors
- As part of regular maintenance checks

---

<!--
END OF INITIAL SKELETON
========================
This document will be massively expanded by the automation system.
Each enhancement phase will add detail, clarity, and depth to the sections above.
-->

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.782185 -->
> [LOCAL-STUB] Phase P8.0009 (lines 960-972) – No Cursor driver. Echoing original chunk for testing.

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.732264 -->

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.738601 -->

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.745777 -->

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.752527 -->

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.759295 -->

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.766613 -->

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.773611 -->

<!-- Enhanced by automation system (fake mode) at 2025-11-19T22:40:40.783481 -->

---

# 12. EVALUATION, SMOKE TESTS & BENCHMARKS

This section defines how to evaluate the health, performance, and effectiveness of the automation system. Use these tools to verify your setup, measure performance, and ensure quality before running long unattended automation sessions.

<!-- EVAL_SECTION_START -->

## 12.1 Smoke Tests

Smoke tests provide quick verification that the automation system works end-to-end without modifying files.

### Purpose

Smoke tests verify:
- Core automation commands are accessible and functional
- Configuration is valid and complete
- State files are consistent
- AI integration (Cursor or local stub) is working
- No critical invariant violations exist

### Running Smoke Tests

**Automated**:
```bash
python3 auto_master.py smoke_test
```

**Manual Checklist** (if automated command not available):

1. **Doctor Check**: `python3 auto_master.py doctor` - Verify severity is OK or WARN
2. **Status Check**: `python3 auto_master.py status --verbose` - Verify state is loaded correctly
3. **Enhance Dry-Run**: `python3 auto_master.py enhance --dry-run --limit 1` - Verify dry-run mode works
4. **Grow Simulation**: Temporarily set `max_passes=1`, `max_chunks_per_pass=2`, run `grow`, verify no errors
5. **Implementation Plan Check**: `python3 auto_master.py plan_impl` - Verify plan generation works

### Success Criteria

✅ All smoke test checks pass
✅ No critical errors in logs
✅ State remains consistent
✅ No file corruption detected

### When to Run

- Before first use of the automation system
- After configuration changes
- After updating `auto_master.py` or core files
- Periodically to verify system health
- After system errors or crashes

---

## 12.2 Growth Benchmarks

Growth benchmarks measure PRD expansion performance and quality.

### Purpose

Benchmarks help you understand:
- How fast the PRD grows (lines per pass)
- Quality of enhancements (success rate, length ratios)
- Typical progression from small to large PRDs
- Performance characteristics of your setup

### Running Growth Benchmarks

**Automated**:
```bash
python3 auto_master.py benchmark_growth
```

**Expected Benchmarks**:
- Small PRD (1k → 10k lines): ~500-1,000 lines per pass
- Medium PRD (10k → 50k lines): ~300-800 lines per pass
- Large PRD (50k → 100k lines): ~200-500 lines per pass
- Success rate should be >80% (ideally >90%)
- Length ratio should stay >0.9 (90% of original length preserved)

---

## 12.3 Implementation Benchmarks

Implementation benchmarks test the code generation pipeline.

### Purpose

Verify that:
- Implementation planning works correctly
- Code generation prompts are effective
- Multi-file parsing works
- File path validation is correct
- Generated code structure is reasonable

### Running Implementation Benchmarks

**Automated**:
```bash
python3 auto_master.py benchmark_impl
```

**Success Criteria**:
✅ Implementation plan can be generated
✅ Prompts are built correctly with role context
✅ AI responses contain valid `<<<CODE_FILE_START>>>` markers
✅ File paths are validated and within allowed directories
✅ Generated code has proper structure and markers

---

## 12.4 Qualitative Evaluation

Beyond automated metrics, qualitative evaluation assesses the actual quality and usefulness of generated content.

### PRD Quality Assessment

**Clarity & Completeness**: Are requirements clear? Are all major sections covered? Is the level of detail appropriate?

**Consistency**: Do role-based enhancements align with their expertise? Are terminology and concepts used consistently?

**Usefulness**: Can the PRD guide actual implementation? Are implementation mappings clear?

### Code Quality Assessment

**Structure**: Is code organized logically? Are files in appropriate directories?

**Readability**: Is code well-commented? Are naming conventions followed?

**Completeness**: Are imports and dependencies included? Is error handling present?

---

## 12.5 Meta-Improvement & Evolution

This automation system can improve itself through a structured meta-improvement process.

### Meta-Improvement Process

1. **Identify Improvement Opportunity**: Something fails or behaves suboptimally
2. **Document the Issue**: Capture in "Automation Evolution Log"
3. **Design the Improvement**: Propose change, ensure backward compatibility
4. **Implement in Dedicated Phase**: Use special Phase prefix: `AUTO-IMPROVE-X.Y`
5. **Validate**: Run `smoke_test` and benchmarks
6. **Document**: Update Evolution Log and relevant sections

### Automation Evolution Log Template

| Phase ID | Date | Improvement | Rationale | Status |
|----------|------|-------------|-----------|--------|
| AUTO-IMPROVE-1.1 | 2025-XX-XX | Added smoke_test command | Need quick verification | ✅ Complete |

**Legend**: ✅ Complete | 🔄 In Progress | 📋 Planned | ❌ Rejected

### Guidelines for Meta-Improvements

- **Small & Incremental**: Make one focused change at a time
- **Backward Compatible**: Don't break existing configs
- **Well-Tested**: Always run smoke tests and benchmarks
- **Well-Documented**: Update `prd.md` sections and Evolution Log

<!-- EVAL_SECTION_END -->

---

# 13. OPEN-SOURCE GOVERNANCE & CONTRIBUTION GUIDE

This section defines how this automation system is governed, versioned, extended, and contributed to. It establishes clear boundaries between the stable core and user extensions, ensuring the system remains reliable and maintainable as an open-source template.

<!-- GOVERNANCE_SECTION_START -->

## 13.1 Core vs Extension Zones (Architecture of Responsibility)

This system is organized into distinct layers with different rules for modification and contribution.

### CORE AUTOMATION LAYER

**Files**: `auto_master.py`, `auto_config.json`, `cursor_driver.scpt`, `auto_master.sh`, `.auto_state.json` (runtime), `auto_master.log` (runtime)

**Rules**:
- Changes to these files affect **all users** of the template
- Must maintain backward compatibility where possible
- Breaking changes require MAJOR version bump
- All changes must pass `smoke_test` and relevant benchmarks

### CORE SPEC LAYER

**Content in `prd.md`**: Omni-Corp Role Library, Prompt Library, Phase & Task Framework, Meta-Orchestrator Instructions, Evaluation & Benchmarks, Governance section

**Rules**:
- Changes here affect how AI agents behave for **all** projects using this template
- Breaking changes to Meta-Orchestrator instructions require MAJOR version bump
- New roles, prompts, or templates can be added as MINOR version features

### PROJECT-SPECIFIC LAYER

**Content**: Project-specific PRD content, application code under `project_root`

**Rules**:
- Users can change these freely without affecting the template
- Not subject to template versioning
- Can be customized for any project type

### EXTENSION LAYER

**Optional User-Defined**: Additional Python scripts, extra documentation, custom build scripts, project-specific automation helpers

**Rules**:
- Must not modify or override core behaviors unless clearly opt-in
- Should be documented in `prd.md` under "Extensions" subsection
- Can be shared as examples but are not part of the core template

---

## 13.2 Versioning & Release Semantics

This template uses **Semantic Versioning** (SemVer): **MAJOR.MINOR.PATCH**

- **MAJOR** (X.0.0): Breaking changes to core automation or spec
- **MINOR** (X.Y.0): New features, backwards compatible
- **PATCH** (X.Y.Z): Bug fixes, internal improvements

### Version Storage

**In `auto_master.py`**:
```python
TEMPLATE_VERSION = "1.0.0"
```

**In `prd.md`**: Recorded in "Template Version & Changelog" subsection

**In `auto_config.json`** (optional):
```json
{
  "_template_version": "1.0.0",
  "_template_compatible_from": "1.0.0"
}
```

### Template Versioning

Template-wide changes should bump `TEMPLATE_VERSION` in `auto_master.py`:
- **MAJOR**: Breaking changes (incompatible API or behavior changes)
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

Release tags in GitHub should match the version (e.g., `v1.0.0-template`).

For detailed template versioning information, see Section 24.4 (Template Versioning).

### Release Process

1. **Pre-Release Validation**: Run `smoke_test`, `benchmark_growth`, `benchmark_impl`, `template_check`
2. **Version Update**: Update `TEMPLATE_VERSION` in `auto_master.py` and changelog in `prd.md`
3. **Changelog Entry**: Add entry with version, date, changes (grouped by MAJOR/MINOR/PATCH)
4. **Git Tagging**: `git tag -a v1.0.0-template -m "Release v1.0.0"`
5. **Release Notes**: Create GitHub release with summary and migration notes

### Template Version & Changelog

| Version | Date | Type | Changes |
|---------|------|------|---------|
| 1.0.0 | 2025-XX-XX | Initial | Initial stable release with full automation pipeline |

**Current Version**: 1.0.0

---

## 13.3 Contribution Workflow & Guidelines

### How to Contribute

1. **Fork the Repository**: Create your own fork and clone locally
2. **Create a Feature Branch**: `git checkout -b feature/your-feature-name`
3. **Make Changes**: Core changes, spec changes, documentation, or extensions
4. **Test Your Changes**: Run `smoke_test`, `benchmark_growth`, `benchmark_impl`
5. **Update Documentation**: Update relevant sections in `prd.md` and `README.md`
6. **Submit a Pull Request**: Include description, impact, testing, and type

### Review Guidelines

**What Gets Reviewed**:
- ✅ All changes to core commands
- ✅ Config schema changes
- ✅ Meta-Orchestrator instruction changes
- ✅ New roles, prompts, or templates
- ✅ Breaking changes (MAJOR version)

**Review Criteria**:
- Backward Compatibility: Does this break existing configs or workflows?
- Safety: Does this maintain safety guarantees?
- Testing: Have appropriate tests been run?
- Documentation: Is the change documented?
- Clarity: Is the code/change clear and maintainable?

**Encouraged Practices**:
- ✅ Small, atomic PRs (one feature or fix per PR)
- ✅ Clear commit messages
- ✅ Tests for core changes
- ✅ Documentation updates

**Discouraged Practices**:
- ❌ Large, multi-feature PRs
- ❌ Breaking changes without migration notes
- ❌ Changes that reduce safety or universality
- ❌ Project-specific code in core files

### Extension Contributions

**Contributing Extensions**:
- Useful extensions can be shared as examples
- Consider contributing to template if extension is generally useful
- Follow extension patterns (Section 21.3)
- Document in Section 21

**Contributing Core Features**:
- Core features must be template-wide and universally useful
- Follow contribution workflow (Section 13.3)
- Ensure backward compatibility
- Update version and changelog

---

## 13.4 Extensions & Customization Patterns

### Custom Roles

**Pattern**: Add new roles under a separate subsection in `prd.md` (e.g., "Project-Specific Roles")

**Guidelines**:
- ✅ Add to project-specific section
- ✅ Follow existing role template structure
- ✅ Document clearly
- ❌ Don't modify core role library structure

### Custom Prompts

**Pattern**: Add project-specific prompts under "Project-Specific Prompt Library" (Section 8.X)

**Guidelines**:
- ✅ Add to project-specific section
- ✅ Reference project-specific roles if needed
- ✅ Keep core templates intact

### Custom Implementation Logic

**Pattern**: Create separate scripts in `tools/` or `scripts/` directory, use `auto_master.py` as a library or call it via CLI

**Guidelines**:
- ✅ Create separate files/directories
- ✅ Use `auto_master.py` CLI or import as library
- ✅ Document your extensions
- ❌ Don't modify `auto_master.py` for project-specific needs

### Custom Profiles

**Pattern**: Extend `profiles.profiles` in `auto_config.json`, document new profiles in `prd.md`

**Guidelines**:
- ✅ Add to `auto_config.json` `profiles.profiles`
- ✅ Document in `prd.md`
- ✅ Use descriptive names
- ❌ Don't remove or rename existing profiles

<!-- GOVERNANCE_SECTION_END -->

---

# 14. APP FACTORY MODE & MULTI-PROJECT USAGE

This section describes how to use this template as an "App Factory" to manage multiple independent projects, each with its own repository and PRD automation.

<!-- APP_FACTORY_SECTION_START -->

## 14.1 App Factory Concept

**App Factory Pattern**: A pattern where one developer or team can spin up many independent projects (each with its own repo and PRD automation), using this template.

**Key Principles**:
- Each app or system lives in its own repo using this template
- One template → many derived repos
- Each derived repo has: its own `prd.md`, `auto_master.py`, `auto_config.json`, `.auto_state.json`, `auto_master.log`, git history and remote
- Master Controller exists *outside* this repo (AI agent, human + scripts, CI pipeline)

## 14.2 Standard Multi-Project Workflows

### Workflow 1: Create a New App Project from Template

1. Create new repo from template (GitHub "Use this template" or `git clone` & `git remote`)
2. Set repo name (e.g., `xyz-app`)
3. In new repo: Open `prd.md`, insert app description, run `python3 auto_master.py init`, `sync_roles`, `grow`
4. Summarize: Where the new repo is, how to continue work

### Workflow 2: Maintain N Projects in Parallel

1. Maintain list of active project repos (paths or remote URLs)
2. For each project: `cd` into repo, run `doctor`, `status --verbose`, optionally `grow`
3. When user requests "regrow all PRDs": Loop over each repo and run `grow`
4. When user requests "implement top tasks on project X": Focus on project X, run `plan_impl` / `impl_loop`

### Workflow 3: Archive / Freeze a Project

1. Run final `doctor`, `status`, `git_status`
2. Tag a release (e.g., `v1.0.0-app-X`)
3. Mark in `prd.md` a "Project Completed / Archived" note
4. Master Controller can keep repo listed as "archived" but not run `grow` or `impl_loop` on it

## 14.3 Conventions for Naming & Paths

**Repo Naming**: Template repo (e.g., `prd-auto-template`), Project repos (e.g., `app-<project-name>`, `game-<project-name>`)

**Directory Layout**: One app per repo; app source code lives under `project_root` (as configured in `auto_config.json`)

**Config Customization**: After creating new repo, edit `auto_config.json`: `master_md_path`, `implementation` settings, `profiles.default_profile`

## 14.4 Master Control Pattern

**Master Controller** is an external entity (AI agent, human, CI pipeline) that:
- Creates new repos from template
- Applies Meta-Orchestrator Start Prompt to each repo
- Runs `start` for each project
- Monitors health across multiple projects (via `doctor`, `status`)

**Important**: Master Controller exists *outside* this repo, not as code in this repo.

## 14.5 Template Upgrade / Migration Across Many Projects

**Template Upgrade Playbook**:
1. For each project repo: Create branch `template-upgrade-v1.1.0`
2. Compare: `auto_master.py`, `auto_config.json`, `cursor_driver.scpt`, `.gitignore`, `LICENSE`, `README.md`
3. Merge or reapply template changes carefully (use diff tools, avoid overwriting project-specific config)
4. Run: `doctor`, `smoke_test`, `benchmark_*`
5. If everything passes, merge branch into main and tag release

**Note**: `prd.md` is part core, part project-specific. Keep core sections aligned with latest template, keep project-specific sections intact.

<!-- APP_FACTORY_SECTION_END -->

---

# 15. DOMAIN PACKS & PRESETS

This section describes Domain Packs and Presets – reusable bundles of roles, prompts, phase patterns, and implementation hints tailored to different kinds of projects.

<!-- DOMAIN_PACKS_SECTION_START -->

## 15.1 What Are Domain Packs?

A **Domain Pack** is a predefined bundle of:
- **Recommended Roles**: Subset of Omni-Corp roles best suited for this domain
- **Suggested Tech Stack**: Languages, frameworks, and tools commonly used
- **Phase Patterns**: Common phase patterns and task structures
- **Implementation Tracks**: Prioritized implementation tracks (Client, Backend, AI, etc.)

**Important**: Domain Packs are **guidance, not strict constraints**. You can override any pack suggestion, mix and match elements, create custom packs, or change stack/roles at any time.

## 15.2 Available Domain Packs

The following Domain Packs are available in `auto_config.json`:

### generic_app
**Best For**: General-purpose apps when domain is unclear. **Primary Target**: Multi-platform. **Suggested Stack**: React Native/Flutter (mobile), React/Next.js (web), Node.js/Python (backend)

### mobile_app
**Best For**: Mobile-first apps (iOS/Android). **Primary Target**: Mobile. **Suggested Stack**: React Native or Flutter. **Phase Patterns**: MVP_CORE, AUTH, PUSH_NOTIFICATIONS, OFFLINE_MODE

### web_app
**Best For**: Web-first apps or SaaS dashboards. **Primary Target**: Web. **Suggested Stack**: Next.js or React. **Phase Patterns**: MVP_CORE, AUTH, ANALYTICS, BILLING, SEO

### game_2d
**Best For**: 2D games with core loop, levels, monetization. **Primary Target**: Game. **Suggested Stack**: Unity or Godot. **Phase Patterns**: CORE_LOOP, LEVELS, UI, MONETIZATION

### ai_tool
**Best For**: AI-powered assistant, generator, or automation tool. **Primary Target**: AI Tool. **Suggested Stack**: Python/FastAPI or Node.js. **Phase Patterns**: MVP_CORE, AI_INTEGRATION, SAFETY_GUARDS, LOGGING

### backend_service
**Best For**: Backend API service or microservice. **Primary Target**: Backend. **Suggested Stack**: Python/FastAPI, Node.js/Express, or Go. **Phase Patterns**: MVP_CORE, API_DESIGN, AUTH, DATABASE

### data_app
**Best For**: Data analysis, visualization, or business intelligence. **Primary Target**: Multi-platform. **Suggested Stack**: React/Next.js or Python/Dash. **Phase Patterns**: MVP_CORE, DATA_INGESTION, ANALYTICS, VISUALIZATION

## 15.3 Domain Pack Template

To create a custom Domain Pack:
- **Pack ID**: [e.g., "ecommerce_web"]
- **Description**: [what kind of projects this suits]
- **Primary Target Type**: [mobile/web/game/backend/ai_tool/multi]
- **Suggested Roles**: [subset of Omni-Corp roles]
- **Suggested Stack**: [languages, frameworks, engines]
- **Default Phase Patterns**: [labels like MVP_CORE, AUTH, CHECKOUT]
- **Default Implementation Tracks**: [Client, Backend, Data, AI, Infra]

## 15.4 Presets (Domain + Stack + Style)

A **Preset** combines: Domain Pack + Implementation settings + Style tags

**Example Presets**:
- `mobile_todo_react_native`: Domain Pack `mobile_app`, React Native + TypeScript, style tags: ["offline_friendly", "minimal_ui"]
- `web_saas_dashboard_nextjs`: Domain Pack `web_app`, Next.js + TypeScript, style tags: ["multi_tenant", "metrics_first", "b2b"]

## 15.5 Using Domain Packs

**Automatic Selection**: When you describe your app to Meta-Orchestrator and type `start`, it will:
1. Parse your description for domain keywords
2. Match to a Domain Pack
3. Apply pack defaults (set `domain_packs.default_pack`, configure `implementation.*`)
4. Respect your overrides (if you specify framework, use that instead)

**Manual Selection**: Edit `auto_config.json` and set `domain_packs.default_pack = "mobile_app"` or tell the AI agent

<!-- DOMAIN_PACKS_SECTION_END -->

---

# 16. DEPLOYMENT, ENVIRONMENTS & RUNTIME MONITORING

This section describes how to configure and use deployment, environment management, and runtime monitoring as part of the full application lifecycle.

<!-- DEPLOYMENT_SECTION_START -->

## 16.1 High-Level Deployment Model

This template provides a **generic deployment model** that can be adapted to any cloud provider, CI/CD system, or deployment platform.

**Core Principles**:
- **Cloud/Platform Neutral**: No hard dependencies on specific providers
- **CI/CD Agnostic**: Works with GitHub Actions, GitLab CI, CircleCI, or custom scripts
- **Safety First**: No destructive actions by default, requires explicit approval for production
- **Hook-Based**: Defines commands and templates that external systems can execute

### Environment Types

**Local**: Developer's machine, rapid iteration, no remote deployment

**Preview**: Per-branch or per-PR builds, temporary, manual QA

**Staging**: Shared pre-production environment, near-real production setup, requires approval

**Production**: Real users and real data, highest reliability requirements, requires approval and monitoring

## 16.2 Deployment Hooks

Deployment hooks are generic commands defined in `auto_config.json`:

- **build_command**: Command to build/compile (e.g., `npm run build`)
- **test_command**: Command to run tests (e.g., `npm test`)
- **lint_command**: Command to run linters (e.g., `npm run lint`)
- **deploy_command_template**: Template for deploy command (use `{env}` placeholder)
- **rollback_command_template**: Template for rollback command (optional)
- **health_check_command**: Command to verify deployment health (optional)

## 16.3 Monitoring & Feedback

**Monitoring Configuration**:
- **Log Sources**: `auto_master.log`, application logs, CI/CD logs
- **Alert Policy**: `manual_review`, `basic_thresholds`, or `external_system`
- **Basic Thresholds**: `max_error_rate_percent`, `max_failed_deploys`, `min_deploy_interval_minutes`

**Monitoring Workflow**:
1. Collect logs from configured sources
2. Analyze error patterns and calculate error rates
3. Compare against thresholds and generate alerts if needed
4. Report human-readable summary with recommendations

## 16.4 Deployment Best Practices

**Pre-Deployment Checklist**:
- [ ] Run `python3 auto_master.py doctor`
- [ ] Run `python3 auto_master.py smoke_test`
- [ ] Review git changes
- [ ] Run tests and linters locally
- [ ] Test build locally
- [ ] Review deployment plan (dry-run)

**Deployment Process**:
1. Prepare: Ensure all tests pass, review changes, get approvals
2. Build: Execute `build_command`
3. Test: Execute `test_command`
4. Deploy: Execute `deploy_command_template` with environment
5. Verify: Execute `health_check_command` if available
6. Monitor: Watch logs for errors, be ready to rollback

## 16.5 CI/CD Integration

This template is designed to work with any CI/CD system. CI/CD systems can:
- Read hooks from `auto_config.json`
- Execute hooks as part of pipeline
- Substitute environment variables and secrets
- Report results

**Example**: GitHub Actions can read `deployment.deploy_hooks.build_command` from `auto_config.json` and execute it in workflow.

## 16.6 Cloud Provider Adaptation

The deployment model is cloud/provider neutral. Adapt `deploy_command_template` for your provider:
- **AWS**: S3 sync, CloudFront, ECS, etc.
- **GCP**: App Engine, Cloud Run, GKE, etc.
- **Azure**: App Service, Container Instances, AKS, etc.
- **Vercel/Netlify**: Platform-specific CLI commands
- **Mobile Stores**: Fastlane, app store APIs

<!-- DEPLOYMENT_SECTION_END -->

---

# 17. SECURITY, PRIVACY, COMPLIANCE & TESTING

This section establishes security, privacy, compliance, and testing foundations for the application.

<!-- SECURITY_SECTION_START -->

## 17.1 Security Architecture Overview

**Security Principles**:
- **Least Privilege**: Users and systems should have only minimum permissions necessary
- **Defense in Depth**: Multiple layers of security controls
- **Secure Defaults**: Default configurations should be secure
- **Security by Design**: Consider security in architecture decisions
- **Privacy by Design**: Minimize data collection, encrypt sensitive data

### Security Checklist Template

**Authentication & Authorization**: [ ] Authentication required for sensitive actions, [ ] Strong password policy, [ ] Role-based authorization defined

**Input Validation & Output Encoding**: [ ] All inputs validated and sanitized, [ ] SQL injection prevention, [ ] XSS prevention

**Rate Limiting & Abuse Prevention**: [ ] Rate limiting on endpoints, [ ] Account lockout after failed attempts

**Secure Storage**: [ ] Secrets in secure locations, [ ] No secrets in code/logs, [ ] Passwords hashed with strong algorithms

**Transport Security**: [ ] HTTPS enforced in production, [ ] TLS 1.2+ required

**Logging & Monitoring**: [ ] Security events logged, [ ] No sensitive data in logs

## 17.2 Privacy & Data Classification

### Data Classification Levels

- **Public**: Information intended for public consumption
- **Internal**: Information for internal use only
- **Sensitive**: Information that could cause harm if exposed (email, phone, location, payment)
- **Restricted**: Highly sensitive information requiring strict controls (passwords, health records, financial account numbers)

### Data Classification Template

For each data type, document:
- **Classification Level**: [public/internal/sensitive/restricted]
- **Storage Location(s)**: [Database tables, third-party services]
- **Retention Period**: [Days/months/years]
- **Access Roles**: [Which roles/systems can access]
- **Encryption**: [At rest: yes/no, In transit: yes/no]

### Privacy Principles

- **Data Minimization**: Collect only data necessary
- **Purpose Limitation**: Use data only for stated purpose
- **Storage Limitation**: Retain data only as long as necessary
- **Accuracy**: Keep data accurate and up to date
- **Security**: Protect data with appropriate measures
- **Transparency**: Inform users about data collection and use

## 17.3 Compliance & Legal Considerations

### Common Compliance Regimes

- **GDPR**: EU users, consent, data subject rights, breach notification
- **CCPA**: California residents, disclosure, opt-out rights
- **HIPAA**: Healthcare data, PHI safeguards
- **PCI DSS**: Credit card data, secure cardholder environment
- **COPPA**: Children's data, parental consent
- **App Store Policies**: Privacy policy, data use disclosure

### Compliance Checklist

- [ ] Identify target user jurisdictions
- [ ] Identify applicable compliance regimes
- [ ] Privacy policy exists and is accessible
- [ ] Data subject rights handling process defined
- [ ] Data retention and deletion policies implemented
- [ ] Third-party data sharing documented

**Legal Disclaimer**: This section provides general guidance and checklists. It is not legal advice. Consult qualified legal counsel for compliance matters.

## 17.4 Testing Strategy

### Testing Levels

- **Unit Tests**: Fast, isolated tests for individual components (70%+ coverage target)
- **Integration Tests**: Tests for component interactions and APIs
- **End-to-End Tests**: Complete user workflow tests
- **Security Tests**: Static analysis, dependency scanning, DAST, penetration testing
- **Performance Tests**: Load testing, stress testing, benchmarking

### Testing Strategy Template

Document your testing approach:
- **Unit Tests**: Framework, scope, coverage target, command, frequency
- **Integration Tests**: Framework, scope, command, frequency
- **End-to-End Tests**: Framework, scope, command, frequency
- **Security Tests**: Tools, frequency
- **Performance Tests**: Tool, scenarios, metrics, frequency

## 17.5 Incident Response & Evolution

### Incident Response Process

1. **Detection**: Monitor logs, use automated alerts
2. **Assessment**: Determine scope and severity
3. **Containment**: Isolate affected systems
4. **Eradication**: Remove malware or backdoors
5. **Recovery**: Restore systems from backups
6. **Post-Incident**: Document, conduct post-mortem, implement improvements

### Incident Documentation Template

When recording incidents:
- **Date/Time**: When did it occur?
- **Severity**: [Low/Medium/High/Critical]
- **Type**: [Data breach, DDoS, unauthorized access, etc.]
- **Affected Systems**: Which systems were impacted?
- **Response**: Immediate actions taken
- **Root Cause**: What caused the incident?
- **Remediation**: Immediate fixes and long-term improvements

<!-- SECURITY_SECTION_END -->

# 18. PERFORMANCE, COST & RESOURCE OPTIMIZATION

This section provides guidance on optimizing performance and managing costs for both the automation system itself and the applications it generates.

<!-- PERFORMANCE_SECTION_START -->

## 18.1 Automation Performance & AI Usage

The automation system's performance is primarily determined by AI API calls, chunk processing, and growth passes. Understanding and tuning these factors helps balance speed, cost, and quality.

### Key Performance Factors

**Chunk Size**:
- **Smaller chunks** (50-100 lines):
  - Faster per-chunk processing
  - More AI calls (higher cost)
  - Better error isolation
  - More granular progress tracking

- **Larger chunks** (200-400 lines):
  - Fewer AI calls (lower cost)
  - More context per call (potentially better quality)
  - Slower per-chunk processing
  - Larger failure impact

**Number of Passes**:
- Each `grow` pass processes multiple chunks
- More passes = more total processing time
- More passes = more AI calls = higher cost
- Balance between thoroughness and efficiency

**AI Token Usage**:
- Each AI call consumes tokens (input + output)
- Token usage directly correlates with cost
- Larger chunks = more tokens per call
- More calls = more total tokens

### Configuration Tuning

**In `auto_config.json.performance`**:

```json
{
  "ai_usage": {
    "max_tokens_per_call": 8000,
    "max_calls_per_run": 200,
    "soft_budget_tokens_per_day": 500000,
    "enforce_limits": false
  },
  "chunking_tuning": {
    "min_chunk_lines": 50,
    "max_chunk_lines": 400,
    "adaptive_chunking": true,
    "target_latency_seconds_per_chunk": 30
  },
  "growth_tuning": {
    "max_passes_per_run": 3,
    "max_chunks_per_pass": 10,
    "min_growth_ratio": 0.95,
    "max_growth_ratio": 1.5
  }
}
```

**Tuning Guidelines**:

- **For Speed**: Increase `max_chunk_lines`, increase `max_chunks_per_pass`, increase `max_passes_per_run`
- **For Cost**: Decrease `max_tokens_per_call`, decrease `max_calls_per_run`, prefer larger chunks
- **For Quality**: Use moderate chunk sizes (120-200 lines), allow more passes, use adaptive chunking
- **For Safety**: Use smaller chunks, lower `max_passes_per_run`, enable `enforce_limits`

### Automation Performance Checklist

Use this checklist to ensure optimal automation performance:

- [ ] Chunk sizes tuned appropriately (not too tiny, not too huge)
- [ ] Growth passes limited to avoid runaway runs
- [ ] AI token and call budgets configured in `auto_config.json`
- [ ] Long-running commands (`grow`, `impl_loop`) monitored and logged
- [ ] Expensive operations done in smaller batches where possible
- [ ] Adaptive chunking enabled if latency varies significantly
- [ ] Performance metrics logged for analysis

### Performance Monitoring

**Track in `auto_master.log`**:
- Chunk processing times
- AI call counts and token usage (if available)
- Growth pass durations
- Implementation phase durations

**Use `perf_status` command**:
```bash
python3 auto_master.py perf_status
```

This command summarizes:
- Current performance configuration
- Recent usage patterns (if logged)
- Budget status
- Recommendations

---

## 18.2 Application Performance (Runtime)

Beyond automation performance, the applications generated by this system must also be performant. This section provides guidance for optimizing runtime performance across different application types.

### Mobile Apps

**Performance Goals**:
- **Frame Rate**: 60fps for critical UI, 30fps minimum for non-critical
- **App Launch**: < 2 seconds cold start, < 0.5 seconds warm start
- **Network**: Batch API calls, minimize round trips
- **Memory**: Monitor memory usage, avoid leaks

**Optimization Strategies**:
- **Caching**: Local storage for frequently accessed data
- **Lazy Loading**: Load content on demand, not all at once
- **Image Optimization**: Compress images, use appropriate formats
- **Code Splitting**: Load only necessary code modules
- **Background Processing**: Offload heavy work to background threads

**Common Bottlenecks**:
- Over-fetching data from APIs
- Rendering large lists without virtualization
- Synchronous operations on main thread
- Unoptimized images and assets
- Excessive re-renders

### Web Apps

**Performance Goals**:
- **Core Web Vitals**:
  - Largest Contentful Paint (LCP): < 2.5s
  - First Input Delay (FID): < 100ms
  - Cumulative Layout Shift (CLS): < 0.1
- **Time to Interactive (TTI)**: < 3.5s
- **First Contentful Paint (FCP)**: < 1.8s

**Optimization Strategies**:
- **CDN Usage**: Serve static assets from CDN
- **Caching**: Browser caching, service worker caching, CDN caching
- **Code Splitting**: Route-based and component-based splitting
- **Image Optimization**: WebP format, lazy loading, responsive images
- **SSR vs CSR**: Choose based on SEO and performance needs
- **Bundle Optimization**: Tree shaking, minification, compression

**Common Bottlenecks**:
- Large JavaScript bundles
- Unoptimized images and fonts
- Render-blocking resources
- Excessive API calls
- Poor caching strategies

### Backend Services & APIs

**Performance Goals**:
- **API Latency**: < 200ms for simple endpoints, < 500ms for complex
- **Throughput**: Handle expected load with headroom
- **Database Queries**: < 100ms for simple queries, < 500ms for complex
- **Cold Start**: < 1s for serverless functions

**Optimization Strategies**:
- **Caching**: Redis/Memcached for frequently accessed data
- **Database Optimization**: Indexes, query optimization, connection pooling
- **Rate Limiting**: Prevent abuse and ensure fair resource usage
- **Async Processing**: Offload long-running tasks to queues
- **Horizontal Scaling**: Scale out rather than up when possible

**Common Bottlenecks**:
- N+1 query problems
- Missing database indexes
- Synchronous blocking operations
- Inefficient serialization
- Lack of caching

### AI Tools & LLM Applications

**Performance Goals**:
- **Response Time**: < 2s for simple queries, < 10s for complex
- **Token Usage**: Minimize context length while maintaining quality
- **Cost**: Optimize for cost per request

**Optimization Strategies**:
- **Context Management**: Trim or summarize long contexts
- **Response Caching**: Cache common queries and responses
- **Streaming**: Stream responses for better perceived performance
- **Batching**: Batch multiple requests when possible
- **Model Selection**: Choose appropriate model size for task

**Common Bottlenecks**:
- Excessive context length
- No response caching
- Synchronous processing
- Inefficient prompt engineering
- No rate limiting

### Application Performance Template

Document your application's performance goals and strategies:

```markdown
#### Application Performance: [Project Name]

**Performance Goals:**
- Target response time: [e.g., 200ms for main endpoints]
- Target frame rate: [e.g., 60fps for critical UI]
- Max acceptable cold-start time: [e.g., 1s]
- Target throughput: [e.g., 1000 requests/second]

**Bottleneck Risks:**
- [e.g., heavy DB queries, over-fetching, network latency, large LLM contexts]
- [e.g., unoptimized images, large bundles, synchronous operations]

**Optimization Strategies:**
- **Caching:**
  - [memory cache / CDN / local storage / Redis]
  - [cache invalidation strategy]

- **Data Loading & Pagination:**
  - [lazy loading / infinite scroll / chunked queries]
  - [prefetching strategy]

- **AI Calls:**
  - [summarization / trimming context / reuse partial results]
  - [response caching / streaming]

- **Code Optimization:**
  - [code splitting / tree shaking / minification]
  - [bundle size targets]

**Monitoring:**
- [performance metrics to track]
- [alerting thresholds]
- [tools used for monitoring]
```

---

## 18.3 Cost Awareness & Budgeting

Understanding and managing costs is crucial for sustainable automation and application operation. This section provides frameworks for cost awareness without vendor lock-in.

### AI Usage Costs

**Token-Based Pricing**:
- Most AI APIs charge per token (input + output)
- Typical costs: $0.01-0.03 per 1K tokens (varies by model)
- Large contexts and long outputs increase costs

**Cost Estimation**:
- Track token usage in `auto_master.log` (if available)
- Estimate based on chunk sizes and number of calls
- Use `cost_per_1k_tokens_usd` in config for rough estimates

**Cost Optimization**:
- Use larger chunks to reduce call count
- Trim context when possible
- Cache and reuse AI responses
- Use smaller models when appropriate
- Batch operations to reduce overhead

### Infrastructure Costs

**Compute Costs**:
- Serverless: Pay per invocation and duration
- Containers/VMs: Pay per instance and uptime
- Edge functions: Pay per request

**Database Costs**:
- Storage: Pay per GB stored
- Operations: Pay per read/write (some providers)
- Connections: Pay per connection pool

**Storage & CDN Costs**:
- Object storage: Pay per GB stored and transferred
- CDN: Pay per GB transferred
- Bandwidth: Pay per GB outbound

**Cost Optimization Strategies**:
- Right-size resources (don't over-provision)
- Use auto-scaling to match demand
- Implement caching to reduce compute and database load
- Use CDN for static assets
- Optimize database queries to reduce operations
- Consider reserved instances for predictable workloads

### Cost Awareness Template

Document your cost assumptions and optimization opportunities:

```markdown
#### Cost Awareness: [Project Name]

**AI Cost Assumptions:**
- Cost per 1K tokens: [approx USD, e.g., 0.02]
- Typical tokens per run: [rough estimate, e.g., 50,000]
- Monthly AI budget: [USD or other currency, e.g., 100]

**Infra Cost Assumptions:**
- Hosting: [cloud tier, approximate monthly, e.g., "AWS t3.small, ~$15/month"]
- Database: [tier & usage assumptions, e.g., "PostgreSQL db.t3.micro, ~$12/month"]
- Storage / CDN: [rough estimate, e.g., "S3 + CloudFront, ~$5/month"]
- Total estimated monthly: [USD, e.g., 32]

**Optimization Opportunities:**
- [e.g., cache popular AI responses, reduce context length, off-peak batch jobs]
- [e.g., use CDN for static assets, implement database query caching]
- [e.g., right-size compute resources, use auto-scaling]

**Cost Monitoring:**
- [how to track costs: cloud provider dashboards, custom logging, etc.]
- [alerting thresholds: e.g., "alert if monthly cost exceeds $50"]
```

### Budget Management

**Setting Budgets**:
- Define soft budgets in `auto_config.json.performance.ai_usage.soft_budget_tokens_per_day`
- Set `enforce_limits: true` for hard stops (use with caution)
- Monitor actual usage vs. budgets

**Cost Alerts**:
- Log warnings when approaching budget limits
- Alert on unexpected cost spikes
- Review cost trends regularly

---

## 18.4 Build, Test & Deploy Performance

Build, test, and deployment performance affects developer productivity and CI/CD efficiency. This section connects to the Deployment section (Section 16) and provides performance considerations.

### Build Performance

**Build Time Targets**:
- **Small projects**: < 30 seconds
- **Medium projects**: < 2 minutes
- **Large projects**: < 5 minutes

**Optimization Strategies**:
- **Incremental Builds**: Only rebuild changed modules
- **Parallel Builds**: Build multiple modules in parallel
- **Caching**: Cache dependencies and build artifacts
- **Dependency Optimization**: Minimize dependencies, use tree shaking
- **Build Tools**: Choose fast build tools (e.g., Vite, esbuild, Turbopack)

**Configuration**:
```json
{
  "performance": {
    "build_runtime": {
      "build_timeout_seconds": 900,
      "monitor_build_time": true,
      "warn_if_build_slow": true,
      "slow_build_threshold_seconds": 300
    }
  }
}
```

### Test Performance

**Test Time Targets**:
- **Unit tests**: < 10 seconds for full suite
- **Integration tests**: < 2 minutes for full suite
- **E2E tests**: < 5 minutes for critical paths

**Optimization Strategies**:
- **Parallel Execution**: Run tests in parallel
- **Test Selection**: Run only relevant tests (changed files, affected tests)
- **Test Sharding**: Split test suite across multiple runners
- **Mocking**: Mock external services to avoid network delays
- **Test Data**: Use minimal test data, generate on demand

**Configuration**:
```json
{
  "performance": {
    "build_runtime": {
      "test_timeout_seconds": 600,
      "monitor_build_time": true
    }
  }
}
```

### Deployment Performance

**Deployment Time Targets**:
- **Preview deployments**: < 2 minutes
- **Staging deployments**: < 5 minutes
- **Production deployments**: < 10 minutes (including verification)

**Optimization Strategies**:
- **Incremental Deployments**: Deploy only changed files
- **Blue-Green Deployments**: Zero-downtime deployments
- **Canary Deployments**: Gradual rollout for safety
- **CDN Invalidation**: Selective cache invalidation
- **Database Migrations**: Run migrations separately from code deployment

### Build & Deploy Performance Checklist

Use this checklist to ensure optimal build and deployment performance:

- [ ] Build command completes under target time
- [ ] Test suite runtime is acceptable and parallelizable
- [ ] CI/CD is configured to avoid redundant builds
- [ ] Deploys include basic smoke tests before flipping traffic
- [ ] Build artifacts are cached between runs
- [ ] Dependencies are cached and updated efficiently
- [ ] Database migrations are optimized and tested separately
- [ ] Deployment rollback process is fast (< 2 minutes)

### Performance Monitoring

**Track**:
- Build times (per build type: dev, staging, production)
- Test suite durations (unit, integration, E2E)
- Deployment durations (per environment)
- Build artifact sizes

**Alert On**:
- Build times exceeding thresholds
- Test suite regressions (sudden slowdowns)
- Deployment failures or timeouts
- Unexpected build artifact size increases

---

## 18.5 Performance Tuning Workflow

### Initial Setup

1. **Set Baseline**:
   - Run `python3 auto_master.py perf_status` to see current config
   - Run initial `grow` or `impl_loop` and note times
   - Log baseline metrics

2. **Define Goals**:
   - Target automation speed (e.g., "grow should complete in < 30 minutes")
   - Target AI cost (e.g., "< $10 per full PRD growth")
   - Target application performance (e.g., "API < 200ms, 60fps UI")

3. **Configure Limits**:
   - Set `ai_usage` budgets
   - Tune `chunking_tuning` and `growth_tuning`
   - Configure `build_runtime` thresholds

### Ongoing Optimization

1. **Monitor**:
   - Regularly run `perf_status`
   - Review `auto_master.log` for performance patterns
   - Track application performance metrics

2. **Analyze**:
   - Run `perf_suggest` for recommendations
   - Identify bottlenecks (slow chunks, expensive calls, long builds)
   - Compare actual vs. target performance

3. **Tune**:
   - Adjust config based on analysis
   - Test changes with small runs first
   - Document changes and rationale

4. **Iterate**:
   - Re-measure after changes
   - Refine based on results
   - Update performance goals as needed

### Performance vs. Cost Trade-offs

**Speed-Optimized Configuration**:
- Larger chunks (300-400 lines)
- More chunks per pass (15-20)
- More passes per run (5-10)
- Higher token limits
- **Result**: Faster automation, higher cost

**Cost-Optimized Configuration**:
- Larger chunks (300-400 lines)
- Fewer chunks per pass (5-8)
- Fewer passes per run (1-2)
- Lower token limits
- **Result**: Slower automation, lower cost

**Balanced Configuration**:
- Moderate chunks (120-200 lines)
- Moderate chunks per pass (8-12)
- Moderate passes per run (2-4)
- Moderate token limits
- **Result**: Balanced speed and cost

**Quality-Optimized Configuration**:
- Moderate chunks (120-200 lines)
- Fewer chunks per pass (5-8)
- More passes per run (5-10)
- Higher token limits
- Adaptive chunking enabled
- **Result**: Higher quality, moderate speed, higher cost

---

## 18.6 Integration with Existing Systems

### Evaluation Integration

**Performance Metrics in Benchmarks**:
- `benchmark_growth` should report:
  - Time per pass
  - Time per chunk
  - Estimated token usage
  - Cost estimates (if configured)

- `benchmark_impl` should report:
  - Time per phase
  - Files generated per minute
  - Build/test times

### Deployment Integration

**Pre-Deployment Performance Checks**:
- Verify build times are acceptable
- Check test suite duration
- Review deployment time estimates
- Confirm resource requirements

**Post-Deployment Monitoring**:
- Monitor application performance metrics
- Track resource usage (CPU, memory, network)
- Alert on performance regressions
- Review cost trends

### Security Integration

**Performance Security Considerations**:
- Rate limiting to prevent abuse
- Resource quotas to prevent DoS
- Timeout configurations to prevent hanging
- Cost limits to prevent runaway spending

<!-- PERFORMANCE_SECTION_END -->

# 19. ANALYTICS, TELEMETRY, USER FEEDBACK & CONTINUOUS LEARNING

This section defines how the application collects, analyzes, and learns from user behavior, feedback, and system telemetry to continuously improve the product.

<!-- ANALYTICS_SECTION_START -->

## 19.1 Analytics Strategy & KPIs

Analytics provides the foundation for data-driven product decisions. This section defines what to measure, why it matters, and how success is evaluated.

### Purpose of Analytics

**Understanding User Behavior**:
- How users interact with the product
- Which features are used most
- Where users drop off or encounter issues
- User journey patterns and flows

**Measuring Feature Effectiveness**:
- Whether new features achieve their goals
- Feature adoption rates
- Impact on key metrics
- ROI of feature development

**Informing Product Decisions**:
- Prioritizing roadmap items
- Identifying improvement opportunities
- Validating hypotheses
- Measuring product-market fit

### KPI Planning Template

Document your key performance indicators:

```markdown
#### KPI Planning: [Project Name]

**Primary KPIs:**
- [e.g., Daily Active Users (DAU)]
  - Definition: Number of unique users who engage with the app in a 24-hour period
  - Target: [e.g., 10,000 DAU by month 3]
  - Measurement: Count unique user IDs with at least one event per day

- [e.g., 7-Day Retention Rate]
  - Definition: Percentage of users who return 7 days after first use
  - Target: [e.g., 40% retention by month 2]
  - Measurement: (Users active on day 0 AND day 7) / (Users active on day 0)

- [e.g., Conversion Rate]
  - Definition: Percentage of users who complete a key action (signup, purchase, etc.)
  - Target: [e.g., 15% signup-to-purchase conversion]
  - Measurement: (Users who purchase) / (Users who sign up)

**Secondary KPIs:**
- [e.g., Session Length]
  - Definition: Average time users spend in app per session
  - Target: [e.g., 5+ minutes average]
  - Measurement: Average time between app_open and app_close events

- [e.g., Feature Adoption Rate]
  - Definition: Percentage of active users who use a specific feature
  - Target: [e.g., 60% of users use core feature X]
  - Measurement: (Users with feature_used event) / (Total active users)

- [e.g., Error Rate]
  - Definition: Percentage of sessions with at least one error
  - Target: [e.g., < 2% error rate]
  - Measurement: (Sessions with error event) / (Total sessions)

**Success Criteria:**
- [e.g., Reach 10,000 DAU by month 3]
- [e.g., Achieve 40% 7-day retention by month 2]
- [e.g., Maintain < 2% error rate]

**Measurement Plan:**
- [How each KPI is calculated]
- [Which events are required for calculation]
- [Data sources and tools]
- [Reporting frequency]
```

### KPI Configuration

Map your KPIs to `auto_config.json.analytics.kpis`:

```json
{
  "analytics": {
    "kpis": {
      "primary": [
        "daily_active_users",
        "retention_d7",
        "conversion_rate"
      ],
      "secondary": [
        "session_length",
        "feature_adoption_rate",
        "error_rate"
      ]
    }
  }
}
```

---

## 19.2 Event Tracking Plan (Telemetry)

A well-defined event tracking plan ensures consistent, meaningful data collection. This section documents the event schema and tracking strategy.

### Event Schema Principles

**Consistency**:
- Use consistent naming conventions (snake_case recommended)
- Group related events by category
- Document all events in this section

**Privacy**:
- Classify events by privacy level (public, internal, sensitive, restricted)
- Avoid collecting PII unless necessary
- Respect user opt-out preferences

**Completeness**:
- Track all critical user actions
- Include error and system events
- Cover key user journeys end-to-end

### Event Schema Template

For each event, document:

```markdown
#### Event: [event_name]

- **Description:** [What does this event represent? What user action or system state does it capture?]

- **Category:** [auth / engagement / monetization / error / system / navigation]

- **Trigger Conditions:** [What exactly causes this event to fire? When does it occur?]

- **Properties:**
  - `property_name`: type (required/optional, description)
  - Example: `user_id`: string (required, anonymized user identifier)
  - Example: `feature_name`: string (required, name of feature used)
  - Example: `timestamp`: number (required, Unix timestamp)

- **Privacy Level:** [public / internal / sensitive / restricted]

- **Data Classification:** [How does this event relate to data classification levels?]

- **Destination(s):** [analytics_tool / logs / data_warehouse / all]

- **Required for KPIs:** [List which KPIs depend on this event]

- **Example:**
  ```json
  {
    "event": "feature_used",
    "properties": {
      "user_id": "anon_abc123",
      "feature_name": "export_data",
      "timestamp": 1703123456
    }
  }
  ```
```

### Core Events

Map the core events from `auto_config.json.analytics.events.core_events` to detailed schemas:

#### Event: app_open

- **Description:** User opens the application (cold start or background resume)

- **Category:** engagement

- **Trigger Conditions:** App launches or resumes from background

- **Properties:**
  - `user_id`: string (optional if not logged in, required if logged in)
  - `session_id`: string (required, unique session identifier)
  - `platform`: string (required, "ios" / "android" / "web" / "desktop")
  - `app_version`: string (required, version number)
  - `timestamp`: number (required, Unix timestamp)

- **Privacy Level:** internal

- **Required for KPIs:** daily_active_users, weekly_active_users, session_length

#### Event: sign_up

- **Description:** User completes registration/signup flow

- **Category:** auth

- **Trigger Conditions:** User successfully creates account

- **Properties:**
  - `user_id`: string (required, new user identifier)
  - `signup_method`: string (required, "email" / "oauth_google" / "oauth_apple" / etc.)
  - `timestamp`: number (required, Unix timestamp)

- **Privacy Level:** sensitive

- **Required for KPIs:** conversion_rate, retention_d7

#### Event: login

- **Description:** User successfully authenticates

- **Category:** auth

- **Trigger Conditions:** User completes login flow successfully

- **Properties:**
  - `user_id`: string (required)
  - `login_method`: string (required, "email" / "oauth" / "biometric" / etc.)
  - `timestamp`: number (required, Unix timestamp)

- **Privacy Level:** sensitive

- **Required for KPIs:** daily_active_users, session_length

#### Event: feature_used

- **Description:** User interacts with a specific feature

- **Category:** engagement

- **Trigger Conditions:** User performs action that represents feature usage

- **Properties:**
  - `user_id`: string (required)
  - `feature_name`: string (required, name of feature)
  - `feature_category`: string (optional, category of feature)
  - `timestamp`: number (required, Unix timestamp)

- **Privacy Level:** internal

- **Required for KPIs:** feature_adoption_rate

#### Event: purchase

- **Description:** User completes a purchase transaction

- **Category:** monetization

- **Trigger Conditions:** Purchase transaction successfully completed

- **Properties:**
  - `user_id`: string (required)
  - `transaction_id`: string (required, unique transaction identifier)
  - `product_id`: string (required, product identifier)
  - `amount`: number (required, purchase amount)
  - `currency`: string (required, currency code)
  - `timestamp`: number (required, Unix timestamp)

- **Privacy Level:** restricted

- **Required for KPIs:** conversion_rate

#### Event: error

- **Description:** An error occurs in the application

- **Category:** error

- **Trigger Conditions:** Application encounters an error (exception, API failure, etc.)

- **Properties:**
  - `user_id`: string (optional)
  - `error_type`: string (required, "exception" / "api_error" / "validation_error" / etc.)
  - `error_message`: string (required, error message - sanitized, no PII)
  - `error_code`: string (optional, error code)
  - `feature_name`: string (optional, feature where error occurred)
  - `timestamp`: number (required, Unix timestamp)

- **Privacy Level:** internal

- **Required for KPIs:** error_rate

#### Event: feedback_submitted

- **Description:** User submits feedback through in-app feedback form

- **Category:** engagement

- **Trigger Conditions:** User submits feedback form

- **Properties:**
  - `user_id`: string (optional)
  - `feedback_type`: string (required, "bug_report" / "feature_request" / "general" / etc.)
  - `feedback_text`: string (optional, feedback text - sanitized, no PII)
  - `rating`: number (optional, 1-5 rating if applicable)
  - `timestamp`: number (required, Unix timestamp)

- **Privacy Level:** sensitive

- **Required for KPIs:** (feedback analysis, not a direct KPI)

### Custom Events

Beyond core events, document project-specific events using the same template. Examples:

- `screen_view` - User views a screen/page
- `button_click` - User clicks a button (for critical actions)
- `search_performed` - User performs a search
- `content_shared` - User shares content
- `subscription_started` - User starts a subscription
- `tutorial_completed` - User completes onboarding tutorial

### Event Tracking Implementation

**Implementation Guidelines**:
- Instrument events at the point of user action or system event
- Use consistent event names across platforms
- Include all required properties
- Sanitize and anonymize data before sending
- Respect user privacy preferences

**Testing**:
- Verify events fire correctly in development
- Test event properties are correct
- Validate events appear in analytics tool
- Check privacy compliance (no PII leakage)

---

## 19.3 User Feedback & Qualitative Signals

Quantitative analytics tell you what users do; qualitative feedback tells you why. This section defines how to collect, analyze, and act on user feedback.

### Feedback Channels

**In-App Feedback**:
- Feedback forms within the application
- Rating prompts after key actions
- Bug reporting tools
- Feature request forms

**App Store Reviews**:
- Ratings and reviews on app stores
- Response to user reviews
- Review sentiment analysis

**Email Support**:
- Support tickets and inquiries
- Feature requests via email
- Bug reports via email

**Community Forums**:
- Community discussions (Discord, forums, etc.)
- Feature discussions
- User questions and answers

**Social Media**:
- Mentions and discussions on social platforms
- Direct messages and comments

### Feedback Intake & Summarization Template

Document feedback collection and analysis:

```markdown
#### Feedback Summary: [Date Range]

**Feedback Channel:** [in_app / app_store / email / community / social]

**Volume:** [approx # per week/month]

**Common Themes:**
- [e.g., "confusing onboarding flow" - mentioned 15 times]
- [e.g., "performance issues on older devices" - mentioned 8 times]
- [e.g., "request for dark mode" - mentioned 12 times]

**Top User Requests:**
1. [e.g., "Dark mode support" - 12 requests]
2. [e.g., "Offline mode" - 8 requests]
3. [e.g., "Export data feature" - 6 requests]
4. [e.g., "Better search functionality" - 5 requests]
5. [e.g., "Customizable dashboard" - 4 requests]

**Critical Issues:**
- [e.g., "App crashes on login for iOS 15 users" - 3 reports, high severity]
- [e.g., "Data loss bug in export feature" - 2 reports, critical severity]

**Actionable Items:**
- [Link to Phase/Task in PRD, e.g., "Phase 4.2.1: Implement dark mode"]
- [Link to Bug Fix Task, e.g., "Task 5.1.3: Fix iOS 15 login crash"]
- [Link to Feature Request, e.g., "Task 6.2.1: Add offline mode"]

**Sentiment:**
- Positive: [%]
- Neutral: [%]
- Negative: [%]

**Trends:**
- [e.g., "Onboarding confusion decreasing after recent UI update"]
- [e.g., "Performance complaints increasing on Android devices"]
```

### Feedback Analysis Workflow

1. **Collect**: Gather feedback from all configured channels
2. **Categorize**: Group feedback by theme, type, and severity
3. **Prioritize**: Rank feedback by impact, frequency, and feasibility
4. **Document**: Add to Feedback Summary in this section
5. **Action**: Create tasks/phases in PRD for high-priority items
6. **Follow-up**: Track resolution and communicate back to users

### Feedback Configuration

Configure feedback channels in `auto_config.json.analytics.feedback`:

```json
{
  "analytics": {
    "feedback": {
      "enabled": true,
      "channels": [
        "in_app_feedback",
        "app_store_reviews",
        "email_support",
        "community_forum"
      ],
      "auto_summarize_feedback": true,
      "feedback_review_frequency": "weekly"
    }
  }
}
```

---

## 19.4 Experiments & A/B Testing

Experiments allow you to test hypotheses and make data-driven decisions about product changes. This section defines a generic, tool-agnostic approach to experimentation.

### Experimentation Principles

**Hypothesis-Driven**:
- Every experiment starts with a clear hypothesis
- Define success criteria before running
- Measure against specific KPIs

**Statistical Rigor**:
- Ensure adequate sample sizes
- Run experiments for sufficient duration
- Use appropriate statistical tests

**Ethical Considerations**:
- Don't experiment on critical user flows without safeguards
- Respect user privacy
- Provide opt-out mechanisms

### Experiment Template

Document each experiment:

```markdown
#### Experiment: [Experiment ID]

- **Experiment ID:** [e.g., "EXP-ONBOARDING-001"]

- **Hypothesis:** [e.g., "A shorter signup form (3 fields instead of 5) will improve signup completion rate by 10%"]

- **Variants:**
  - **Control:** [e.g., "Current signup form with 5 fields (email, password, name, phone, company)"]
  - **Variant A:** [e.g., "Short signup form with 3 fields (email, password, name)"]
  - **Variant B:** [optional, e.g., "Social signup only (OAuth)"]

- **Target Users:** [e.g., "New users on web platform, 50% control, 50% variant A"]

- **Primary KPI(s):** [e.g., "Signup completion rate (users who complete signup / users who start signup)"]

- **Secondary KPI(s):** [e.g., "Time to complete signup", "Drop-off points in signup flow"]

- **Duration:** [e.g., "2 weeks or until 1,000 users per variant"]

- **Start Date:** [YYYY-MM-DD]

- **End Date:** [YYYY-MM-DD or "Ongoing"]

- **Status:** [planned / running / completed / paused / cancelled]

- **Results:**
  - Control: [e.g., "65% completion rate, avg 2.3 minutes"]
  - Variant A: [e.g., "78% completion rate, avg 1.8 minutes"]
  - Statistical Significance: [e.g., "p < 0.01, 95% confidence"]

- **Decision:** [e.g., "Ship Variant A - 13% improvement in completion rate, statistically significant"]

- **Next Steps:** [e.g., "Roll out Variant A to 100% of users, monitor for 1 week, then archive experiment"]
```

### Experiment Lifecycle

1. **Plan**: Define hypothesis, variants, and success criteria
2. **Design**: Create experiment template, set up tracking
3. **Launch**: Start experiment with appropriate traffic split
4. **Monitor**: Track metrics and watch for issues
5. **Analyze**: Evaluate results and statistical significance
6. **Decide**: Choose winning variant or iterate
7. **Document**: Record results and learnings in PRD
8. **Act**: Implement winning variant or plan next iteration

### Experiment Configuration

Configure experiments in `auto_config.json.analytics.experiments`:

```json
{
  "analytics": {
    "experiments": {
      "enabled": true,
      "framework": "generic",
      "max_concurrent_experiments": 5,
      "require_hypothesis": true,
      "min_sample_size": 100
    }
  }
}
```

---

## 19.5 Continuous Learning Loop

The continuous learning loop connects analytics, feedback, and experiments to product improvement. This section defines how to close the loop between data and action.

### Learning Loop Stages

**1. Instrument & Collect**:
- Implement event tracking
- Set up feedback channels
- Configure analytics tools
- Begin data collection

**2. Analyze & Summarize**:
- Review KPIs regularly
- Analyze event patterns
- Summarize feedback themes
- Evaluate experiment results

**3. Synthesize Insights**:
- Identify trends and patterns
- Connect quantitative and qualitative data
- Formulate hypotheses
- Prioritize opportunities

**4. Plan & Implement**:
- Create new phases/tasks in PRD
- Update roadmap and backlog
- Implement improvements
- Design new experiments

**5. Measure & Iterate**:
- Track impact of changes
- Measure against KPIs
- Collect new feedback
- Start next iteration

### Learning Loop Integration

**With Progress Log** (Section 10):
- Document analytics insights in Progress Log
- Track how data influenced decisions
- Record experiment results and learnings

**With Automation Evolution Log** (Section 12.5):
- Document how analytics improved automation
- Track performance optimizations based on data
- Record feedback-driven improvements

**With Security & Privacy** (Section 17):
- Ensure analytics respects privacy constraints
- Document data handling practices
- Comply with regulations (GDPR, CCPA, etc.)

### Continuous Learning Template

Document your learning loop:

```markdown
#### Learning Cycle: [Date Range, e.g., "2025-01-01 to 2025-01-31"]

**Data Collected:**
- Events: [e.g., "1.2M events, 45K unique users"]
- Feedback: [e.g., "127 feedback items across 4 channels"]
- Experiments: [e.g., "2 experiments completed, 1 ongoing"]

**Key Insights:**
- [e.g., "Signup completion rate improved 15% after onboarding redesign"]
- [e.g., "Feature X adoption increased 40% after in-app tutorial"]
- [e.g., "Error rate decreased 30% after bug fixes in Phase 4.2"]

**Hypotheses Formed:**
- [e.g., "Adding social login will increase signup rate by 20%"]
- [e.g., "Reducing app load time will improve retention"]

**Actions Taken:**
- [Link to Phase/Task, e.g., "Phase 5.1: Implemented social login"]
- [Link to Phase/Task, e.g., "Phase 5.2: Optimized app load time"]

**Results:**
- [e.g., "Social login increased signup rate by 18% (hypothesis validated)"]
- [e.g., "App load time reduced 40%, retention improved 5%"]

**Next Iteration:**
- [Planned experiments]
- [Planned improvements]
- [Areas to investigate further]
```

---

## 19.6 Privacy & Compliance Considerations

Analytics and feedback collection must respect user privacy and comply with regulations.

### Privacy Principles

**Data Minimization**:
- Collect only data necessary for defined purposes
- Avoid collecting PII unless required
- Use anonymization and aggregation where possible

**User Control**:
- Provide opt-out mechanisms
- Respect user privacy preferences
- Allow data deletion requests

**Transparency**:
- Clearly communicate what data is collected
- Explain how data is used
- Provide privacy policy and terms

### Compliance Checklist

- [ ] Privacy policy includes analytics data collection
- [ ] User consent obtained where required (GDPR, CCPA)
- [ ] Data retention policies defined and implemented
- [ ] User data deletion process documented
- [ ] Analytics data anonymized where possible
- [ ] Third-party analytics tools comply with regulations
- [ ] Data processing agreements in place (if applicable)

### Integration with Security Section

Refer to Section 17 (Security, Privacy, Compliance & Testing) for:
- Data classification levels
- Privacy principles
- Compliance requirements
- Data handling procedures

<!-- ANALYTICS_SECTION_END -->

---

# 20. DEVELOPER EXPERIENCE, ONBOARDING & EDUCATION

This section provides comprehensive guidance for developers and AI agents using this template, covering onboarding, workflows, troubleshooting, and learning resources.

<!-- DX_SECTION_START -->

## 20.1 Personas: Who Is This For?

This template is designed for different types of users, each with different needs and workflows.

### Solo Developer

**Profile**: Individual developer building a personal project or startup MVP.

**Needs**:
- Quick setup and getting started
- Clear documentation
- AI assistance for PRD growth and code generation
- Minimal overhead

**Recommended Workflow**:
1. Use GitHub "Use this template" to create new repo
2. Configure `auto_config.json` minimally (project name, type)
3. Use Meta-Orchestrator (Section 11) to drive automation
4. Focus on product development, let automation handle PRD growth

**Key Sections to Read**:
- Section 0: How to Read This Document
- Section 11: Meta-Orchestrator Instructions
- Section 20: This section (DX & Onboarding)

### Small Team (2-5 People)

**Profile**: Small team collaborating on a product.

**Needs**:
- Shared understanding of the system
- Clear contribution guidelines
- Version control and collaboration
- Role-based development

**Recommended Workflow**:
1. One person sets up repo from template
2. Team reviews and customizes `auto_config.json`
3. Team uses Meta-Orchestrator or manual commands
4. Regular PRD reviews and updates
5. Use git for collaboration

**Key Sections to Read**:
- Section 0: How to Read This Document
- Section 11: Meta-Orchestrator Instructions
- Section 13: Governance & Contribution
- Section 20: This section (DX & Onboarding)

### AI Agent as Code Assistant

**Profile**: AI assistant helping with code generation and implementation.

**Needs**:
- Clear implementation patterns
- Understanding of code generation commands
- Respect for safety constraints
- Knowledge of available roles

**Recommended Workflow**:
1. Read Section 5 (Implementation & Engineering Notes)
2. Read Section 2 (Omni-Corp Role Library)
3. Use `plan_impl` to generate implementation plan
4. Use `impl_phase` to generate code for specific phases
5. Respect `auto_config.json.implementation` settings

**Key Sections to Read**:
- Section 2: Omni-Corp Role Library
- Section 5: Implementation & Engineering Notes
- Section 11: Meta-Orchestrator Instructions (for context)

### AI Agent as Project Orchestrator

**Profile**: AI agent acting as Meta-Orchestrator, driving the full automation pipeline.

**Needs**:
- Complete understanding of automation system
- Knowledge of all commands and workflows
- Respect for safety and governance constraints
- Ability to interpret user intent

**Recommended Workflow**:
1. Read Section 11 (Meta-Orchestrator Instructions) completely
2. Understand all sections (0-20) for context
3. Use `auto_master.py` commands as primary interface
4. Never modify core automation files without explicit request
5. Provide clear summaries and next steps

**Key Sections to Read**:
- Section 11: Meta-Orchestrator Instructions (complete)
- All sections for full context
- Section 20: This section (DX & Onboarding)

---

## 20.2 Typical Workflows (DX View)

### Workflow 1: "I Have a New App Idea"

**Goal**: Start a new project from scratch using this template.

**Steps**:

1. **Create Repository**:
   ```bash
   # Option A: Use GitHub template
   # Click "Use this template" on GitHub, create new repo
   
   # Option B: Clone and customize
   git clone <template-repo> my-app
   cd my-app
   ```

2. **Initial Configuration**:
   - Edit `auto_config.json`:
     - Set `implementation.primary_target_type` (mobile/web/game/backend/ai_tool)
     - Set `implementation.primary_language` (typescript/python/dart/etc.)
     - Set `implementation.primary_framework` (react_native/nextjs/flutter/etc.)
     - Optionally set `domain_packs.default_pack`
   - Edit `prd.md` Section 1:
     - Update project name and description
     - Add initial vision and target users

3. **Initialize System**:
   ```bash
   python3 auto_master.py init
   python3 auto_master.py status
   ```

4. **Let AI Drive (Recommended)**:
   - Open repo in AI IDE (Cursor, Claude Desktop, etc.)
   - Open `prd.md`, find Section 11 (Meta-Orchestrator Instructions)
   - Copy the complete prompt between `<!-- META_ORCHESTRATOR_PROMPT_START -->` and `<!-- META_ORCHESTRATOR_PROMPT_END -->`
   - Paste into new AI chat
   - Describe your app idea in 2-5 sentences
   - Type: `start`
   - The AI will:
     - Run `init` and `sync_roles`
     - Run `grow` to expand PRD
     - Run `plan_impl` to create implementation plan
     - Suggest next steps

5. **Or Use Manual Commands**:
   ```bash
   python3 auto_master.py sync_roles
   python3 auto_master.py grow
   python3 auto_master.py plan_impl
   ```

6. **Review and Iterate**:
   - Review generated PRD content
   - Review implementation plan
   - Use `python3 auto_master.py impl_phase --phase X.Y.Z` to generate code
   - Continue with `grow` and `impl_phase` as needed

**Expected Timeline**:
- Setup: 5-10 minutes
- Initial PRD growth: 30-60 minutes (automated)
- Review and iteration: Ongoing

### Workflow 2: "I Want to Continue an Existing Project"

**Goal**: Resume work on a project that's already been set up.

**Steps**:

1. **Pull Latest Changes**:
   ```bash
   git pull origin main  # or your branch
   ```

2. **Check System Health**:
   ```bash
   python3 auto_master.py doctor
   python3 auto_master.py status --verbose
   ```

3. **Understand Current State**:
   - Read Section 10 (Progress Log) in `prd.md` to see what's been done
   - Read Section 9 (Tasks, Backlog & Roadmap) to see what's planned
   - Check `auto_master.log` for recent activity

4. **Continue Work**:
   - **If PRD needs more detail**: `python3 auto_master.py grow`
   - **If ready to implement**: `python3 auto_master.py plan_impl` then `impl_phase`
   - **If using AI**: Use Meta-Orchestrator commands (`start`, `status`, `regrow`, `implement phase X`)

5. **Review Changes**:
   - Review PRD updates
   - Review generated code
   - Test and iterate

**Common Commands**:
```bash
python3 auto_master.py status        # Check current state
python3 auto_master.py grow          # Continue PRD growth
python3 auto_master.py plan_impl     # Update implementation plan
python3 auto_master.py impl_phase --phase 3.2.1  # Implement specific phase
```

### Workflow 3: "I Want to Debug Something"

**Goal**: Diagnose and fix issues with the automation system.

**Steps**:

1. **Run Health Check**:
   ```bash
   python3 auto_master.py doctor
   ```
   - Review severity (OK/WARN/ERROR)
   - Note any issues reported

2. **Check System Status**:
   ```bash
   python3 auto_master.py status --verbose
   ```
   - Review chunk status
   - Check for inconsistencies

3. **Inspect Logs**:
   ```bash
   tail -n 100 auto_master.log
   # Or open auto_master.log in editor
   ```
   - Look for error messages
   - Check timestamps
   - Identify patterns

4. **Run Diagnostic Commands**:
   ```bash
   python3 auto_master.py smoke_test          # Verify system works
   python3 auto_master.py security_check      # Check security config
   python3 auto_master.py perf_status         # Check performance config
   python3 auto_master.py analytics_status    # Check analytics config
   ```

5. **Common Fixes**:
   - **State is corrupted**: `python3 auto_master.py init` (rebuilds state)
   - **Config is invalid**: Fix `auto_config.json`, validate with `python -m json.tool auto_config.json`
   - **PRD is out of sync**: Run `init` to rebuild state from PRD
   - **Git issues**: Check `git_status`, resolve conflicts manually

6. **Document Issues**:
   - Add to Section 10 (Progress Log) if significant
   - Add to Section 12.5 (Automation Evolution Log) if system improvement needed
   - Update this FAQ if issue is common

**Common Error Messages**:

- **"prd.md not found"**: Ensure you're in the repo root, file should exist
- **"Failed to parse auto_config.json"**: Run `python -m json.tool auto_config.json` to validate JSON
- **"State file corrupted"**: Run `python3 auto_master.py init` to rebuild
- **"Chunk processing failed"**: Check `auto_master.log` for details, may be AI integration issue

### Workflow 4: "I Want to Add Custom Functionality"

**Goal**: Add project-specific automation without modifying core.

**Steps**:

1. **Identify Need**:
   - Determine if functionality is project-specific or template-wide
   - If template-wide, consider contributing to core (see Section 13)
   - If project-specific, create extension

2. **Create Extension**:
   - Create script in `tools/` or `scripts/`
   - Use `auto_master.py` commands as API
   - Follow extension protocols (Section 21.3)

3. **Register Extension**:
   - Add to `auto_config.json.extensions.known_extensions`
   - Document in `prd.md` Section 21

4. **Test Extension**:
   - Test extension works correctly
   - Verify it doesn't break core functionality
   - Update documentation if needed

**Key Principle**: Don't modify core automation files unless you're contributing to the template itself.

---

## 20.3 FAQ for Common Confusions

### General Questions

**Q: Where is the main spec and prompts?**
A: In `prd.md`. This is the only master spec file. Everything lives here.

**Q: What files should I never delete?**
A: Core automation files: `prd.md`, `auto_master.py`, `auto_config.json`, `auto_master.sh`, `cursor_driver.scpt`, `.gitignore`, `LICENSE`, `README.md`. Runtime files (`.auto_state.json`, `auto_master.log`) can be regenerated.

**Q: How do I run the automation from the terminal?**
A:
```bash
python3 auto_master.py --help              # See all commands
python3 auto_master.py init                # Initialize system
python3 auto_master.py status              # Check status
python3 auto_master.py grow                # Grow PRD
python3 auto_master.py plan_impl           # Generate implementation plan
python3 auto_master.py impl_phase --phase 3.2.1  # Implement phase
```

**Q: How do I let the AI drive everything?**
A: Open the repo in your AI IDE, copy the Meta-Orchestrator prompt from `prd.md` Section 11, paste it into a new chat, describe your app, and type `start`. The AI will orchestrate the full pipeline.

**Q: What if the AI keeps making extra files I don't want?**
A: The template rules say: only core automation files are allowed. Merge or delete extras, and re-run `doctor` & `status`. If using Meta-Orchestrator, remind it of the file constraints from Section 11.

**Q: Can I use this for multiple projects?**
A: Yes! See Section 14 (App Factory Mode) for multi-project usage. Each project should have its own repo.

### Configuration Questions

**Q: How do I configure the system for my project?**
A: Edit `auto_config.json`:
- Set `implementation.primary_target_type` (mobile/web/game/backend/ai_tool)
- Set `implementation.primary_language` and `primary_framework`
- Optionally set `domain_packs.default_pack`
- Configure other sections as needed (deployment, security, performance, analytics)

**Q: What's the difference between profiles?**
A: Profiles (in `auto_config.json.profiles`) define how the Meta-Orchestrator behaves:
- `hands_free_local`: Full automation, can run shell commands
- `hands_free_no_cursor`: Full automation, no Cursor driver
- `assistive_read_only`: Read-only, suggests commands
- `semi_automatic`: Requires confirmation for major operations

**Q: How do I enable Cursor integration?**
A: Set `use_cursor_driver: true` in `auto_config.json`. Requires macOS and Cursor IDE. See `cursor_driver.scpt` for details.

### PRD Growth Questions

**Q: How long does it take to grow the PRD?**
A: Depends on target size and AI model. Typical: 1K → 10K lines takes 1-2 hours, 10K → 50K takes 3-5 hours. Use `grow` command and monitor progress.

**Q: Can I control how fast the PRD grows?**
A: Yes, configure in `auto_config.json`:
- `growth.max_passes`: Limit passes per `grow` command
- `growth.max_chunks_per_pass`: Limit chunks per pass
- `chunk_size_lines`: Adjust chunk size (affects speed vs. cost)

**Q: What if the PRD gets too large or detailed?**
A: You can:
- Stop growing (don't run `grow`)
- Manually edit `prd.md` to remove or consolidate sections
- Use `reset` to start over (backup first!)

### Implementation Questions

**Q: How do I generate code?**
A:
1. Ensure `implementation.enabled: true` in `auto_config.json`
2. Run `python3 auto_master.py plan_impl` to generate implementation plan
3. Run `python3 auto_master.py impl_phase --phase X.Y.Z` to generate code for a phase
4. Review generated code in `generated_dir` (configured in `auto_config.json`)

**Q: Where does generated code go?**
A: In `implementation.generated_dir` (default: `src/generated`). This directory is safe to overwrite. Manual code should go elsewhere.

**Q: Can I customize the code generation?**
A: Yes, edit `auto_config.json.implementation`:
- Set `default_roles_for_impl` to use specific expert roles
- Set `impl_max_files_per_phase` to limit files per phase
- Configure `source_dir`, `generated_dir`, `test_dir`

### Troubleshooting Questions

**Q: The system seems broken. What do I do?**
A:
1. Run `python3 auto_master.py doctor` to diagnose
2. Check `auto_master.log` for errors
3. Run `python3 auto_master.py status --verbose` to see state
4. If state is corrupted: `python3 auto_master.py init` (rebuilds state)
5. If still broken: Check Section 20.2 (Workflow 3: Debugging)

**Q: Commands are failing. How do I debug?**
A:
- Check `auto_master.log` for detailed error messages
- Run `python3 auto_master.py doctor` for health check
- Verify `auto_config.json` is valid JSON: `python -m json.tool auto_config.json`
- Check that required files exist (`prd.md`, `auto_config.json`)

**Q: AI integration isn't working.**
A:
- If using Cursor: Check `use_cursor_driver: true` and macOS/Cursor setup
- If using local stub: This is expected - commands will log but not call AI
- Check `auto_master.log` for AI-related errors

### Extension Questions

**Q: Can I add my own commands to `auto_master.py`?**
A: For project-specific commands, create separate scripts in `tools/` or `scripts/` that use `auto_master.py` as a library. Don't modify `auto_master.py` directly unless contributing to the template.

**Q: Can I add custom roles?**
A: Yes! Add to a project-specific section in `prd.md` (e.g., Section 2.X: Project-Specific Roles). Follow the role template from Section 2.

**Q: Can I customize the Meta-Orchestrator prompt?**
A: Yes, but be careful. The prompt in Section 11 is the core automation interface. If you modify it, document changes and consider contributing back to the template.

---

## 20.4 Learning Resources & Hints

### Internal Learning Resources

**Within This Template**:

- **Section 0**: How to Read This Document (start here)
- **Section 11**: Meta-Orchestrator Instructions (for AI-driven workflows)
- **Section 12**: Evaluation & Benchmarks (how to verify system works)
- **Section 13**: Governance & Contribution (how to extend safely)
- **Section 15**: Domain Packs (project type guidance)
- **Section 16**: Deployment (deployment patterns)
- **Section 17**: Security (security best practices)
- **Section 18**: Performance (optimization strategies)
- **Section 19**: Analytics (data-driven development)
- **Section 20**: This section (DX & Onboarding)

### External Learning Resources

**Software Architecture**:
- Learn about system design, scalability, and architecture patterns
- Understand domain-driven design and clean architecture
- Study microservices vs. monolith trade-offs

**Prompt Engineering**:
- Learn how to write effective prompts for AI models
- Understand role-based prompting and few-shot learning
- Study prompt templates and patterns

**Testing**:
- Learn unit, integration, and E2E testing strategies
- Understand test-driven development (TDD)
- Study testing frameworks for your stack

**Security**:
- Learn about common vulnerabilities (OWASP Top 10)
- Understand authentication and authorization patterns
- Study secure coding practices

**Performance**:
- Learn about performance optimization techniques
- Understand profiling and monitoring
- Study caching, database optimization, and CDN usage

**Analytics**:
- Learn about event tracking and KPI design
- Understand A/B testing and experimentation
- Study data-driven product development

### Experimentation Tips

**Start Small**:
- Begin with a simple project to learn the system
- Experiment with different domain packs
- Try different AI models and configurations

**Iterate Gradually**:
- Don't try to configure everything at once
- Start with defaults, customize as needed
- Learn from each iteration

**Use Version Control**:
- Commit frequently
- Use branches for experiments
- Tag stable versions

**Document Learnings**:
- Add to Section 10 (Progress Log)
- Update Section 12.5 (Automation Evolution Log)
- Share insights with community (if contributing)

### Getting Help

**Self-Service**:
1. Read Section 0 and Section 20 (this section)
2. Run `python3 auto_master.py --help` for command reference
3. Check `auto_master.log` for detailed error messages
4. Review relevant sections in `prd.md`

**Community** (if applicable):
- Check repository issues and discussions
- Review contribution guidelines (Section 13)
- Ask questions in community forums

**For Template Improvements**:
- Follow Section 13.3 (Contribution Workflow)
- Submit pull requests with clear descriptions
- Document changes in Automation Evolution Log

---

## 20.5 Quick Reference: Common Commands

### Initialization & Status

```bash
python3 auto_master.py init              # Initialize system (rebuild state)
python3 auto_master.py status            # Show system status
python3 auto_master.py status --verbose  # Detailed status with chunk info
python3 auto_master.py doctor            # Health check and diagnostics
```

### PRD Growth

```bash
python3 auto_master.py sync_roles        # Sync role library into prd.md
python3 auto_master.py enhance --limit 2 # Process 2 chunks (testing)
python3 auto_master.py grow              # Full autonomous growth loop
python3 auto_master.py reset             # Reset state (backup first!)
```

### Implementation

```bash
python3 auto_master.py plan_impl                    # Generate implementation plan
python3 auto_master.py impl_phase --phase 3.2.1     # Implement specific phase
python3 auto_master.py impl_phase --phase 3.2.1 --limit-files 3  # Limit files
python3 auto_master.py impl_loop --max-tasks 5      # Implement multiple tasks
```

### Git Operations

```bash
python3 auto_master.py git_status       # Show git and automation status
python3 auto_master.py git_sync         # Manual git sync (add, commit, push)
```

### Evaluation & Diagnostics

```bash
python3 auto_master.py smoke_test              # Quick system verification
python3 auto_master.py benchmark_growth        # Measure growth performance
python3 auto_master.py benchmark_impl          # Test implementation pipeline
python3 auto_master.py security_check          # Check security configuration
python3 auto_master.py perf_status             # Show performance settings
python3 auto_master.py analytics_status        # Show analytics configuration
```

### Deployment & Monitoring

```bash
python3 auto_master.py deploy --env staging --dry-run    # Dry-run deployment
python3 auto_master.py deploy_status --env staging       # Check deployment status
python3 auto_master.py monitor                           # Monitor application health
```

### Help & Documentation

```bash
python3 auto_master.py --help           # Show all commands and options
python3 auto_master.py <command> --help # Show help for specific command
```

---

## 20.6 Troubleshooting Guide

### Common Issues and Solutions

**Issue: "prd.md not found"**
- **Solution**: Ensure you're in the repo root directory. The file should be at the root.

**Issue: "Failed to parse auto_config.json"**
- **Solution**: Validate JSON: `python -m json.tool auto_config.json`. Fix syntax errors.

**Issue: "State file corrupted"**
- **Solution**: Run `python3 auto_master.py init` to rebuild state from `prd.md`.

**Issue: "No chunks to process"**
- **Solution**: All chunks may be done. Run `reset` then `init` to start over, or manually add content to `prd.md`.

**Issue: "AI integration not working"**
- **Solution**: 
  - If using Cursor: Check macOS, Cursor installation, and `use_cursor_driver: true`
  - If using local stub: This is expected - commands log but don't call AI
  - Check `auto_master.log` for specific errors

**Issue: "Chunk processing keeps failing"**
- **Solution**:
  - Check `auto_master.log` for error details
  - Verify AI integration is working
  - Try reducing `chunk_size_lines` in config
  - Check network connectivity if using remote AI

**Issue: "Git sync fails"**
- **Solution**:
  - Check `git_status` to see repository state
  - Ensure `git.enable_auto: true` if using automatic sync
  - Resolve conflicts manually
  - Verify remote and branch names in config

**Issue: "Generated code is wrong"**
- **Solution**:
  - Review implementation plan in Section 5
  - Check `auto_config.json.implementation` settings
  - Verify phase ID exists in PRD
  - Regenerate with different roles if needed

### Debugging Workflow

1. **Gather Information**:
   ```bash
   python3 auto_master.py doctor > debug_report.txt
   python3 auto_master.py status --verbose >> debug_report.txt
   tail -n 200 auto_master.log >> debug_report.txt
   ```

2. **Identify Issue**:
   - Review debug report
   - Check error messages in logs
   - Verify configuration

3. **Apply Fix**:
   - Follow solution from troubleshooting guide
   - Or consult relevant section in `prd.md`

4. **Verify Fix**:
   ```bash
   python3 auto_master.py doctor
   python3 auto_master.py smoke_test
   ```

5. **Document**:
   - Add to Section 10 (Progress Log) if significant
   - Update this troubleshooting guide if issue is common

<!-- DX_SECTION_END -->

---

# 21. EXTENSIBILITY, PLUGINS & LONG-TERM EVOLUTION

This section defines how to safely extend, customize, and evolve this automation system without breaking its minimal core or creating incompatible forks.

<!-- EXTENSION_SECTION_START -->

## 21.1 Extension Philosophy

This template is designed with a **minimal, stable core** that can be safely extended with project-specific functionality.

### Core Principles

**The Automation Core Is**:
- **Minimal**: Only essential files for universal functionality
- **Stable**: Changes are carefully versioned and documented
- **Template-Wide**: Core files are shared across all projects using this template

**Extensions Should**:
- Live in project-specific locations (code directories, `tools/`, `scripts/`)
- Use `auto_master.py` commands and `auto_config.json` as their "API"
- Avoid introducing new permanent automation control files that compete with core files
- Be clearly documented and discoverable

**Core vs Extension Separation**:

**Core Automation Files** (managed by template maintainers):
- `prd.md` - Single master document
- `auto_master.py` - CLI orchestrator
- `auto_config.json` - Configuration
- `auto_master.sh` - Shell wrapper
- `cursor_driver.scpt` - Cursor integration
- `.gitignore`, `LICENSE`, `README.md` - Repo hygiene

**Extensions** (local, per-project add-ons):
- Custom scripts in `tools/` or `scripts/`
- Project-specific code in application directories
- Custom prompts or roles in `prd.md` (project-specific sections)
- Additional configuration in `auto_config.json.extensions`

**Key Rule**: Do not add new permanent PRD or automation controller files. If you need more structure, add sections to `prd.md` or fields to `auto_config.json`.

---

## 21.2 Extension Zones (Where to Put Custom Logic)

Extensions should live in clearly designated zones that are separate from the core automation files.

### Recommended Extension Zones

**1. Application Code Tree**:
- `src/`, `app/`, `backend/`, `game/`, etc. for domain-specific logic
- These directories are for your application code, not automation extensions
- Extensions that generate or process application code can live here

**2. Tools Directory** (`tools/`):
- Helper scripts and utilities
- Examples:
  - `tools/regenerate_docs.sh` - Regenerate documentation from PRD
  - `tools/export_prd_to_pdf.py` - Export PRD sections to PDF
  - `tools/validate_implementation.py` - Validate generated code

**3. Scripts Directory** (`scripts/`):
- Automation and workflow scripts
- Examples:
  - `scripts/run_full_cycle.sh` - Run full automation cycle
  - `scripts/ci_pipeline_helper.sh` - CI/CD integration
  - `scripts/custom_deploy.sh` - Custom deployment logic

**4. Project-Specific PRD Sections**:
- Custom roles in `prd.md` Section 2.X (Project-Specific Roles)
- Custom prompts in `prd.md` Section 8.X (Project-Specific Prompt Library)
- Custom domain packs documented in Section 15

**5. Extension Configuration**:
- `auto_config.json.extensions.known_extensions` - Registry of extensions
- Additional config under `auto_config.json.extensions.*`

### Extension Zone Rules

**DO**:
- ✅ Put extensions in `tools/` or `scripts/` directories
- ✅ Document extensions in `auto_config.json.extensions.known_extensions`
- ✅ Document extensions in this section of `prd.md`
- ✅ Use `auto_master.py` as an API (call commands, don't replace them)
- ✅ Follow extension protocols (see Section 21.3)

**DON'T**:
- ❌ Add new permanent automation files at repo root
- ❌ Modify core automation files (`auto_master.py`, core `prd.md` sections) unless contributing to template
- ❌ Create competing automation systems
- ❌ Store secrets or sensitive data in extension scripts

---

## 21.3 Extension Protocols (How Extensions Talk to Core)

Extensions interact with the core through well-defined protocols.

### Protocol 1: Shell / Script Wrappers

**Pattern**: Scripts that call `auto_master.py` commands.

**Example**:
```bash
#!/bin/bash
# tools/run_full_cycle.sh (example extension, not part of core)

set -euo pipefail

echo "Running full automation cycle..."

# Health check
python3 auto_master.py doctor

# Grow PRD
python3 auto_master.py grow

# Plan implementation
python3 auto_master.py plan_impl

# Implement first phase (if provided)
if [ -n "${1:-}" ]; then
    python3 auto_master.py impl_phase --phase "$1"
fi

echo "Cycle complete!"
```

**Characteristics**:
- Simple shell scripts that orchestrate `auto_master.py` commands
- Can accept parameters and pass them to commands
- Can include project-specific logic between commands
- Should be documented in `auto_config.json.extensions.known_extensions`

### Protocol 2: Python Module Extensions

**Pattern**: Python scripts that import or call `auto_master.py` functions.

**Example**:
```python
#!/usr/bin/env python3
# tools/custom_analyzer.py (example extension)

import sys
import json
from pathlib import Path

# Read config
config_path = Path("auto_config.json")
with open(config_path) as f:
    config = json.load(f)

# Use auto_master.py as library (if functions are importable)
# Or call via subprocess
import subprocess

result = subprocess.run(
    ["python3", "auto_master.py", "status", "--verbose"],
    capture_output=True,
    text=True
)

# Process results
print("Status:", result.stdout)

# Custom analysis logic here...
```

**Characteristics**:
- Python scripts that use `auto_master.py` as a library or call it via subprocess
- Can read `auto_config.json` directly
- Can process outputs and perform custom logic
- Should be documented in extension registry

### Protocol 3: Config-Driven Extensions

**Pattern**: Extensions that read configuration from `auto_config.json.extensions`.

**Example**:
```json
{
  "extensions": {
    "known_extensions": [
      {
        "id": "ci_pipeline_helper",
        "type": "script",
        "entrypoint": "scripts/ci_pipeline_helper.sh",
        "description": "Runs tests, lint, and a dry-run deploy for CI",
        "owner": "team",
        "dependencies": ["npm", "pytest"]
      }
    ]
  }
}
```

**Characteristics**:
- Extensions are registered in config
- Core system can discover and report on extensions
- Extensions can declare dependencies
- Extensions are documented and versioned

### Protocol 4: AI Meta-Prompt Extensions

**Pattern**: Additional agent scripts that live inside `prd.md`.

**Example**:
```markdown
### Project-Specific Agent: Custom Deployment Orchestrator

**Act as:** A specialized deployment orchestrator for this project.

**Instructions:**
- Read deployment config from auto_config.json
- Execute custom deployment steps
- Use auto_master.py deploy commands as base
- Add project-specific validation

[Additional prompt content...]
```

**Characteristics**:
- Custom prompts live in `prd.md` (Section 8.X or project-specific section)
- Not separate `.md` files
- Can reference core Meta-Orchestrator prompt
- Can extend or specialize core behavior

### Extension Protocol Best Practices

**1. Use Core as API**:
- Call `auto_master.py` commands, don't reimplement them
- Read `auto_config.json` for configuration
- Respect core safety constraints

**2. Document Extensions**:
- Register in `auto_config.json.extensions.known_extensions`
- Document in `prd.md` Section 21
- Include description, owner, and usage instructions

**3. Follow Safety Rules**:
- Never delete `prd.md` or core files
- Never force-push git
- Never store secrets in extension scripts
- Respect user privacy and security constraints

**4. Make Extensions Discoverable**:
- Use consistent naming conventions
- Place in designated directories (`tools/`, `scripts/`)
- Register in extension registry

---

## 21.4 Evolution Rules for Core

The core template must evolve carefully to maintain stability and compatibility.

### Core Evolution Principles

**Do Not**:
- ❌ Rename or remove core automation files
- ❌ Break CLI command signatures without version bump
- ❌ Introduce new mandatory files for all users
- ❌ Remove or break existing config sections without migration path
- ❌ Change Meta-Orchestrator prompt in breaking ways without version bump

**When Evolving Core**:

1. **Version Bumping**:
   - Update `TEMPLATE_VERSION` in `auto_master.py`
   - Follow Semantic Versioning (MAJOR.MINOR.PATCH)
   - MAJOR: Breaking changes
   - MINOR: New features, backward compatible
   - PATCH: Bug fixes, internal improvements

2. **Documentation**:
   - Update Template Version & Changelog in `prd.md` Section 13.2
   - Document changes grouped by MAJOR/MINOR/PATCH
   - Provide migration notes for breaking changes

3. **Migration Path**:
   - For breaking changes, provide clear upgrade instructions
   - Maintain compatibility shims where possible
   - Give users reasonable time to migrate

4. **Testing**:
   - Run `smoke_test` and benchmarks before release
   - Test with multiple profiles
   - Verify backward compatibility

### Core File Modification Rules

**`prd.md` Core Sections** (Sections 0, 2, 3, 8, 11-21):
- Changes affect all projects using template
- Breaking changes require MAJOR version bump
- New features can be MINOR version
- Bug fixes are PATCH version

**`auto_master.py`**:
- Command signatures must remain stable
- New commands can be added (MINOR)
- Breaking command changes require MAJOR version
- Internal refactoring is PATCH

**`auto_config.json` Schema**:
- New optional fields can be added (MINOR)
- Breaking schema changes require MAJOR version
- Field renames require migration notes

**Core Safety**:
- Never remove safety constraints
- Never allow operations that could delete `prd.md`
- Never bypass git safety checks

---

## 21.5 Extension Versioning & Ownership

Extensions are project-specific and can use their own versioning schemes.

### Extension Versioning

**Recommended Approaches**:

1. **Project-Specific Versioning**:
   - Simple version tags in extension comments
   - Example: `# Extension v1.2 - Updated for new API`
   - No formal versioning required

2. **Semantic Versioning** (for complex extensions):
   - Use SemVer if extension is shared across projects
   - Example: `"version": "1.2.0"` in `known_extensions` entry

3. **Git-Based Versioning**:
   - Use git tags or commit hashes
   - Example: `"version": "git:abc123"` or `"version": "tag:v1.0"`

4. **No Versioning** (for simple scripts):
   - Simple scripts may not need versioning
   - Document changes in PRD or commit messages

### Extension Ownership

**Document in `auto_config.json.extensions.known_extensions`**:
- `owner`: String - Owner/maintainer name or team
- `description`: String - What the extension does
- `documented_in_prd_section`: String - Where it's documented in PRD

**Document in `prd.md` Section 21**:
- Extension purpose and usage
- When to use the extension
- Dependencies and requirements
- Maintenance status

### Extension Lifecycle

**1. Creation**:
- Create extension in designated zone (`tools/`, `scripts/`)
- Register in `auto_config.json.extensions.known_extensions`
- Document in `prd.md` Section 21

**2. Maintenance**:
- Update extension as needed
- Update documentation if behavior changes
- Update version if using versioning

**3. Deprecation**:
- Mark as deprecated in config and PRD
- Provide migration path if needed
- Remove after deprecation period

**4. Removal**:
- Remove from `known_extensions`
- Remove from PRD documentation
- Delete extension files
- Document removal in PRD if significant

---

## 21.6 Example Extensions

### Example 1: CI Pipeline Helper

**Purpose**: Integrate automation with CI/CD pipelines.

**Location**: `scripts/ci_pipeline_helper.sh`

**Implementation**:
```bash
#!/bin/bash
# CI Pipeline Helper - Runs automation checks for CI

set -euo pipefail

echo "Running CI automation checks..."

# Health check
python3 auto_master.py doctor

# Run smoke tests
python3 auto_master.py smoke_test

# Check security
python3 auto_master.py security_check --dry-run

# Run tests
python3 auto_master.py quick_test --scope full

echo "CI checks complete!"
```

**Registration**:
```json
{
  "id": "ci_pipeline_helper",
  "type": "script",
  "entrypoint": "scripts/ci_pipeline_helper.sh",
  "description": "Runs automation checks for CI/CD pipelines (doctor, smoke_test, security_check, quick_test)",
  "owner": "devops_team",
  "dependencies": ["python3", "auto_master.py"]
}
```

### Example 2: PRD Exporter

**Purpose**: Export PRD sections to PDF or other formats for stakeholders.

**Location**: `tools/export_prd_to_pdf.py`

**Implementation** (conceptual):
```python
#!/usr/bin/env python3
# PRD Exporter - Exports key PRD sections to PDF

import sys
from pathlib import Path

# Read PRD
prd_path = Path("prd.md")
# Parse markdown
# Convert to PDF
# Export
```

**Registration**:
```json
{
  "id": "prd_exporter",
  "type": "python_module",
  "entrypoint": "tools/export_prd_to_pdf.py",
  "description": "Exports key PRD sections to PDF for stakeholder review",
  "owner": "product_team",
  "dependencies": ["python3", "markdown", "pdfkit"]
}
```

### Example 3: Custom Deployment Script

**Purpose**: Project-specific deployment logic that extends core deployment.

**Location**: `scripts/custom_deploy.sh`

**Implementation**:
```bash
#!/bin/bash
# Custom Deployment - Extends core deploy with project-specific steps

set -euo pipefail

ENV="${1:-staging}"

# Use core deploy command
python3 auto_master.py deploy --env "$ENV" --dry-run

# Custom pre-deployment steps
echo "Running custom pre-deployment checks..."

# Custom deployment logic
echo "Deploying to $ENV..."

# Use core deploy_status
python3 auto_master.py deploy_status --env "$ENV"
```

**Registration**:
```json
{
  "id": "custom_deploy",
  "type": "script",
  "entrypoint": "scripts/custom_deploy.sh",
  "description": "Custom deployment script that extends core deploy with project-specific steps",
  "owner": "devops_team"
}
```

---

## 21.7 Extension Discovery & Documentation

### Discovery

**Via Config**:
- Extensions are registered in `auto_config.json.extensions.known_extensions`
- Use `python3 auto_master.py extensions_status` to list extensions

**Via File System**:
- Extensions live in `tools/` or `scripts/` directories
- Can be discovered by scanning these directories

**Via PRD**:
- Extensions are documented in `prd.md` Section 21
- Search for "Extension:" or extension IDs

### Documentation Requirements

**In `auto_config.json`**:
- Extension ID, type, entrypoint, description, owner
- Optional: version, dependencies, PRD section reference

**In `prd.md` Section 21**:
- Extension purpose and use cases
- How to use the extension
- Dependencies and requirements
- Examples and workflows

**In Extension File**:
- Header comment with description
- Usage instructions
- Dependencies
- Version (if applicable)

---

## 21.8 Long-Term Evolution Strategy

### Template Evolution

**Versioning**:
- Core template uses Semantic Versioning
- Versions tracked in `auto_master.py` and `prd.md` Section 13.2
- Breaking changes require MAJOR version bump

**Migration**:
- Provide migration guides for major versions
- Maintain backward compatibility where possible
- Give users time to migrate

**Community Contributions**:
- Follow Section 13 (Governance) for contributions
- Core improvements go through PR process
- Extensions can be shared as examples

### Extension Evolution

**Independent Evolution**:
- Extensions evolve independently of core
- No version coupling required
- Extensions can be updated without template upgrade

**Sharing Extensions**:
- Useful extensions can be shared as examples
- Consider contributing to template if generally useful
- Document in community resources (if applicable)

**Extension Compatibility**:
- Extensions should work with multiple template versions
- Use `auto_master.py` API for compatibility
- Test with different template versions if sharing

### Avoiding Fragmentation

**Core Stability**:
- Keep core minimal and stable
- Avoid adding features that should be extensions
- Maintain clear core vs. extension boundary

**Extension Patterns**:
- Encourage standard extension patterns
- Document best practices
- Provide examples

**Community Alignment**:
- Share extension patterns and examples
- Contribute generally useful extensions back
- Maintain compatibility with core

<!-- EXTENSION_SECTION_END -->

---

# 22. AI PROVIDERS, MODEL STRATEGY & TOOL INTEGRATION

This section defines how this project uses AI providers, models, and tools for automation tasks.

<!-- AI_STRATEGY_SECTION_START -->

## 22.1 AI Provider Inventory

This project is designed to work with multiple AI providers and tools. The actual provider configuration is stored in `auto_config.json` under `"ai"`.

### Current Provider Strategy

**Primary Provider**:
- IDE-integrated assistant (e.g., Cursor, Google AI agent)
  - Used for: PRD growth, code generation, refactoring
  - Advantages: Integrated workflow, no API costs, fast iteration
  - Limitations: Requires IDE, may have usage limits

**Secondary Provider** (if configured):
- Remote API model (e.g., OpenAI, Anthropic)
  - Used for: Evaluation, high-quality reviews, background tasks
  - Advantages: High quality, can run in background, no IDE required
  - Limitations: API costs, requires network, may have rate limits

**Optional Provider** (if configured):
- Local model (e.g., Ollama, local LLM)
  - Used for: Offline mode, privacy-sensitive tasks, cost-free operations
  - Advantages: No API costs, works offline, privacy-preserving
  - Limitations: May have lower quality, requires local setup, resource-intensive

**Stub Mode** (fallback):
- No AI provider available
  - Used for: Validation, state management, manual workflows
  - Behavior: Commands log operations but don't call AI

### Provider Configuration

Provider details are configured in `auto_config.json` under `"ai.providers"`. Each provider entry includes:
- Type (IDE assistant, API, local, stub)
- Supported tasks (PRD growth, code generation, evaluation, etc.)
- Requirements (IDE needed, API keys, local setup)
- Cost model

**Note**: Provider-specific secrets, API keys, and credentials are **not** stored in this repository. They should be configured via environment variables, IDE settings, or secure configuration files outside the repo.

---

## 22.2 Model Strategy by Task Type

Different tasks benefit from different AI providers and models. This project uses task-specific routing to optimize for quality, cost, and availability.

### AI Task Routing Template

**PRD Growth & Enhancement**:
- **Preferred**: IDE assistant (Cursor, Google agent)
  - Fast iteration, integrated with editor
  - Can reference full PRD context
- **Fallback**: Remote API (OpenAI, Anthropic)
  - High-quality output for complex enhancements
- **Alternative**: Local model
  - For offline work or privacy-sensitive content

**Code Generation & Implementation**:
- **Preferred**: IDE assistant
  - Integrated with codebase, understands context
  - Can generate and test code in same environment
- **Fallback**: Remote API
  - For complex code generation or when IDE unavailable
- **Not Recommended**: Local model (unless high-quality local model available)

**Evaluation & Benchmarks**:
- **Preferred**: Remote API (high-quality model)
  - Objective evaluation, consistent quality
  - Can run in background
- **Fallback**: IDE assistant
  - For quick checks or when API unavailable
- **Alternative**: Local model
  - For basic evaluation or offline mode

**Refactoring & Documentation**:
- **Preferred**: IDE assistant
  - Understands codebase structure
  - Can make incremental changes
- **Fallback**: Remote API or local model
  - For large-scale refactoring or documentation generation

**Documentation & Summaries**:
- **Preferred**: Any available provider
  - Lower quality requirements
  - Can use cheaper/faster models
- **Fallback**: Local model
  - For offline documentation work

### Task Routing Configuration

Task routing is configured in `auto_config.json` under `"ai.task_routing"`. Each task type specifies:
- `preferred_provider`: Primary provider for this task
- `fallback_providers`: Ordered list of fallback providers
- `model_preference`: Specific model or "auto" to let provider choose

**Example Configuration**:
```json
{
  "task_routing": {
    "prd_growth": {
      "preferred_provider": "cursor",
      "fallback_providers": ["openai", "anthropic"],
      "model_preference": "auto"
    }
  }
}
```

**Alignment**: This strategy should align with `auto_config.json.ai.task_routing` settings.

---

## 22.3 Tool/IDE Integration

This template is designed to work seamlessly with IDE-based AI assistants and terminal-based automation.

### IDE Integration

**Primary Workflow**:
1. Open repository in AI-enabled IDE (Cursor, VSCode with AI, etc.)
2. Copy Meta-Orchestrator prompt from `prd.md` Section 11
3. Paste into AI chat within IDE
4. Use natural language commands to drive automation
5. AI agent uses `auto_master.py` commands to execute operations

**IDE AI Agent Behavior**:
- Stays within user's IDE environment
- Does not launch new windows or IDE instances
- Uses existing terminal/shell access
- Respects IDE permissions and security settings

**Supported IDEs**:
- **Cursor**: Full integration via `cursor_driver.scpt` (macOS)
- **VSCode with AI**: Via terminal commands
- **Google AI Agent (antigravity)**: Via terminal commands
- **Other IDEs**: Via terminal commands and file access

### Terminal-Based Automation

**CLI Workflow**:
1. Run `auto_master.py` commands directly from terminal
2. Commands route AI tasks through configured providers
3. Results are logged and state is updated
4. Can be used in CI/CD or headless environments

**Hybrid Workflow**:
- IDE AI agent orchestrates high-level workflow
- `auto_master.py` commands handle low-level operations
- State is shared via `.auto_state.json` and `prd.md`

### Integration Best Practices

**For IDE Users**:
- Use Meta-Orchestrator prompt for high-level automation
- Let AI agent call `auto_master.py` commands
- Review AI suggestions before applying
- Use `auto_master.py` commands directly for debugging

**For Terminal Users**:
- Use `auto_master.py` commands directly
- Configure providers in `auto_config.json`
- Use `ai_status` and `ai_policy` to inspect configuration
- Set `execution_modes.allow_api_calls=true` if using remote APIs

**For CI/CD**:
- Use terminal-based automation
- Configure API providers for headless operation
- Set `execution_modes.allow_api_calls=true`
- Use stub mode for validation-only operations

---

## 22.4 Fallbacks & Graceful Degradation

The system is designed to work even when AI providers are unavailable or misconfigured.

### Fallback Strategy

**When Primary Provider Unavailable**:
1. Check `task_routing[task_type].fallback_providers`
2. Try each fallback provider in order
3. Use first available provider that supports the task
4. If all providers unavailable, use stub mode

**When All Providers Unavailable**:
- **Stub Mode**: Commands log operations but don't call AI
  - State management still works
  - Config validation still works
  - Tests can still run
  - Human can follow logged instructions manually

**Fallback Configuration**:
Configured in `auto_config.json` under `"ai.fallback_strategy"`:
- `on_provider_unavailable`: Behavior when provider unavailable
- `on_all_providers_unavailable`: Behavior when all providers unavailable
- `stub_mode_behavior`: What to do in stub mode

### Graceful Degradation Guidelines

**If Primary Provider Not Available**:
- Use `task_routing.fallback_providers` where allowed by `execution_modes`
- Log which provider is being used
- Continue operation with available provider

**If No AI Available**:
- `auto_master.py` commands should still:
  - Manage state (`.auto_state.json`)
  - Validate configuration
  - Run tests and diagnostics
  - Provide clear instructions for humans to follow manually
- Never hard-crash because a specific AI provider is missing
- Prefer clear logs and degraded behavior over errors

**If API Calls Not Allowed**:
- Respect `execution_modes.allow_api_calls=false`
- Use IDE-only or local providers
- Fall back to stub mode if no IDE/local provider available
- Log clear message about why API calls are disabled

**If Local Models Not Available**:
- Respect `execution_modes.allow_local_models=false`
- Use IDE or API providers
- Fall back to stub mode if no other providers available

### Error Handling

**Provider Errors**:
- Log error with provider name and task type
- Try fallback providers
- If all fail, enter stub mode with clear log message

**Configuration Errors**:
- Validate `auto_config.json.ai` on startup
- Report missing or invalid configuration
- Use safe defaults (stub mode) if config invalid

**Network Errors** (for API providers):
- Retry with exponential backoff (if configured)
- Fall back to other providers
- Enter stub mode if all API providers fail

---

## 22.5 Safety & Guardrails (AI-Specific)

AI operations must respect security, privacy, and safety constraints.

### Security & Privacy

**Secrets & Credentials**:
- **Never** store API keys, tokens, or credentials in:
  - `prd.md`
  - `auto_config.json` (unless encrypted or in secure config)
  - `auto_master.log`
  - Git-committed files
- Use environment variables or secure configuration files
- Use IDE's built-in credential management when available

**Data Handling**:
- **Never** paste secrets into PRD or logs
- **Never** let AI auto-commit secrets
- Review AI suggestions before applying
- Treat AI output as suggestions, subject to human/owner review

**Provider-Specific Security**:
- Respect provider rate limits and usage policies
- Monitor API usage and costs
- Use secure connections (HTTPS) for API calls
- Validate provider responses before processing

### AI Decision Review

**Critical Operations**:
- AI decisions affecting security or privacy should be reviewed
- AI-generated code should be reviewed before deployment
- AI-suggested config changes should be validated

**Review Process**:
1. AI generates suggestion or change
2. Human reviews suggestion
3. Human approves or modifies
4. Change is applied

**Automated Review** (if configured):
- Use `execution_modes.require_human_approval_for_api=true`
- Require explicit approval for API calls
- Log all AI operations for audit

### Usage Policies

**Rate Limits**:
- Respect provider-specific rate limits
- Implement backoff and retry logic
- Monitor usage and adjust if needed

**Cost Management**:
- Monitor API costs (if using paid providers)
- Use cheaper models for non-critical tasks
- Set budgets in `performance.ai_usage` (if configured)

**Quality vs. Cost Trade-offs**:
- Use high-quality models for critical tasks
- Use cheaper/faster models for routine tasks
- Balance quality, cost, and speed based on project needs

### Connection to Security Section

This AI safety guidance complements the broader Security section (Section 17):
- AI operations must respect data classification (Section 17.2)
- AI-generated code must pass security checks (Section 17.4)
- AI operations must comply with privacy rules (Section 17.3)
- AI usage must be auditable (Section 17.5)

---

## 22.6 Provider-Specific Notes

### Cursor Integration

**Setup**:
- Requires macOS and Cursor IDE
- Configured via `cursor_driver.scpt`
- Uses IDE's built-in AI capabilities

**Usage**:
- Primary provider for most tasks
- Integrated with editor and terminal
- No API costs (included in IDE)

**Limitations**:
- Requires IDE to be open
- May have usage limits
- macOS-only for full integration

### OpenAI/Anthropic API

**Setup**:
- Requires API keys (configured via environment variables)
- Set `execution_modes.allow_api_calls=true`
- Configure `api_base_url` if using custom endpoint

**Usage**:
- High-quality output for complex tasks
- Can run in background
- Per-token pricing

**Limitations**:
- Requires network connection
- API costs
- Rate limits may apply

### Local Models

**Setup**:
- Requires local model installation (e.g., Ollama)
- Set `execution_modes.allow_local_models=true`
- Configure `model_path` or `api_endpoint`

**Usage**:
- Offline operation
- No API costs
- Privacy-preserving

**Limitations**:
- May have lower quality
- Resource-intensive
- Requires local setup

---

## 22.7 Configuration Examples

### Example 1: IDE-Only Setup

```json
{
  "ai": {
    "enabled": true,
    "default_provider": "cursor",
    "execution_modes": {
      "allow_ide_only": true,
      "allow_api_calls": false,
      "allow_local_models": false
    }
  }
}
```

### Example 2: API-Enabled Setup

```json
{
  "ai": {
    "enabled": true,
    "default_provider": "openai",
    "execution_modes": {
      "allow_ide_only": true,
      "allow_api_calls": true,
      "allow_local_models": false,
      "require_human_approval_for_api": true
    }
  }
}
```

### Example 3: Offline/Local Setup

```json
{
  "ai": {
    "enabled": true,
    "default_provider": "local_llm",
    "execution_modes": {
      "allow_ide_only": true,
      "allow_api_calls": false,
      "allow_local_models": true,
      "prefer_offline": true
    }
  }
}
```

<!-- AI_STRATEGY_SECTION_END -->

---

# 23. VALIDATION, DRY-RUNS & EXPERIMENT LOG

This section tracks how we verify that the automation system works correctly, safely, and without losing content.

<!-- VALIDATION_SECTION_START -->

## 23.1 Purpose of Validation

Validation ensures that:

- **Automation works correctly**: Commands execute as expected
- **PRD growth does not lose content**: `prd.md` is never truncated or corrupted
- **Implementation commands are wired correctly**: Code generation and planning work
- **Git automation is safe**: Git operations don't cause data loss
- **No garbage files are created**: Only allowed files are created
- **System is repeatable**: Same commands produce consistent results

### Validation Methods

Validation can be performed:

1. **Manually by a human**:
   - Run commands step-by-step
   - Review outputs and logs
   - Verify file integrity

2. **Semi-automatically by an AI agent**:
   - Use Meta-Orchestrator validation commands
   - Review and log results
   - Append to validation log

3. **Using CLI commands**:
   - Run `python3 auto_master.py validate --dry-run`
   - Review `auto_master.log` for results
   - Check validation section in `prd.md`

### Validation Frequency

- **After initial setup**: Verify template works in new environment
- **Before major changes**: Ensure system is stable
- **After template upgrades**: Verify compatibility
- **Periodically**: Catch regressions early

---

## 23.2 Standard Dry-Run Scenario

This is the standard "first validation" scenario for a fresh project. It exercises all major automation flows in safe, non-destructive mode.

### Step-by-Step Dry-Run

#### 1. Initialize Core State

**Command**: `python3 auto_master.py init`

**Expectations**:
- `.auto_state.json` is created or updated
- `auto_master.log` contains a clear entry
- `prd.md` remains intact (no modifications)
- No errors or warnings

**Validation**:
- Check `.auto_state.json` exists and is valid JSON
- Check `auto_master.log` has entry for `init` command
- Verify `prd.md` line count unchanged (or note initial count)

#### 2. Check Status

**Command**: `python3 auto_master.py status`

**Expectations**:
- Shows current growth state (lines, phases, tasks)
- Displays chunk status
- No errors

**Validation**:
- Status output is readable and complete
- No error messages
- State information matches actual `prd.md` content

#### 3. Run PRD Growth in Dry-Run Mode

**Command**: `python3 auto_master.py grow --dry-run`

**Expectations**:
- Logs proposed enhancements
- Does not truncate or overwrite PRD content
- Optionally writes suggested changes to log or notes
- Shows what would be added without actually adding

**Validation**:
- `prd.md` line count unchanged
- `auto_master.log` contains `[DRY_RUN]` entries
- Log shows what would have been added
- No errors or warnings

#### 4. Generate/Verify Implementation Plan

**Command**: `python3 auto_master.py plan_impl --dry-run`

**Expectations**:
- Checks or drafts the Implementation Plan section
- Does not wipe existing content
- Logs what would be generated

**Validation**:
- `prd.md` Implementation Plan section unchanged (or improved if empty)
- Log shows what would have been generated
- No content loss

#### 5. Simulate Implementing a Phase

**Command**: `python3 auto_master.py impl_phase --phase <test_phase_id> --dry-run`

**Expectations**:
- Logs what code or changes would be made
- Does not commit or modify source files aggressively
- Shows file paths and content that would be generated

**Validation**:
- No source files created or modified
- Log shows what would have been generated
- Phase ID is valid (exists in PRD)

#### 6. Run Health Checks

**Commands**:
- `python3 auto_master.py doctor`
- `python3 auto_master.py smoke_test`
- `python3 auto_master.py quick_test`

**Expectations**:
- All pass or clearly explain missing pieces
- No critical errors
- Warnings are acceptable if explained

**Validation**:
- `doctor` reports OK or WARN (not ERROR)
- `smoke_test` passes or explains what's missing
- `quick_test` passes or explains what's missing

#### 7. Inspect AI & Extensions Status

**Commands**:
- `python3 auto_master.py ai_status`
- `python3 auto_master.py extensions_status`

**Expectations**:
- Show config overview
- No critical errors
- Clear status for each provider/extension

**Validation**:
- Status output is readable
- No errors
- Configuration is valid

#### 8. Git Dry-Run (Optional)

**Commands**:
- `python3 auto_master.py git_status`
- `python3 auto_master.py git_sync --dry-run`

**Expectations**:
- Summarizes what would be committed or pushed
- Does not actually commit or push
- Shows file changes clearly

**Validation**:
- No actual git commits or pushes
- Log shows what would have been committed
- Git status is accurate

### Dry-Run Success Criteria

A successful dry-run should:
- ✅ Complete all steps without errors
- ✅ Not modify `prd.md` destructively
- ✅ Not create unexpected files
- ✅ Not commit to git
- ✅ Not deploy anything
- ✅ Log all operations clearly
- ✅ Show what would happen in real mode

---

## 23.3 Validation Runs

This table tracks validation runs performed on this project. Each entry documents a complete validation cycle.

### Validation Run Template

| Run ID | Date/Time | Environment | Commands | Result | Notes |
|--------|-----------|-------------|----------|--------|-------|
| VAL-001 | [YYYY-MM-DD HH:MM] | [IDE + OS + AI provider] | init, status, grow --dry-run | success | initial template validation |

### Field Definitions

- **Run ID**: Unique identifier (VAL-001, VAL-002, etc.)
- **Date/Time**: When validation was performed
- **Environment**: IDE, OS, AI provider used
- **Commands**: List of commands executed
- **Result**: success / warnings / failures
- **Notes**: Additional context, issues found, manual interventions

### Example Validation Runs

| Run ID | Date/Time | Environment | Commands | Result | Notes |
|--------|-----------|-------------|----------|--------|-------|
| VAL-001 | 2024-01-15 10:30 | Cursor + macOS + Cursor AI | init, status, grow --dry-run, plan_impl --dry-run, doctor | success | Initial template validation, all checks passed |
| VAL-002 | 2024-01-20 14:15 | VSCode + Linux + OpenAI API | validate --dry-run | warnings | AI API not configured, used stub mode |
| VAL-003 | 2024-02-01 09:00 | Cursor + macOS + Cursor AI | init, status, grow --dry-run, impl_phase --phase 3.2.1 --dry-run, git_sync --dry-run | success | Full validation after template upgrade |

### Adding Validation Entries

**For Humans**:
1. Run validation commands
2. Review results
3. Add entry to table above
4. Update notes with any issues or observations

**For AI Agents**:
1. Use `log validation result` command
2. Agent will append entry to table
3. Agent will format consistently

---

## 23.4 PRD Integrity Checks

The system includes automatic integrity checks to prevent PRD corruption or truncation.

### Integrity Check Points

**After PRD Writes**:
- Verify file exists
- Check line count hasn't decreased unexpectedly
- Optionally verify checksum
- Log any anomalies

**Before Major Operations**:
- Verify PRD is readable
- Check state consistency
- Validate structure

### Integrity Metrics

**Tracked in `.auto_state.json`**:
- `prd_last_line_count`: Last known line count
- `prd_last_checksum`: Optional checksum hash
- `prd_last_modified`: Timestamp of last modification

**Warning Thresholds**:
- If current line count < 0.7 * previous line count: WARNING
- If current line count < 0.5 * previous line count: ERROR
- If file missing: ERROR

### Manual Integrity Verification

**Check PRD Integrity**:
```bash
python3 auto_master.py doctor  # Includes integrity checks
```

**Verify Line Count**:
```bash
wc -l prd.md  # Manual check
python3 auto_master.py status  # Shows line count
```

---

## 23.5 Safety Rules

### Never Do These in Dry-Run Mode

- ❌ Truncate or overwrite `prd.md`
- ❌ Commit or push to git
- ❌ Deploy to remote environments
- ❌ Create new permanent automation files
- ❌ Delete core files
- ❌ Modify `.gitignore` or core config

### Always Do These in Dry-Run Mode

- ✅ Log all operations with `[DRY_RUN]` prefix
- ✅ Show what would happen
- ✅ Verify integrity after operations
- ✅ Report status clearly
- ✅ Allow review before real execution

### Safety Checkpoints

**Before Any PRD Write**:
1. Read current PRD
2. Record line count and checksum
3. Perform write operation
4. Verify integrity
5. Log result

**After Any PRD Write**:
1. Verify file exists
2. Check line count
3. Compare to previous state
4. Log warnings if anomalies detected

---

## 23.6 Validation Troubleshooting

### Common Issues

**Issue: PRD line count decreased unexpectedly**
- **Cause**: Truncation or corruption
- **Solution**: Restore from git, check logs, verify backup
- **Prevention**: Use dry-run mode, verify integrity checks

**Issue: Validation fails with "file not found"**
- **Cause**: Missing core files or wrong directory
- **Solution**: Run `init`, verify file structure
- **Prevention**: Use `doctor` command regularly

**Issue: Dry-run mode still modifies files**
- **Cause**: Command doesn't respect `--dry-run` flag
- **Solution**: Report bug, use git to restore
- **Prevention**: Test dry-run mode before real operations

**Issue: Validation takes too long**
- **Cause**: AI calls or large PRD
- **Solution**: Use `--limit` flags, reduce scope
- **Prevention**: Configure timeouts, use stub mode for testing

### Getting Help

1. Check `auto_master.log` for detailed error messages
2. Run `python3 auto_master.py doctor` for diagnostics
3. Review this validation section for known issues
4. Check `prd.md` Section 20 (DX & Onboarding) for troubleshooting

<!-- VALIDATION_SECTION_END -->

# 24. TEMPLATE PACKAGING & GITHUB PUBLISHING

This section defines how this repository functions as a reusable GitHub template and how to maintain it.

<!-- PACKAGING_SECTION_START -->

## 24.1 Template vs Project

This repository serves as a **template** that can be used to create new project repositories. Understanding the distinction between template and project is crucial.

### Template Repository

**Purpose**: Generic automation code and documentation that can be reused across many projects.

**Characteristics**:
- Contains generic automation code (`auto_master.py`, `auto_config.json`, etc.)
- Contains template documentation and examples
- No project-specific code or secrets
- No runtime state or logs
- Intended to be published on GitHub as a reusable template
- Can be forked or used via "Use this template" button

**Content**:
- Core automation files (see Section 24.2)
- Generic `prd.md` with template structure and examples
- Documentation and guides
- Example configurations

**What It Does NOT Contain**:
- Application source code
- Project-specific PRD content (beyond examples)
- Runtime state files (`.auto_state.json`, `auto_master.log`)
- Secrets or API keys
- Project-specific scripts or tools

### Project Repository (Created from Template)

**Purpose**: Actual application, game, website, or tool being built.

**Characteristics**:
- Created by cloning or using the template
- Adds actual app/game/website source code
- Expands `prd.md` to 100,000+ lines of project-specific PRD & prompts
- May add project-specific scripts, domain packs, CI config, etc.
- Contains runtime state and logs (git-ignored)

**Content**:
- All template core files (inherited from template)
- Application code in `src/`, `app/`, `backend/`, `game/`, etc.
- Project-specific PRD content in `prd.md`
- Project-specific configuration in `auto_config.json`
- Project-specific scripts in `tools/`, `scripts/`
- Runtime files (`.auto_state.json`, `auto_master.log`) - git-ignored

**What It Adds**:
- Domain-specific code and assets
- Project-specific documentation
- Custom extensions and tools
- CI/CD configuration
- Deployment configurations

### Core vs. Project-Specific

**Shared Core** (part of template):
- `prd.md` - Template structure and examples
- `auto_master.py` - CLI orchestrator
- `auto_config.json` - Base configuration
- `auto_master.sh` - Shell wrapper
- `cursor_driver.scpt` - IDE integration
- `.gitignore` - Git ignore rules
- `LICENSE` - License file
- `README.md` - Template documentation

**Project-Specific** (added in projects):
- Application code directories (`src/`, `app/`, etc.)
- Project-specific PRD content (Sections 1-9 in `prd.md`)
- Project-specific configuration (customized `auto_config.json`)
- Project-specific scripts (`tools/`, `scripts/`)
- Runtime state (`.auto_state.json`, `auto_master.log`)
- Project-specific documentation

**Key Principle**: The automation core is shared by all projects. All new code, assets, and scripts should live in regular project directories and are not part of the template core.

---

## 24.2 Template File Manifest

This section documents the exact set of files that must exist in the template repository.

### Template Core Files

These files are **required** and must be present in the template:

| File | Purpose | Required |
|------|---------|----------|
| `prd.md` | Single master Product Requirements & Prompt document | ✅ Yes |
| `auto_master.py` | CLI orchestrator for growth, implementation, validation | ✅ Yes |
| `auto_config.json` | Configuration (paths, chunking, AI, git, security, etc.) | ✅ Yes |
| `auto_master.sh` | Shell wrapper around `auto_master.py` | ✅ Yes |
| `cursor_driver.scpt` | IDE integration script (or stub) | ✅ Yes |
| `.gitignore` | Ignore runtime/state/log files and temp outputs | ✅ Yes |
| `LICENSE` | License for the template | ✅ Yes |
| `README.md` | Human-facing documentation and quickstart | ✅ Yes |

**Total**: 8 core files

### Runtime/Generated Files (Never Commit)

These files are **generated** by the automation system and must **never** be committed to the template:

| File/Pattern | Purpose | Git Status |
|--------------|---------|------------|
| `.auto_state.json` | Automation state (per project) | ❌ Must be ignored |
| `auto_master.log` | Automation log | ❌ Must be ignored |
| `*.tmp`, `*.temp` | Temporary files | ❌ Must be ignored |
| `.DS_Store` | macOS system file | ❌ Should be ignored |
| `__pycache__/` | Python cache | ❌ Should be ignored |
| `*.pyc` | Python bytecode | ❌ Should be ignored |

### .gitignore Requirements

The `.gitignore` file must include patterns for:

**Required Patterns**:
```
# Automation runtime files
.auto_state.json
auto_master.log

# Temporary files
*.tmp
*.temp
*.swp
*.swo
*~

# System files
.DS_Store
Thumbs.db

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# IDE files (optional, but recommended)
.vscode/
.idea/
*.sublime-project
*.sublime-workspace
```

**Verification**: Run `git status` and ensure no runtime files appear as untracked or staged.

### Files That Should NOT Be in Template

**Never Include**:
- ❌ Application source code (`src/`, `app/`, `backend/`, etc.)
- ❌ Project-specific PRD content (beyond examples)
- ❌ Runtime state files (`.auto_state.json`, `auto_master.log`)
- ❌ Secrets or API keys (`.env`, `secrets.json`, etc.)
- ❌ Compiled binaries or build artifacts
- ❌ Node modules, Python virtual environments, etc.
- ❌ Project-specific CI/CD configs (unless generic examples)

**If Found**: These should be removed before publishing the template.

---

## 24.3 Template Release Checklist

Before publishing or updating the template, maintainers should follow this checklist.

### Pre-Release Checklist

#### 1. Clean Working Tree

**Action**: `git status`

**Expectation**:
- No untracked runtime files (state/logs) are staged or committed
- Only intended changes are staged
- No unexpected files in root directory

**If Issues Found**:
- Remove runtime files: `git rm --cached .auto_state.json auto_master.log` (if accidentally staged)
- Review untracked files and add to `.gitignore` if needed
- Commit only intended changes

#### 2. Validation Dry-Run

**Actions**:
```bash
python3 auto_master.py init
python3 auto_master.py validate --dry-run
```

**Expectation**:
- All checks pass or report only expected "not configured yet" warnings
- No errors
- PRD integrity checks pass

**If Issues Found**:
- Fix errors before proceeding
- Document expected warnings
- Update validation section if needed

#### 3. Template Health Check

**Action**: `python3 auto_master.py template_check`

**Expectation**:
- All core files present
- No runtime files committed
- No suspicious files in root
- Template is clean and ready

**If Issues Found**:
- Fix reported issues
- Remove unwanted files
- Update `.gitignore` if needed

#### 4. File Manifest Check

**Action**: Manual review

**Expectation**:
- Only allowed core files are in the root
- No project-specific code or secrets are present
- No runtime files are committed

**If Issues Found**:
- Remove project-specific files
- Remove secrets (if any)
- Clean up root directory

#### 5. README & LICENSE

**Action**: Review documentation

**Expectation**:
- README explains how to use the repo as a template
- README includes quick start guide
- LICENSE is correct and up to date
- All links work

**If Issues Found**:
- Update README with missing information
- Verify LICENSE is appropriate
- Fix broken links

#### 6. Version Check

**Action**: Verify version consistency

**Expectation**:
- `TEMPLATE_VERSION` in `auto_master.py` is current
- Version is recorded in `prd.md` Section 24
- Version matches release tag (if applicable)

**If Issues Found**:
- Update `TEMPLATE_VERSION` if needed
- Update `prd.md` with current version
- Create or update release tag

#### 7. GitHub Template Settings

**Action**: Configure GitHub repository

**Steps**:
1. Go to repository Settings
2. Check "Template repository" checkbox
3. Save changes
4. Optionally create a release tag (e.g., `v1.0.0-template`)

**Expectation**:
- Repository is marked as template
- "Use this template" button appears on GitHub
- Release tag created (if applicable)

### Post-Release

**Actions**:
- Test template by creating a new project from it
- Verify new project initializes correctly
- Document any issues or improvements needed

---

## 24.4 Template Versioning

The template uses semantic versioning to track releases and changes.

### Version Format

**Semantic Versioning**: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (incompatible API or behavior changes)
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Version Location

**In Code**: `TEMPLATE_VERSION` constant in `auto_master.py`
```python
TEMPLATE_VERSION = "1.0.0"
```

**In Documentation**: Recorded in this section (Section 24) of `prd.md`
- Current Template Version: `1.0.0`

**In Git**: Release tags matching version (e.g., `v1.0.0-template`)

### Version Bumping Rules

**When to Bump MAJOR**:
- Breaking changes to `auto_master.py` command signatures
- Breaking changes to `auto_config.json` schema
- Breaking changes to `prd.md` structure
- Removal of core files

**When to Bump MINOR**:
- New commands added
- New configuration options (backward compatible)
- New sections added to `prd.md`
- New features added

**When to Bump PATCH**:
- Bug fixes
- Documentation updates
- Minor improvements
- Internal refactoring

### Version Update Process

1. Update `TEMPLATE_VERSION` in `auto_master.py`
2. Update version in `prd.md` Section 24
3. Update changelog in `prd.md` Section 13 (Governance)
4. Create release tag: `git tag v1.0.0-template`
5. Push tag: `git push origin v1.0.0-template`

---

## 24.5 Template Maintenance

### Regular Maintenance Tasks

**Monthly**:
- Review and update documentation
- Check for security updates
- Review and merge community contributions

**Before Each Release**:
- Run full release checklist (Section 24.3)
- Update version and changelog
- Test template with fresh project

**After Each Release**:
- Monitor for issues
- Update documentation based on feedback
- Plan next release

### Contributing to Template

See `prd.md` Section 13 (Governance & Contribution) for:
- Contribution guidelines
- Code of conduct
- Pull request process
- Review process

---

## 24.6 Creating a New Project from Template

### Using GitHub Template

1. **Click "Use this template"** on GitHub
2. **Create new repository** (private or public)
3. **Clone locally**: `git clone <your-repo-url>`
4. **Initialize**: `python3 auto_master.py init`
5. **Validate**: `python3 auto_master.py validate --dry-run`
6. **Start building**: Edit `prd.md` and begin development

### Manual Setup

1. **Clone template**: `git clone <template-repo-url> my-project`
2. **Remove template history**: `rm -rf .git && git init`
3. **Initialize**: `python3 auto_master.py init`
4. **Validate**: `python3 auto_master.py validate --dry-run`
5. **Start building**: Edit `prd.md` and begin development

### First Steps in New Project

1. **Configure project**: Edit `auto_config.json` with project-specific settings
2. **Update PRD**: Edit `prd.md` Section 1 with project vision
3. **Run validation**: `python3 auto_master.py validate --dry-run`
4. **Start automation**: Use Meta-Orchestrator or manual commands

---

## 24.7 Upgrading Projects from Template

When the template evolves, existing projects can be upgraded.

### Upgrade Process

1. **Review template changes**: Check release notes or changelog
2. **Backup project**: Commit all changes, create backup branch
3. **Merge template updates**:
   - `auto_master.py` - Replace with new version
   - `auto_config.json` - Merge carefully with local changes
   - `prd.md` - Update template sections only (keep project content)
   - `.gitignore`, `README.md` - Update if needed
4. **Validate**: `python3 auto_master.py template_check`
5. **Test**: `python3 auto_master.py validate --dry-run`
6. **Fix issues**: Resolve any conflicts or problems
7. **Commit**: Commit upgrade changes

### What to Update

**Always Update**:
- `auto_master.py` - Core automation code
- Template sections in `prd.md` (Sections 0, 11-24)
- `.gitignore` - If new patterns added

**Merge Carefully**:
- `auto_config.json` - Preserve project-specific settings
- `README.md` - Merge template updates with project-specific content

**Never Overwrite**:
- Project-specific PRD content (Sections 1-9)
- Application source code
- Project-specific scripts and tools

### Upgrade Safety

- Always backup before upgrading
- Test in a branch first
- Review changes carefully
- Run validation after upgrade
- Document any manual fixes needed

<!-- PACKAGING_SECTION_END -->

# 25. EXPERIMENTS, SANDBOX MODES & FUTURE IDEAS

This section provides a safe playground for experimental features and future ideas without destabilizing the core template.

<!-- SANDBOX_SECTION_START -->

## 25.1 Purpose of the Sandbox

The Sandbox is an **optional, experimental space** for exploring new ideas and features that are not yet part of the stable core template.

### What the Sandbox Is For

**Experimental Features**:
- New prompt patterns and AI workflows
- Prototype commands and automation flows
- Alternative chunking or growth strategies
- Different deployment or integration approaches
- Ideas that might later be promoted into the core

**What the Sandbox Is NOT For**:
- ❌ Breaking changes to core functionality
- ❌ Required features for normal template use
- ❌ Production-critical functionality
- ❌ Features that affect all users by default

### Key Principles

1. **Opt-In Only**: Sandbox features are disabled by default
2. **Clearly Labeled**: All experimental features are marked as such
3. **Isolated**: Experiments don't affect core behavior
4. **Documented**: All experiments are logged and tracked
5. **Promotable**: Successful experiments can become core features

### Safety Guarantees

- Sandbox features **never run automatically**
- Core template behavior is **never modified** by sandbox features
- Experiments are **clearly marked** in logs and output
- Sandbox can be **disabled entirely** if not needed

---

## 25.2 Sandbox Experiments Log

This log tracks experiments tried in the sandbox, their results, and decisions about promotion or abandonment.

### Experiment Log Template

| Exp ID | Date/Time | Idea | Files Touched | Result | Decision |
|--------|-----------|------|---------------|--------|----------|
| EXP-001 | [YYYY-MM-DD HH:MM] | [Brief description] | [Files modified] | [improved / no change / worse] | [keep / discard / promote] |

### Field Definitions

- **Exp ID**: Unique identifier (EXP-001, EXP-002, etc.)
- **Date/Time**: When experiment was performed
- **Idea**: Brief description of what was tried
- **Files Touched**: Which files were modified (sandbox config, experimental scripts, etc.)
- **Result**: Outcome (improved, no change, worse, needs more testing)
- **Decision**: What to do with the experiment (keep, discard, promote to core)

### Example Experiments

| Exp ID | Date/Time | Idea | Files Touched | Result | Decision |
|--------|-----------|------|---------------|--------|----------|
| EXP-001 | 2024-01-15 10:30 | Try different chunking strategy for large PRDs | auto_config.json (sandbox section only) | improved growth speed | keep |
| EXP-002 | 2024-01-20 14:15 | Test aggressive growth mode | auto_config.json, experimental script | faster but lower quality | discard |
| EXP-003 | 2024-02-01 09:00 | New AI routing for code generation | auto_config.json, prd.md (sandbox section) | significantly improved | promote |

### Adding Experiment Entries

**For Humans**:
1. Perform experiment
2. Document results
3. Add entry to table above
4. Update decision when ready

**For AI Agents**:
1. Use `log experiment EXP-XXX` command
2. Agent will append entry to table
3. Agent will format consistently

---

## 25.3 Promotion Rules

Experiments must meet strict criteria before being promoted to the core template.

### Promotion Criteria

**Before Promotion, Experiment Must**:
1. ✅ Be run on at least one real project
2. ✅ Pass validation (Step 23) with the new idea
3. ✅ Show clear benefit over existing approach
4. ✅ Not break existing functionality
5. ✅ Be documented and understood
6. ✅ Have explicit approval from template maintainers

### Promotion Process

**Step 1: Evaluation**:
- Run experiment on real project(s)
- Collect metrics and feedback
- Document results in experiment log

**Step 2: Validation**:
- Run `python3 auto_master.py validate --dry-run` with experiment enabled
- Verify no regressions
- Check all core functionality still works

**Step 3: Review**:
- Template maintainers review experiment
- Assess benefit vs. complexity
- Decide on promotion

**Step 4: Promotion**:
- Move idea into relevant core section (e.g., Implementation, Validation, AI Strategy)
- Update `auto_master.py`, `auto_config.json`, and `README.md` accordingly
- Update `TEMPLATE_VERSION` (MINOR or MAJOR bump)
- Note the change in Governance / Changelog (Section 13)
- Remove from sandbox (or keep as legacy option)

**Step 5: Documentation**:
- Update relevant sections in `prd.md`
- Update `README.md` if needed
- Create release notes

### What NOT to Promote

**Do NOT Promote**:
- ❌ Experiments that break backward compatibility
- ❌ Features that require significant new dependencies
- ❌ Ideas that are too project-specific
- ❌ Features that complicate the core unnecessarily
- ❌ Experiments that haven't been validated

### Abandonment

**When to Abandon**:
- Experiment shows no benefit
- Experiment causes problems
- Better alternative found
- Experiment is too complex for benefit

**Abandonment Process**:
1. Mark experiment as "discard" in log
2. Remove experimental code/config
3. Document why it was abandoned
4. Learn from the experiment

---

## 25.4 Sandbox Configuration

Sandbox features are controlled via `auto_config.json` under the `"sandbox"` section.

### Configuration Structure

```json
{
  "sandbox": {
    "enabled": false,
    "notes": "Optional playground for experimental behaviors.",
    "allow_experimental_commands": false,
    "experimental_flags": {
      "alt_chunking": false,
      "aggressive_growth": false,
      "auto_git_experiments": false,
      "custom_ai_routing": false
    }
  }
}
```

### Configuration Fields

- **`enabled`**: Boolean - Master switch for sandbox features (default: `false`)
- **`notes`**: String - Optional notes about sandbox usage
- **`allow_experimental_commands`**: Boolean - Allow experimental CLI commands (default: `false`)
- **`experimental_flags`**: Object - Individual feature flags

### Experimental Flags

**`alt_chunking`**: Alternative chunking strategies
- When enabled: Use experimental chunking algorithm
- Risk: May affect PRD growth quality
- Default: `false`

**`aggressive_growth`**: Faster but potentially lower-quality growth
- When enabled: Skip some validation steps for speed
- Risk: May produce lower-quality PRD content
- Default: `false`

**`auto_git_experiments`**: Experimental git automation
- When enabled: Try new git integration features
- Risk: May cause unexpected git operations
- Default: `false`

**`custom_ai_routing`**: Custom AI provider routing
- When enabled: Use experimental routing logic
- Risk: May affect AI task quality
- Default: `false`

### Safety Semantics

**When `sandbox.enabled = false`**:
- All experimental behaviors MUST NOT run automatically
- CLI should treat all sandbox features as disabled
- Experimental commands should show "sandbox disabled" message
- AI agents should not suggest enabling sandbox without explicit request

**When `sandbox.enabled = true`**:
- Experimental commands MAY be available
- All experimental features are clearly labeled in logs and help output
- AI agents should still be cautious
- Use dry-run where possible
- Warn users about experimental nature

---

## 25.5 Experiment Guidelines

### Good Experiments

**Characteristics**:
- ✅ Well-scoped and focused
- ✅ Clearly documented
- ✅ Easy to enable/disable
- ✅ Don't affect core behavior
- ✅ Have clear success criteria
- ✅ Can be easily abandoned if needed

**Examples**:
- Testing different prompt patterns
- Trying alternative chunk sizes
- Experimenting with AI routing
- Testing new validation checks

### Bad Experiments

**Characteristics**:
- ❌ Modify core files directly
- ❌ Break existing functionality
- ❌ Require significant refactoring
- ❌ Affect all users by default
- ❌ Hard to disable or revert
- ❌ Poorly documented

**Examples**:
- Changing core command signatures
- Removing required features
- Adding mandatory dependencies
- Breaking backward compatibility

### Experiment Best Practices

1. **Start Small**: Begin with minimal changes
2. **Document Everything**: Log what you're trying and why
3. **Test Thoroughly**: Validate before promoting
4. **Get Feedback**: Share results with community
5. **Be Ready to Abandon**: Not all experiments succeed
6. **Respect Core**: Never break stable functionality

---

## 25.6 Future Ideas

This section can be used to brainstorm and document future ideas that haven't been tried yet.

### Idea Categories

**Automation Enhancements**:
- New command types
- Alternative workflows
- Integration with other tools

**AI Improvements**:
- Better prompt patterns
- Smarter routing
- Quality improvements

**User Experience**:
- Better error messages
- Improved documentation
- New helper commands

**Performance**:
- Faster operations
- Better resource usage
- Optimization strategies

### Idea Template

**Idea**: [Brief description]

**Category**: [Automation / AI / UX / Performance]

**Benefit**: [What problem does it solve?]

**Risk**: [What could go wrong?]

**Effort**: [Low / Medium / High]

**Status**: [Not Started / In Progress / Testing / Abandoned]

**Notes**: [Additional context]

---

## 25.7 Sandbox Safety

### Safety Rules

**Never**:
- ❌ Enable sandbox features by default
- ❌ Run experiments without explicit user request
- ❌ Modify core files in experimental code
- ❌ Break existing functionality
- ❌ Hide experimental nature of features

**Always**:
- ✅ Require explicit enablement
- ✅ Clearly label experimental features
- ✅ Use dry-run when possible
- ✅ Log all experimental operations
- ✅ Provide easy way to disable

### Recovery

**If Experiment Goes Wrong**:
1. Disable sandbox: Set `sandbox.enabled = false`
2. Revert changes: Restore from git if needed
3. Review logs: Check `auto_master.log` for details
4. Document: Add to experiment log with "discard" decision
5. Learn: Understand what went wrong

**If Core Is Affected**:
1. Stop immediately
2. Restore from git backup
3. Review what happened
4. Fix any issues
5. Document the problem

<!-- SANDBOX_SECTION_END -->
