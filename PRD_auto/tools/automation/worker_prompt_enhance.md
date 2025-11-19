# Enhancement Worker Prompt Template

You are helping to enhance a chunk of a Product Requirements Document (PRD) for a project called **{{PROJECT_NAME}}**.

## Context

This chunk is part of a longer PRD document (`prd.md`). The full project overview is provided below for context.

## Project Overview

{{PROJECT_OVERVIEW}}

---

## Your Task

Enhance the following chunk of the PRD. Your goal is to create a professional, improved version that:

1. **Preserves all information** – Do not remove or lose any content.

2. **Improves clarity and structure** – Rewrite for better readability, professional language, and logical flow.

3. **Expands vague parts** – Turn vague notes into:
   - Clear user stories
   - Explicit functional requirements
   - Non-functional requirements
   - Edge cases
   - Success criteria

4. **Marks assumptions** – If you infer or invent reasonable details, mark them as:
   ```
   [ASSUMPTION] <your assumption>
   ```

5. **Identifies open questions** – Mark unclear items as:
   ```
   [OPEN_QUESTION] <description>
   ```

6. **Preserves special markers** – Keep any existing `[ASSUMPTION]`, `[OPEN_QUESTION]`, `[DEPRECATED]`, or `PROMPT` blocks exactly as they are.

7. **Suggests prompt candidates** – If you identify opportunities for new AI prompts that should be added to the Prompt Library (Section 9), suggest them as:
   ```
   [PROMPT_CANDIDATE] <brief description of the prompt and where it would be used>
   ```

## Chunk Content

{{CHUNK_TEXT}}

---

## Output Format

You MUST wrap your improved chunk between these exact markers:

```
<<<IMPROVED_CHUNK_START>>>
... your improved markdown for this chunk ...
<<<IMPROVED_CHUNK_END>>>
```

After the improved chunk, provide a "Notes for This Chunk" section:

### Notes for This Chunk

- [ASSUMPTION] ... (if any)
- [OPEN_QUESTION] ... (if any)
- [PROMPT_CANDIDATE] ... (if any)

The improved chunk will be concatenated with other chunks to build the final `prd_enhanced.md`, so ensure it flows naturally and maintains proper Markdown structure.

