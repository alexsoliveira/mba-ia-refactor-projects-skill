# Audit Report Template

Purpose: exact Phase 2 report structure and ordering rules.

Use this template shape for every audit.

## Required Structure

1. Header block
2. Project metadata
3. Summary table
4. Findings sorted by severity (CRITICAL -> HIGH -> MEDIUM -> LOW)
5. Completion footer with confirmation prompt

## Literal Template

```markdown
================================
ARCHITECTURE AUDIT REPORT
================================

Project: [PROJECT_NAME]
Stack:   [LANGUAGE] + [FRAMEWORK VERSION]
Files:   [N] analyzed | ~[LOC] LOC total

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | [N]   |
| HIGH     | [N]   |
| MEDIUM   | [N]   |
| LOW      | [N]   |

**Total Findings: [N]**

---

## Findings

### [CRITICAL] [TITLE]

File: [path/to/file], Line: [N] or Lines: [N-M]

[3-5 line code snippet showing the issue]

Impact: [one concise impact sentence]

---

### [HIGH] [TITLE]

File: [path/to/file], Line: [N] or Lines: [N-M]

[3-5 line code snippet showing the issue]

Impact: [one concise impact sentence]

---

### [MEDIUM] [TITLE]

File: [path/to/file], Line: [N] or Lines: [N-M]

[3-5 line code snippet showing the issue]

Impact: [one concise impact sentence]

---

### [LOW] [TITLE]

File: [path/to/file], Line: [N] or Lines: [N-M]

[3-5 line code snippet showing the issue]

Impact: [one concise impact sentence]

---

================================
PHASE 2 COMPLETE
================================

Total Findings: [N]
  - CRITICAL: [N]
  - HIGH: [N]
  - MEDIUM: [N]
  - LOW: [N]

Proceed with refactoring (Phase 3)? [y/n]
```

## Mandatory Rules

- Always include exact file and line information.
- Include deprecated API finding if applicable.
- Do not propose implementation steps in Phase 2.
- Stop after the confirmation prompt.
- Use markdown table format (`| Severity | Count |`) only; ASCII/box tables are invalid.
- Output at least 2 MEDIUM findings and at least 2 LOW findings before closing Phase 2.
- Do not print narrative text between Phase 1 completion and the Phase 2 header.

## Cross-Link

Detection source of truth: `references/anti-patterns.md`.
