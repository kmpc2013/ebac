---
name: ask
description: Read-only Q&A skill for answering questions about the current project, repository context, configuration, and conversation state. Use when the user wants explanations, guidance, file references, or context without creating, editing, generating, or mutating anything.
---

# Ask

Use this skill to answer questions about context without changing anything.

## Rules

- Read files, configs, and available context to improve the answer.
- Do not write, edit, generate, refactor, or delete anything.
- Do not run mutating actions.
- If the user asks for a change, explain what would change and where, but do not execute it.
- If local context supports it, cite the relevant file path and line number.
- If information is missing, say what would need to be inspected next.

## Response style

- Be concise, direct, and natural.
- Prefer short answers that stay focused on the user's question.
- Separate facts from assumptions.

