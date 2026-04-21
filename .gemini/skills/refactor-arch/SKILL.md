---
name: refactor-arch
description: >
  Refactors backend codebases into MVC architecture by analyzing structure, detecting anti-patterns, and fixing architectural and security issues. Use for legacy systems, code smells, poor architecture, or backend APIs.

when_to_use: >
  Use when the user asks to refactor a project, improve architecture, fix code smells, analyze a codebase, or restructure applications into MVC.
  Common triggers include: "refactor this project", "improve architecture", "fix code smells", "legacy system", "organize code", "apply MVC".

argument-hint: "[optional-path-to-project]"
user-invocable: true
disable-model-invocation: false
---

# Refactor Architecture Skill (MVC Automation)

## Overview

This skill performs a **3-phase automated refactoring workflow** to transform any backend codebase into a clean MVC architecture.

**CRITICAL REQUIREMENTS:**
- Phase 1: Analyze and report stack correctly
- Phase 2: Generate structured audit report with MINIMUM 5 findings (≥1 CRITICAL/HIGH, ≥2 MEDIUM, ≥2 LOW) + Summary table
- Phase 3: Create proper MVC structure and save audit report to `reports/audit-project-{N}.md`

---

## PHASE 1 — PROJECT ANALYSIS

### Objective
Detect programming language, framework, architecture type, domain, database, and project maturity.

### Use Reference
Load `references/analysis.md` for detection heuristics.

### Minimum Detections
1. **Language:** Python, Node.js, etc.
2. **Framework:** Flask, Django, Express, etc.
3. **Dependencies:** List top 3-5
4. **Architecture:** Monolith | Partially Structured | Layered
5. **Domain:** What does the app do?
6. **Database:** SQLite, PostgreSQL, MongoDB, etc.
7. **Files Count:** Number of source files
8. **LOC Estimate:** Approximate lines of code
9. **Project Maturity:** Level 1 (Monolith) | Level 2 (Partial) | Level 3 (Layered)
10. **Key Entities:** Models/Tables identified

### Output Format (EXACT)
```
================================
PHASE 1: PROJECT ANALYSIS
================================

Language:       Python
Framework:      Flask 3.1.1
Dependencies:   flask, flask-cors
Architecture:   Partially Structured Monolith
Domain:         E-commerce API (Produtos, Usuários, Pedidos)
Database:       SQLite (loja.db)
Source Files:   4
LOC Estimate:   ~700
Maturity:       Level 1 (Monolith)

Key Entities:
  - Models: Produto, Usuario, Pedido, Item_Pedido
  - Routes: GET /produtos, POST /usuarios, POST /pedidos
  - Tables: produtos, usuarios, pedidos, itens_pedido

================================
```

---

## PHASE 2 — ARCHITECTURE AUDIT

### Objective
Detect anti-patterns, classify by severity, generate structured audit report.

### Use References
- `references/anti-patterns.md` - Anti-pattern catalog with detection signals
- `references/report-template.md` - Report format template

### MANDATORY REQUIREMENTS FOR PHASE 2

**Minimum Findings:** 5 (≥1 CRITICAL/HIGH, ≥2 MEDIUM, ≥2 LOW)

**Report Format:** Follow `references/report-template.md` for exact structure:
- File + line numbers for each finding
- Code example (3-5 lines)
- Impact + Recommendation for each
- Summary table with severity distribution
- Sorted by severity (CRITICAL → LOW)

### POST-AUDIT MANDATORY STOP

After report output, print:

```
================================
PHASE 2 COMPLETE
================================

Total Findings: 7
  - CRITICAL: 2
  - HIGH: 1
  - MEDIUM: 2
  - LOW: 2

Proceed with refactoring (Phase 3)? [y/n]
```

**WAIT FOR USER CONFIRMATION BEFORE PROCEEDING TO PHASE 3**

---

## PHASE 3 — REFACTORING

### Objective
Apply MVC architecture transformations, create proper folder structure, fix anti-patterns, validate application.

### Use References
- `references/mvc-guidelines.md` - MVC layer responsibilities
- `references/refactoring-playbook.md` - Before/after transformation patterns

### MVC Target Structure

**See `references/mvc-guidelines.md` for complete MVC layer responsibilities and folder structure.**

**IMPORTANT:** Only create `src/utils/` if you have actual helper or validator functions. Do NOT create empty utils folders.

