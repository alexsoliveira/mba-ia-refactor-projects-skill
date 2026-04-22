---
name: refactor-arch
description: >
  Analyze, audit, and refactor backend codebases into MVC using a strict 3-phase workflow.
when_to_use: >
  Use when user asks to analyze architecture, detect anti-patterns, or refactor legacy backend projects to MVC.
argument-hint: "[optional-path-to-project]"
user-invocable: true
disable-model-invocation: false
---

# Refactor Arch Skill (Gemini, Literal Mode)

This skill MUST follow exactly 3 phases:
1. Phase 1 - Analysis
2. Phase 2 - Audit
3. Phase 3 - Refactoring (only after explicit confirmation)

Do not add extra phases. Do not mutate files before Phase 2 confirmation.

References:
- `references/analysis.md`
- `references/anti-patterns.md`
- `references/report-template.md`
- `references/mvc-guidelines.md`
- `references/refactoring-playbook.md`

## Global Rules

- Technology agnostic: support Python/Flask and Node.js/Express at minimum.
- No preamble before Phase 1 template output.
- Use exact Phase 1 field order and labels.
- No narrative text between the end of Phase 1 and the start of Phase 2.
- Do not use emojis or decorative symbols in phase outputs.
- Phase 2 findings must be sorted by severity: CRITICAL, HIGH, MEDIUM, LOW.
- Every finding must include exact file and line or line range.
- Include deprecated API detection when applicable.
- End Phase 2 with confirmation prompt and stop.
- Only proceed to Phase 3 when user responds `y` or `yes`.
- Preserve behavior and endpoints after refactor.

## PHASE 1 - PROJECT ANALYSIS (must run first)

Use `references/analysis.md` heuristics to detect:
- Language
- Framework (with version)
- Dependencies (top 3-5)
- Domain
- Architecture
- Source files analyzed
- DB tables

Output MUST be exactly this structure (replace values only):

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      [LANGUAGE]
Framework:      [FRAMEWORK AND VERSION]
Dependencies:  [DEPENDENCY_1, DEPENDENCY_2, DEPENDENCY_3]
Domain:        [APPLICATION DOMAIN]
Architecture:  [CURRENT ARCHITECTURE]
Source files:  [N] files analyzed
DB tables:     [TABLE_1, TABLE_2, TABLE_3]
================================
```

Constraints:
- No extra fields.
- No text before or after template block.
- Keep field order exactly as shown.
- The first and last separator lines in Phase 1 must be exactly `================================`.
- After Phase 1 closing separator, the next non-empty line must be the Phase 2 header.
- `Dependencies` and `DB tables` must be comma-separated plain text without brackets (`[]`).
- `Source files` must count only executable backend source files (exclude docs, lock/manifests, DB files, env files).

Phase 1 compliance gate (mandatory before printing):
- If source-file count includes non-source artifacts (e.g., `README.md`, `requirements.txt`, `.db`), recalculate before printing.
- If current project is `code-smells-project` baseline and `Source files != 4`, recalculate and regenerate Phase 1.

## PHASE 2 - ARCHITECTURE AUDIT (must run second)

Use:
- `references/anti-patterns.md` for detection catalog and severity
- `references/report-template.md` for exact report format

Deterministic render mode (mandatory):
- Build Phase 2 by copying the fenced template from `references/report-template.md` literally.
- Replace placeholders only (`[PROJECT_NAME]`, `[N]`, `[TITLE]`, etc.).
- Do not rewrite section names or table format.
- If generated output diverges from template shape, regenerate before presenting.

Phase 2 non-negotiable output contract (highest priority):
- The output MUST contain these exact markers before it is shown to user:
  - `## Summary`
  - `## Findings`
  - `| Severity | Count |`
  - `### [CRITICAL]`
  - `### [HIGH]`
  - `### [MEDIUM]`
  - `### [LOW]`
- The output MUST NOT contain box-table characters:
  - `┌┐└┘├┤┬┴┼│─`
- If any required marker is missing, or any forbidden character appears, regenerate silently and do not present the invalid version.

Requirements:
- Minimum 5 findings.
- Severity floor for compliance: at least 2 MEDIUM and at least 2 LOW findings.
- Findings sorted by severity (CRITICAL -> LOW).
- Each finding includes: `### [SEVERITY] Title`, `File: path, Line/Lines`, 3-5 line snippet, `Impact:`.
- Include deprecated API finding if applicable.
- Use markdown summary table only. Do not use ASCII/box-drawing tables.
- Do not include proposed refactoring plan text in Phase 2.
- Phase 2 header MUST be exactly:
  - `================================`
  - `ARCHITECTURE AUDIT REPORT`
  - `================================`
