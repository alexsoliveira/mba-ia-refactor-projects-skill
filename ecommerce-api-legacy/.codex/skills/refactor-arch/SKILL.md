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
- `references/readme-update.md`

## Global Rules

- Technology agnostic: support Python/Flask and Node.js/Express at minimum.
- Invocation scope is single-project only:
  - Analyze, audit, and refactor only the project currently targeted by invocation path/CWD.
  - Do not run phases for sibling projects in the same invocation.
- For this challenge repository, treat the root `README.md` manual analysis as a compliance source for Phase 2:
  - Before finalizing the audit, compare findings against the `README.md` section for the current project.
  - The Phase 2 output must include at least 5 findings that correspond to manually documented issues for the current project when that section exists.
  - Prefer README-aligned findings before adding extra valid findings that are not part of the manual analysis.
  - If the README wording is stale but the same underlying issue still exists in source, keep the source-true description while preserving overlap with the manual-analysis theme.
  - This README alignment is a repository-specific compliance layer; it must not replace stack-agnostic detection heuristics or hardcode framework-specific logic into the skill.
- For this challenge repository, treat the root `README.md` pending placeholder sections as Phase 3 documentation debt:
  - `## Construção da Skill`
  - `## Resultados`
  - `## Como Executar`
  - When those sections still contain placeholder text such as `Descreva aqui`, Phase 3 must replace the placeholders with real repository-specific documentation.
  - Preserve the existing `## Análise Manual dos Projetos` content and do not overwrite unrelated sections.
  - Update shared README sections incrementally across runs: merge with existing content, do not duplicate headings, and only add or refresh the current project's result/checklist subsection when working on a single project.
- No preamble before Phase 1 template output.
- Use exact Phase 1 field order and labels.
- No narrative text between the end of Phase 1 and the start of Phase 2.
- Do not use emojis or decorative symbols in phase outputs.
- Use ASCII-only separators and punctuation in phase outputs (no Unicode dash variants).
- Phase 2 findings must be sorted by severity: CRITICAL, HIGH, MEDIUM, LOW.
- Every finding must include exact file and line or line range.
- Include deprecated API detection when applicable.
- End Phase 2 with confirmation prompt and stop.
- Only proceed to Phase 3 when user responds `y` or `yes`.
- Preserve behavior and endpoints after refactor.

## Report Persistence Rules (mandatory)

- At the end of Phase 2, persist only one report file for the current project in the repository root `reports/` directory (never inside project-local folders like `code-smells-project/reports/`):
  - `code-smells-project` -> `<REPO_ROOT>/reports/audit-project-1.md`
  - `ecommerce-api-legacy` -> `<REPO_ROOT>/reports/audit-project-2.md`
  - `task-manager-api` -> `<REPO_ROOT>/reports/audit-project-3.md`
- Resolve `<REPO_ROOT>` as the directory that contains `AGENTS.md` for this challenge repository.
- Do not create or overwrite other `reports/audit-project-*.md` files in the same run.
- If project identity cannot be resolved confidently, stop and ask for clarification before writing any report file.
- Before writing the report, resolve and verify the final absolute output path.
- If the resolved path is inside a project-local folder such as `code-smells-project/reports/`, `ecommerce-api-legacy/reports/`, or `task-manager-api/reports/`, do not write there; correct the target to `<REPO_ROOT>/reports/...` first.
- Treat writing to a project-local `reports/` directory as a compliance failure.

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
- The line immediately after `PHASE 1: PROJECT ANALYSIS` must be exactly `================================`.
- After Phase 1 closing separator, the next non-empty line must be the Phase 2 header.
- `Dependencies` and `DB tables` must be comma-separated plain text without brackets (`[]`).
- `Source files` must count only executable backend source files (exclude docs, lock/manifests, DB files, env files).

