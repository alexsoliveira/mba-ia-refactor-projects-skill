# Audit Report Template

Purpose: exact Phase 2 report structure and ordering rules.

Use this template shape for every audit.

## Required Structure

1. Header block
2. Project metadata
3. Summary table
4. Findings sorted by severity (CRITICAL -> HIGH -> MEDIUM -> LOW)
5. Completion footer with confirmation prompt

## Render Policy (Mandatory)

- Use the literal template block below as the single source of truth for Phase 2 output.
- Replace placeholders only; do not rename sections.
- Keep markdown headings exactly (`## Summary`, `## Findings`).
- Keep findings headings exactly (`### [SEVERITY] Title`).
- Keep summary table as markdown pipe table (`| Severity | Count |`), never ASCII box table.
- Required marker check before presenting output:
  - Must contain: `## Summary`, `## Findings`, `| Severity | Count |`, and all four headings `### [CRITICAL]`, `### [HIGH]`, `### [MEDIUM]`, `### [LOW]`.
  - Must not contain: `┌┐└┘├┤┬┴┼│─`.
  - Must not contain Unicode dash separators: `—`, `–`, `———`.
  - Must contain summary total exactly as `**Total Findings: [N]**`.
  - Must contain both separator lines around `PHASE 2 COMPLETE`.
  - If check fails, regenerate and do not present invalid output.

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
- Do not replace the audit header with alternatives like `### PHASE 2: ...`; use `ARCHITECTURE AUDIT REPORT` exactly.
- Every finding must use markdown heading format: `### [SEVERITY] Title`.
- The `PHASE 2 COMPLETE` block with severity totals is mandatory before the confirmation prompt.
- `Project:`, `Stack:`, and `Files:` lines are mandatory in metadata section.
- `**Total Findings: [N]**` in summary and `Total Findings: [N]` in footer are both mandatory.
- Unicode dash separators (`—`, `–`, `———`) are invalid; use ASCII only.
- The footer must include the second `================================` line after `PHASE 2 COMPLETE`.
- No text is allowed after `Proceed with refactoring (Phase 3)? [y/n]`.
- If `MEDIUM < 2` or `LOW < 2`, the audit is invalid and must be regenerated.
- If finding headings are not in `### [SEVERITY] Title` format, the audit is invalid.
- If summary is not markdown pipe table format, the audit is invalid.
- `## Summary` and `## Findings` headings are mandatory (exact markdown level-2 format).
- Every finding must use exact line references only (`Line: N` or `Lines: N-M`), without ellipsis.
- Do not use bracket list style in Phase 1 values (e.g., `[dep1, dep2]`); use comma-separated text.
- Code snippets must be real source excerpts (3-5 lines), not placeholders (`...`, `# ...`) or pseudo-code.
- Avoid overly broad ranges like `Lines: 1-200`; use the smallest precise range that supports the finding.
- Final severity floor is mandatory: `MEDIUM >= 2` and `LOW >= 2`. Otherwise regenerate the audit.
- The summary table must be this markdown shape (no ASCII table):
  - `| Severity | Count |`
  - `|----------|-------|`
  - rows for `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`
- If output contains any box-drawing characters (`┌┐└┘├┤┬┴┼│─`), the audit is invalid and must be regenerated.
- Plain `Summary`/`Findings` without `##` is invalid and must be regenerated.

## Cross-Link

Detection source of truth: `references/anti-patterns.md`.