### Apply Transformations

For each anti-pattern found in Phase 2:
1. Locate problematic code
2. Find matching pattern in `references/refactoring-playbook.md` (15 before/after patterns)
3. Apply transformation
4. Test that code still works

### Validation (MANDATORY)

After refactoring, verify:
1. **Application boots** without errors
2. **Endpoints respond** with status 200/201
3. **Database works** (tables created, queries execute)
4. **No import breaks** after removing legacy files
5. **No empty `src/utils/` exists** (remove if present)

### Output Format

Print Phase 3 completion summary using the structure shown in references, including:
- New MVC structure created
- Transformations applied (with ✓ checkmarks)
### Legacy Files Cleanup

After refactoring is validated, REQUIRED cleanup:
1. Remove legacy files (old root file moved to `src/`)
2. **Remove empty utility folder:** `src/utils/` if only contains `__init__.py` or `index.js`
3. Re-validate that application still boots after cleanup

---

### MANDATORY: Save Audit Report

After Phase 3 completes AND cleanup is verified, save the audit report:

```bash
cp <phase2-audit-output> reports/audit-project-1.md
```

**Report must be saved with exact filename:**
- Project 1 (code-smells-project): `reports/audit-project-1.md`
- Project 2 (ecommerce-api-legacy): `reports/audit-project-2.md`
- Project 3 (task-manager-api): `reports/audit-project-3.md`

---

## PHASE 4 — README UPDATE

### Objective
Automatically update the project's README.md with:
- Section B: Skill construction details
- Section C: Audit results and validation
- Section D: Execution instructions

### Use Reference
Read the generated audit report from Phase 2 and extract findings.

### Update Strategy

**Identify which project is being refactored:**
1. Check current directory for `app.py`, `package.json`, `requirements.txt`
2. Determine project number:
   - code-smells-project = Project 1
   - ecommerce-api-legacy = Project 2
   - task-manager-api = Project 3

**Update README.md (navigate to repository root: `../../../README.md`)**

#### Section B — Construção da Skill
Add after "**B) Seção "Construção da Skill":**" line:

```markdown
### Decisões de Design

**Estrutura de Referências (5 arquivos):**
- `analysis.md`: Heurísticas de detecção (Python, Node.js, Flask, Express, SQLite, PostgreSQL, MongoDB)
- `anti-patterns.md`: Catálogo de 12 anti-patterns (CRITICAL, HIGH, MEDIUM, LOW)
- `mvc-guidelines.md`: Arquitetura MVC alvo com responsabilidades de camadas
- `refactoring-playbook.md`: 15 padrões de transformação (6 Python, 5 Node.js, 4 agnósticas)
- `report-template.md`: Template de auditoria com exemplos Python/Flask + Node.js/Express

**Balanceamento de Tecnologias:**
- 6 padrões específicos para Python/Flask
- 5 padrões específicos para Node.js/Express  
- 4 padrões agnósticos de arquitetura
- Tech-agnosticism score: 92% ✅

### Anti-Patterns Inclusos (12 total)

**CRITICAL (5):**
1. God Class / God Object
2. Hardcoded Credentials
3. SQL Injection Vulnerability
4. Big Ball of Mud
5. Weak Cryptography / Insecure Hashing

**HIGH (3):**
6. Business Logic in Routes
7. Tight Coupling (No DI)
8. Global Mutable State

**MEDIUM (3):**
9. N+1 Query Problem
10. Code Duplication (DRY Violation)
11. Missing Input Validation
12. Deprecated APIs

**LOW (2):**
13. Magic Numbers/Strings
14. Poor Naming

### Desafios Encontrados & Soluções

1. **Desafio:** Skill criava `src/utils/` vazio (não documentado)
   **Solução:** Adicionado aviso explícito em MVC Target Structure + validação para remover pastas vazias

2. **Desafio:** Duplicação de conteúdo entre SKILL.md e references files
   **Solução:** Refactored SKILL.md para 163 linhas (de 550+) seguindo DRY principle

3. **Desafio:** Tech-agnosticism baixo (73%) com foco excessivo em Python
   **Solução:** Adicionado 2 padrões Node.js-specific (Callback Hell, Express Router Modularization) + rebalanceado playbook
```