Phase 1 compliance gate (mandatory before printing):
- If source-file count includes non-source artifacts (e.g., `README.md`, `requirements.txt`, `.db`), recalculate before printing.
- If current project is `code-smells-project` baseline and `Source files != 4`, recalculate and regenerate Phase 1.
- If the separator line immediately below `PHASE 1: PROJECT ANALYSIS` is missing, regenerate Phase 1 before presenting.

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
- Additional required format checks before presenting:
  - No Unicode dash separators (`—`, `–`, `———`) anywhere in Phase 2 output.
  - Summary total line must be exactly `**Total Findings: [N]**`.
  - Footer must include the second separator line after `PHASE 2 COMPLETE`:
    - `================================`
    - `PHASE 2 COMPLETE`
    - `================================`

Requirements:
- Minimum 5 findings.
- Severity floor for compliance: at least 2 MEDIUM and at least 2 LOW findings.
- Findings sorted by severity (CRITICAL -> LOW).
- Each finding includes: `### [SEVERITY] Title`, `File: path, Line/Lines`, 3-5 line snippet, `Impact:`.
- Every finding snippet must be wrapped in fenced markdown code blocks with a language tag when the language is known.
- For this challenge repo, at least 5 findings must overlap with the current project's manual-analysis issues documented in the root `README.md`.
- When multiple valid findings are available, prefer README-overlap findings over supplemental findings once the minimum severity floor is satisfied.
- Snippets must include the exact offending line or lines that justify the finding, not just nearby setup context.
- Output text must preserve readable source strings and UTF-8 characters; mojibake such as `Ã`, `Â`, or replacement-garbage sequences is invalid.
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
- If fewer than 5 findings overlap with the current project's manual-analysis issues in the root `README.md`, continue auditing and replace lower-priority supplemental findings before printing.
- If any snippet is not inside fenced markdown code blocks, regenerate the report before printing.
- If any snippet omits the core offending line(s) that justify the finding, regenerate the report before printing.
- If output contains mojibake or visibly corrupted source strings, regenerate the report before printing.
- If the intended persisted report path is not the repository root `reports/audit-project-<N>.md` target for the current project, correct the path before printing.
- If output contains narrative or emojis, regenerate output before presenting to user.
- If output uses ASCII/box table characters (`┌ ┬ ┐ ├ ┼ ┤ └ ┴ ┘`), regenerate with markdown table.
- If any finding is formatted as `[SEVERITY] Title` without `###`, regenerate before presenting.
- If `PHASE 2 COMPLETE` block is missing, regenerate before presenting.
- If separator line immediately after `PHASE 2 COMPLETE` is missing, regenerate before presenting.
- If Phase 2 is missing `Project:`, `Stack:`, or `Files:` lines, regenerate before presenting.
- If `## Summary`, `## Findings`, or `**Total Findings: [N]**` is missing, regenerate before presenting.
- If summary contains `Total Findings: [N]` without markdown bold (`**...**`), regenerate before presenting.
- If output contains Unicode dash separators (`—`, `–`, `———`), regenerate before presenting.
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
- If the root `README.md` has manual-analysis findings for the current project and fewer than 5 audit findings overlap with them, do not print Phase 2.
- If metadata block is missing (`Project`, `Stack`, `Files`), do not print Phase 2.
- If summary table is not markdown pipe table, do not print Phase 2.
- If any finding title is not prefixed with `### [SEVERITY]`, do not print Phase 2.
- If any finding does not include exact line or exact line range (`Line: N` or `Lines: N-M`), do not print Phase 2.
- If any finding snippet is not fenced with triple backticks, do not print Phase 2.
- If any finding snippet does not show the exact line(s) that demonstrate the problem, do not print Phase 2.
- If output contains mojibake or broken character decoding, do not print Phase 2.
- If the report is persisted anywhere other than `<REPO_ROOT>/reports/audit-project-<N>.md` for the current project, do not consider Phase 2 complete.
- If any field value in Phase 1 uses bracketed list formatting (e.g., `[a, b, c]`), do not print; regenerate Phase 1.
- If any finding snippet is not an actual excerpt from source code, do not print Phase 2.
- If any finding uses non-specific references instead of precise ranges, do not print Phase 2.
- If summary is missing exact `**Total Findings: [N]**`, do not print Phase 2.
- If footer is missing the second `================================` line after `PHASE 2 COMPLETE`, do not print Phase 2.
- If output contains Unicode dash separators (`—`, `–`, `———`), do not print Phase 2.

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

