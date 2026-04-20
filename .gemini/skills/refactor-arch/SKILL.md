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
4. **No imports break** after removing legacy files

### Output Format

Print Phase 3 completion summary using the structure shown in references, including:
- New MVC structure created
- Transformations applied (with ✓ checkmarks)
### Legacy Files Cleanup

After refactoring is validated:
1. Remove legacy files (old root file moved to `src/`)
2. Remove empty utility folders
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

## Execution Constraints

✓ **MUST** complete all 3 phases in order (no skipping)
✓ **MUST** wait for user confirmation after Phase 2
✓ **MUST** find minimum findings distribution (1 CRITICAL/HIGH, 2 MEDIUM, 2 LOW)
✓ **MUST** create proper MVC folder structure in Phase 3
✓ **MUST** clean up legacy files that were refactored into `src/`
✓ **MUST** remove empty utility folders created by MVC template
✓ **MUST** re-validate application boots after cleanup
✓ **MUST** validate all endpoints still respond after cleanup
✓ **MUST** save audit report to `reports/audit-project-{N}.md`
✗ **MUST NOT** modify files before Phase 2 confirmation
✗ **MUST NOT** skip phases
✗ **MUST NOT** leave legacy files in project root after refactoring
✗ **MUST NOT** leave empty folders in `src/` after cleanup

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