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

## PHASE 2 - ARCHITECTURE AUDIT (must run second)

Use:
- `references/anti-patterns.md` for detection catalog and severity
- `references/report-template.md` for exact report format

Requirements:
- Minimum 5 findings.
- Severity floor for compliance: at least 2 MEDIUM and at least 2 LOW findings.
- Findings sorted by severity (CRITICAL -> LOW).
- Each finding includes: `### [SEVERITY] Title`, `File: path, Line/Lines`, 3-5 line snippet, `Impact:`.
- Include deprecated API finding if applicable.
- Use markdown summary table only. Do not use ASCII/box-drawing tables.
- Do not include proposed refactoring plan text in Phase 2.
- End with this exact prompt and stop:

```
Proceed with refactoring (Phase 3)? [y/n]
```

No mutation is allowed before user confirmation.

Compliance gate (mandatory before printing Phase 2):
- If `MEDIUM < 2` or `LOW < 2`, continue auditing and do not print final Phase 2 output yet.
- If any finding lacks exact file + line/lines, continue auditing and do not print final Phase 2 output yet.
- If output contains narrative or emojis, regenerate output before presenting to user.

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