================================

Proceed with refactoring (Phase 3)? [y/n]
```

Pre-output strict checks (run immediately before final Phase 2 print):
1. Verify `MEDIUM >= 2`. If false, continue auditing and regenerate.
2. Verify summary uses markdown table exactly with `|` separators.
3. If any box-drawing character exists (`┌┐└┘├┤┬┴┼│─`), reject output and regenerate using markdown table.
4. Verify headings are exactly `## Summary` and `## Findings` (not plain `Summary`/`Findings`).
5. Verify finding titles begin with `### [` (no plain `[CRITICAL]` form).
6. Verify summary contains exact markdown bold total line: `**Total Findings: [N]**`.
7. Verify footer contains both separator lines around `PHASE 2 COMPLETE`.
8. Verify output contains no Unicode dash separators (`—`, `–`, `———`).
9. Verify every finding snippet is fenced with triple backticks and uses a language tag when confidently known.
10. Verify every finding snippet includes the exact offending line or lines that justify the finding.
11. Verify output contains no mojibake or visibly corrupted source strings.

Additional strict check:
12. Verify at least 5 findings overlap with the root `README.md` manual-analysis issues for the current project, when that section exists.

## Challenge Alignment Hints

Use these only to improve overlap with the repository `README.md`; never invent issues that are absent from source.
These are semantic categories, not hardcoded implementation signatures. The audit must still infer findings from the current codebase first and only then prefer the best matching README-aligned categories.

- `code-smells-project` expected overlap candidates:
  - hardcoded credentials or insecure runtime config
  - N+1 order/item queries
  - missing layer boundaries or no service layer
  - duplicated validation or duplicated serialization
  - magic strings or magic numbers
  - inconsistent naming
- `ecommerce-api-legacy` expected overlap candidates:
  - hardcoded credentials
  - weak crypto or credential handling
  - missing auth on critical endpoints
  - callback hell or inline payment logic
  - mutable global state
  - magic strings or poor naming
- `task-manager-api` expected overlap candidates:
  - deprecated or insecure hashing
  - hardcoded secrets or email credentials
  - blocking notification flow
  - N+1 queries
  - duplicated serialization
  - generic exception handling or magic numbers

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
- Synchronize the root `README.md` using `references/readme-update.md` after validation succeeds.

Validation checklist:
- App starts without runtime errors.
- Original endpoints still respond.
- No refactor step started before Phase 2 confirmation.
- Root `README.md` no longer contains unresolved placeholder text in the sections covered by the current run.

README synchronization requirements (mandatory during Phase 3 for this challenge repo):
- Resolve the repository root README as the `README.md` that sits beside `AGENTS.md`.
- Use `references/readme-update.md` as the content contract for the three sections:
  - `## Construção da Skill`
  - `## Resultados`
  - `## Como Executar`
- Preserve user-authored content that is already concrete; replace only placeholders, stale boilerplate, or the subsection for the current project when refreshed evidence is available.
- In `## Resultados`, maintain per-project subsections and update only the current project's audit summary, before/after structure notes, validation checklist, and evidence/log summary for the invoked target project.
- In `## Como Executar`, keep commands for all 3 projects available once the section is populated; do not narrow the README to only the current project.
- Do not claim validation that was not actually executed during the current run; when evidence comes from the current run, state it concretely.
- If Phase 3 validation fails, do not mark checklist items as complete in `README.md`.

## Safety Gate

If user answers `n` or `no` after Phase 2:
- Stop without modifying files.
- Wait for revised instructions.