- Phase 2 MUST include section headers exactly: `## Summary` and `## Findings`.
- Every finding title MUST start with `### [CRITICAL]`, `### [HIGH]`, `### [MEDIUM]`, or `### [LOW]`.
- Phase 2 footer MUST include exactly:
  - `================================`
  - `PHASE 2 COMPLETE`
  - `================================`
  - `Total Findings: [N]`
  - `  - CRITICAL: [N]`
  - `  - HIGH: [N]`
  - `  - MEDIUM: [N]`
  - `  - LOW: [N]`
  - the confirmation prompt.
- End with this exact prompt and stop:

```
Proceed with refactoring (Phase 3)? [y/n]
```

No mutation is allowed before user confirmation.

Compliance gate (mandatory before printing Phase 2):
- If `MEDIUM < 2` or `LOW < 2`, continue auditing and do not print final Phase 2 output yet.
- If any finding lacks exact file + line/lines, continue auditing and do not print final Phase 2 output yet.
- If output contains narrative or emojis, regenerate output before presenting to user.
- If output uses ASCII/box table characters (`┌ ┬ ┐ ├ ┼ ┤ └ ┴ ┘`), regenerate with markdown table.
- If any finding is formatted as `[SEVERITY] Title` without `###`, regenerate before presenting.
- If `PHASE 2 COMPLETE` block is missing, regenerate before presenting.
- If Phase 2 is missing `Project:`, `Stack:`, or `Files:` lines, regenerate before presenting.
- If `## Summary`, `## Findings`, or `**Total Findings: [N]**` is missing, regenerate before presenting.
- If any text appears after `Proceed with refactoring (Phase 3)? [y/n]`, regenerate before presenting.
- If `Summary`/`Findings` appear without markdown level-2 headings (`##`), regenerate before presenting.
- If any finding line reference contains ellipsis (`...`) or missing line numbers, regenerate before presenting.
- If `## Summary` and `## Findings` are not present exactly, regenerate before presenting.
- If summary table is not markdown pipe format (`| Severity | Count |`), regenerate before presenting.
- If finding titles are not markdown level-3 (`### [SEVERITY] Title`), regenerate before presenting.
- If any code snippet uses placeholders like `...`, `# ...`, or paraphrased pseudo-code, regenerate with real code lines.
- If any line range is overly broad (e.g., `Lines: 1-200`), regenerate with precise ranges per issue.

Hard failure conditions (must not present output to user):
- If `LOW < 2`, do not print Phase 2; continue analysis until at least 2 LOW findings are documented.
- If `MEDIUM < 2`, do not print Phase 2; continue analysis until at least 2 MEDIUM findings are documented.
- If metadata block is missing (`Project`, `Stack`, `Files`), do not print Phase 2.
- If summary table is not markdown pipe table, do not print Phase 2.
- If any finding title is not prefixed with `### [SEVERITY]`, do not print Phase 2.
- If any finding does not include exact line or exact line range (`Line: N` or `Lines: N-M`), do not print Phase 2.
- If any field value in Phase 1 uses bracketed list formatting (e.g., `[a, b, c]`), do not print; regenerate Phase 1.
- If any finding snippet is not an actual excerpt from source code, do not print Phase 2.
- If any finding uses non-specific references instead of precise ranges, do not print Phase 2.

Literal Phase 2 skeleton to enforce (must match shape):
```
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
...

### [HIGH] [TITLE]
...

### [MEDIUM] [TITLE]
...

### [LOW] [TITLE]
...

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

Pre-output strict checks (run immediately before final Phase 2 print):
1. Verify `MEDIUM >= 2`. If false, continue auditing and regenerate.
2. Verify summary uses markdown table exactly with `|` separators.
3. If any box-drawing character exists (`┌┐└┘├┤┬┴┼│─`), reject output and regenerate using markdown table.
4. Verify headings are exactly `## Summary` and `## Findings` (not plain `Summary`/`Findings`).
5. Verify finding titles begin with `### [` (no plain `[CRITICAL]` form).

## PHASE 3 - REFACTORING (only after explicit confirmation)

Only execute if user answered `y` or `yes` after Phase 2.

Use:
- `references/mvc-guidelines.md` as target architecture
- `references/refactoring-playbook.md` for concrete transformations

Required outcomes:
- Separate responsibilities into MVC layers.
- Remove or mitigate findings from Phase 2.
- Keep existing endpoint behavior.
- Validate application boot.
- Validate key endpoints respond correctly.

Validation checklist:
- App starts without runtime errors.
- Original endpoints still respond.
- No refactor step started before Phase 2 confirmation.

## Safety Gate

If user answers `n` or `no` after Phase 2:
- Stop without modifying files.
- Wait for revised instructions.
