# README Update Contract

Purpose: define how Phase 3 must update the repository root `README.md` so the challenge deliverable is complete and no placeholder sections remain pending.

This reference applies only to the challenge repository root `README.md` that sits beside `AGENTS.md`.

## Sections That Must Be Populated

Phase 3 must ensure these sections contain real content instead of placeholders:
- `## Construção da Skill`
- `## Resultados`
- `## Como Executar`

Do not remove or rewrite the existing `## Análise Manual dos Projetos` section except when explicitly asked by the user.

## Update Strategy

- Preserve existing concrete content written by the user when it is still accurate.
- Replace placeholder text such as `Descreva aqui ...`.
- Merge incrementally across runs; do not duplicate headings or create parallel copies of the same section.
- Because each invocation is single-project scoped, update the current project's subsection in `## Resultados` and preserve the other projects' subsections when they already exist.
- If a shared section is still empty or placeholder-only, populate it with repository-level guidance that applies to all projects.

## Content Contract

### 1) `## Construção da Skill`

This section should describe the skill as a reusable solution for the 3 projects. Include:
- How `SKILL.md` is organized around the 3 mandatory phases.
- Which reference files exist and what each one contributes.
- Which anti-pattern families are covered and why they were chosen.
- How the skill stays technology-agnostic across Flask and Express projects.
- How README alignment, report persistence, and safety gates were enforced.
- Main challenges and the design choices used to solve them.

Recommended subsection headings:
- `### Estrutura do SKILL.md`
- `### Arquivos de Referência`
- `### Catálogo de Anti-Patterns`
- `### Estratégia Agnóstica de Tecnologia`
- `### Salvaguardas e Compliance`
- `### Desafios Encontrados`

### 2) `## Resultados`

This section should be cumulative and keep one subsection per project.

For the current project, include:
- Audit summary with finding counts by severity, sourced from the saved Phase 2 report.
- Brief before/after structure comparison.
- A filled validation checklist for the current project based only on evidence actually verified.
- Short evidence/log summary of boot and endpoint checks.
- Notes on how the skill adapted to this project's architecture maturity.

Recommended subsection headings:
- `### Projeto 1 - code-smells-project`
- `### Projeto 2 - ecommerce-api-legacy`
- `### Projeto 3 - task-manager-api`

Recommended per-project shape:
- `#### Resumo da Auditoria`
- `#### Antes e Depois`
- `#### Checklist de Validação`
- `#### Evidências`
- `#### Observações`

Checklist format:
- Use Markdown checkboxes.
- Mark `[x]` only when the current run produced or verified the evidence.
- Leave `[ ]` for items not verified yet.

### 3) `## Como Executar`

This section is repository-wide and should not depend on a single project only.

Include:
- Prerequisites for the chosen tool and local runtimes.
- Commands to invoke the skill in each of the 3 projects.
- Where audit reports are saved.
- How to validate boot and endpoint behavior after refactoring.

Recommended subsection headings:
- `### Pré-requisitos`
- `### Execução por Projeto`
- `### Relatórios Gerados`
- `### Como Validar`

## Evidence Rules

- Never state that all endpoints were validated unless that was actually checked.
- If only key endpoints were exercised, say `endpoints principais` or equivalent.
- If evidence came from terminal output during the current run, summarize it faithfully.
- If a project still has open validation gaps, keep them visible in the checklist instead of marking them complete.

## Style Rules

- Write in Portuguese to match the repository README.
- Keep content concise but concrete.
- Prefer challenge-specific wording over generic filler.
- Avoid placeholders, TODOs, and vague claims like `a aplicação foi validada` without saying how.

## Minimal Acceptance For README Synchronization

The README update performed in Phase 3 should satisfy all of these:
- No placeholder text remains in the 3 targeted sections.
- `## Resultados` contains a subsection for the current project.
- The current project's checklist reflects real verification status.
- `## Como Executar` includes commands for all 3 projects.
- The section content matches the actual structure and reports present in the repository.
