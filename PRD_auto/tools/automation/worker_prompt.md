# Worker Prompt Template

You are helping to process a chunk of a Product Requirements Document (PRD) for a project called **{{PROJECT_NAME}}**.

## Context

This chunk is part of a longer PRD document (`prd.md`). The full project overview is provided below for context.

## Project Overview

{{PROJECT_OVERVIEW}}

---

## Your Task

Process the following chunk of the PRD. Your goal is to:

1. **Preserve all information and meaning** – Do not remove or lose any content from the original chunk.

2. **Improve clarity and structure** – Rewrite for better readability, professional language, and logical flow.

3. **Expand vague parts** – Where appropriate, turn vague notes into:
   - Clear user stories
   - Explicit functional requirements
   - Non-functional requirements
   - Edge cases
   - Success criteria

4. **Mark assumptions** – If you need to infer or invent reasonable details that aren't explicitly stated, mark them as:
   ```
   [ASSUMPTION] <your assumption>
   ```

5. **Identify open questions** – If something is unclear, ambiguous, or requires a decision, mark it as:
   ```
   [OPEN_QUESTION] <description of what needs clarification>
   ```

6. **Preserve special markers** – Keep any existing `[ASSUMPTION]`, `[OPEN_QUESTION]`, `[DEPRECATED]`, or `PROMPT` blocks exactly as they are.

## Chunk Content

{{CHUNK_TEXT}}

---

## Output Format

Provide your improved version of this chunk in clean Markdown format. No special markers are required around your output – just the improved markdown content.