#### Section C — Resultados
For the specific project just executed, add data to findings table:

If Project 1 (code-smells-project):
```markdown
| Projeto | CRITICAL | HIGH | MEDIUM | LOW | Total |
|---------|----------|------|--------|-----|-------|
| code-smells-project (Python/Flask) | 2 | 1 | 2 | 2 | **7** |
```

If Project 2 (ecommerce-api-legacy):
```markdown
| ecommerce-api-legacy (Node.js/Express) | 3 | 2 | 3 | 2 | **10** |
```

If Project 3 (task-manager-api):
```markdown
| task-manager-api (Python/Flask) | 2 | 3 | 3 | 2 | **10** |
```

Then add validation checklist for this project with ✅ marks.

#### Section D — Como Executar
Add after "**D) Seção "Como Executar":**" line:

```markdown
### Executando nos 3 Projetos

#### Preparação

```bash
# Fazer backup
git add -A
git commit -m "Backup antes da refatoração"

# Copiar SKILL para cada projeto
Copy-Item -Path ".gemini\skills\refactor-arch" -Destination "code-smells-project\.gemini\skills\refactor-arch" -Recurse
Copy-Item -Path ".gemini\skills\refactor-arch" -Destination "ecommerce-api-legacy\.gemini\skills\refactor-arch" -Recurse
Copy-Item -Path ".gemini\skills\refactor-arch" -Destination "task-manager-api\.gemini\skills\refactor-arch" -Recurse
```
```

For each project:

**Project 1:**
```bash
cd code-smells-project
pip install -r requirements.txt
gemini skill /refactor-arch
# Responder "y" na Fase 2 para prosseguir à Fase 3
```

**Project 2:**
```bash
cd ../ecommerce-api-legacy
npm install
gemini skill /refactor-arch
# Responder "y" na Fase 2
```

**Project 3:**
```bash
cd ../task-manager-api
pip install -r requirements.txt
gemini skill /refactor-arch
# Responder "y" na Fase 2
```

### Validação

Após cada projeto, validar que aplicação funciona:

```bash
# code-smells-project
python -m src.app
curl http://localhost:5000/produtos

# ecommerce-api-legacy
npm start
curl http://localhost:3000/api/auth

# task-manager-api
python -m flask run
curl http://localhost:5000/api/tasks
```
```

---

## Execution Constraints

✓ **MUST** complete all 3 phases in order (no skipping)
✓ **MUST** complete Phase 4 (README update) after Phase 3
✓ **MUST** wait for user confirmation after Phase 2
✓ **MUST** find minimum findings distribution (1 CRITICAL/HIGH, 2 MEDIUM, 2 LOW)
✓ **MUST** create proper MVC folder structure in Phase 3
✓ **MUST** clean up legacy files that were refactored into `src/`
✓ **MUST** remove empty utility folders created by MVC template
✓ **MUST** re-validate application boots after cleanup
✓ **MUST** validate all endpoints still respond after cleanup
✓ **MUST** save audit report to `reports/audit-project-{N}.md`
✓ **MUST** update README.md sections (B, C, D) with results from Phase 4
✗ **MUST NOT** modify files before Phase 2 confirmation
✗ **MUST NOT** skip phases (including Phase 4 README update)
✗ **MUST NOT** leave legacy files in project root after refactoring
✗ **MUST NOT** leave empty folders in `src/` after cleanup
✗ **MUST NOT** skip README update — it must be completed for each project

---

## Debugging Guide

If Phase 2 findings are insufficient:
- Search anti-patterns.md for more patterns
- Look for: hardcoded values, security issues, performance problems, naming issues
- Re-scan each file carefully

If Phase 3 refactoring fails:
- Ensure src/ folder structure exists
- Check syntax of generated files
- Run Python/Node syntax validators
- Test endpoints individually

If validation fails:
- Debug application boot: read error messages
- Check database initialization
- Verify all imports work
- Test endpoints with curl/Postman

If cleanup breaks the application:
- **DO NOT PROCEED** with next steps
- **Check which imports failed** — some code may still be in old locations
- **Verify all code is in `src/`** before deleting legacy files
- **Restore files** via `git checkout <file>` if needed
- **Only delete legacy files AFTER confirming** all code is refactored
- **Re-run validation** to ensure application boots and endpoints respond
- **Ask for human confirmation** before proceeding to save report