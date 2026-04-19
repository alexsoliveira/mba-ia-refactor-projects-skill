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

**Minimum Findings:** 5 findings
**Distribution Required:**
- At least 1 CRITICAL or HIGH
- At least 2 MEDIUM
- At least 2 LOW

**Each Finding MUST Include:**
1. Severity: [CRITICAL] [HIGH] [MEDIUM] [LOW]
2. Title: Clear, actionable name
3. File: Exact file path
4. Lines: Specific line numbers (e.g., "10-15" or "23")
5. Description: 2-3 sentences explaining the issue
6. Code Example: Show the problematic code (3-5 lines)
7. Impact: 2-3 concrete consequences
8. Recommendation: Specific solution with modern alternative

**Report MUST Include Summary Table:**
```
| Severity | Count |
|----------|-------|
| CRITICAL | X     |
| HIGH     | Y     |
| MEDIUM   | Z     |
| LOW      | W     |
```

### STRICT FINDINGS CHECK
Before outputting report, verify:
- [ ] Total findings >= 5
- [ ] At least 1 CRITICAL or HIGH
- [ ] At least 2 MEDIUM (if not found, search harder!)
- [ ] At least 2 LOW (if not found, search harder!)
- [ ] Each finding has file + lines
- [ ] Each finding has code example
- [ ] Each finding has impact + recommendation
- [ ] Summary table present
- [ ] Findings sorted by severity (CRITICAL → HIGH → MEDIUM → LOW)

### Output Format (EXACT)

```
================================
ARCHITECTURE AUDIT REPORT
================================

Project: code-smells-project
Stack:   Python + Flask
Files:   4 analyzed | ~700 LOC total

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 2     |
| HIGH     | 1     |
| MEDIUM   | 2     |
| LOW      | 2     |

**Total Findings: 7**

---

## Findings

### [CRITICAL] Finding 1 Title

**File:** code-smells-project/app.py
**Lines:** 9-10
**Severity:** CRITICAL

**Description:**
Brief explanation of the problem.

**Code Example:**
\`\`\`python
app.config["SECRET_KEY"] = "dev-key-keep-it-safe"
\`\`\`

**Impact:**
- Session hijacking possible
- Token forgery risk
- Compliance violation

**Recommendation:**
Use environment variables: `os.environ.get("SECRET_KEY")`

---

### [CRITICAL] Finding 2 Title

[Continue for all findings...]

---

### [MEDIUM] Finding 5 Title

[At least 2 MEDIUM findings required]

---

### [LOW] Finding 7 Title

[At least 2 LOW findings required]

================================
```

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

### MVC Structure to Create

```
src/
├── config/
│   ├── __init__.py
│   ├── settings.py           # Configuration (no hardcoded values)
│   ├── database.py           # Database setup
│   └── constants.py          # Enums, magic numbers → constants
│
├── models/
│   ├── __init__.py
│   ├── base_model.py         # Base model class (if needed)
│   ├── user.py               # User model
│   ├── product.py            # Product model
│   ├── order.py              # Order model
│   └── ...                   # Other domain models
│
├── controllers/
│   ├── __init__.py
│   ├── user_controller.py    # User business logic
│   ├── product_controller.py # Product business logic
│   ├── order_controller.py   # Order business logic
│   └── ...                   # Other controllers
│
├── views/
│   ├── __init__.py
│   ├── user_routes.py        # User endpoints
│   ├── product_routes.py     # Product endpoints
│   ├── order_routes.py       # Order endpoints
│   └── ...                   # Other route blueprints
│
├── services/
│   ├── __init__.py
│   ├── email_service.py      # Email (async if possible)
│   ├── payment_service.py    # Payment processing
│   └── ...                   # Business services
│
├── middlewares/
│   ├── __init__.py
│   ├── auth_middleware.py    # Authentication
│   ├── error_handler.py      # Error handling
│   └── logging_middleware.py # Logging
│
├── utils/
│   ├── __init__.py
│   ├── helpers.py
│   └── validators.py
│
├── app.py                    # App initialization (entry point)
└── database.py               # Database connection helper

reports/
└── audit-project-1.md        # Save Phase 2 report here
```

### Key Transformations (Apply Using Playbook)

1. **Extract Configuration** → `src/config/settings.py`
   - Remove hardcoded SECRET_KEY, DEBUG flags, API keys
   - Use environment variables

2. **Fix Security Issues**
   - Replace MD5 hashing with bcrypt/argon2
   - Fix SQL injection with parameterized queries
   - Add authentication middleware to protected endpoints
   - Remove exposed credentials

3. **Eliminate N+1 Queries**
   - Replace nested loops with JOIN queries
   - Use eager loading

4. **Extract Business Logic**
   - Create Service Layer for complex operations
   - Keep Controllers thin (validation + orchestration)
   - Keep Routes simple (just HTTP handling)

5. **Fix Blocking I/O**
   - Move email/slow operations to async queues
   - Use background jobs if appropriate

6. **Centralize Error Handling**
   - Create error middleware
   - Structured error responses

### Apply Transformations

For each anti-pattern found in Phase 2:
1. Locate problematic code
2. Find matching pattern in `references/refactoring-playbook.md`
3. Apply before/after transformation
4. Test that code still works

### Validation (MANDATORY)

After refactoring:

1. **Application Must Boot**
   - Python: `python src/app.py` → runs without errors
   - Node: `npm start` → runs without errors

2. **Endpoints Must Respond**
   - GET /products → returns 200
   - GET /users → returns 200
   - POST /orders → returns 200 (if endpoint exists)
   - Include actual curl commands or test output

3. **Database Must Work**
   - Tables created automatically
   - Seed data loaded
   - Queries execute without errors

### Output Format (EXACT)

```
================================
PHASE 3: REFACTORING COMPLETE
================================

Project: code-smells-project
New Structure:
  src/
  ├── config/
  │   ├── settings.py (Configuration extracted)
  │   └── database.py (DB setup)
  ├── models/
  │   ├── user.py (User model)
  │   ├── product.py (Product model)
  │   └── order.py (Order model)
  ├── controllers/
  │   ├── user_controller.py (Business logic)
  │   ├── product_controller.py
  │   └── order_controller.py
  ├── views/
  │   ├── user_routes.py (HTTP routes)
  │   ├── product_routes.py
  │   └── order_routes.py
  ├── middlewares/
  │   ├── auth_middleware.py (Authentication)
  │   └── error_handler.py (Error handling)
  └── app.py (Composition root)

Transformations Applied:
  ✓ Configuration extracted to settings.py
  ✓ Hardcoded credentials removed
  ✓ SQL injection fixed (parameterized queries)
  ✓ N+1 queries eliminated (JOINs used)
  ✓ Business logic extracted to controllers
  ✓ Error handling centralized
  ✓ Authentication middleware added
  ✓ Password hashing upgraded to bcrypt

Validation Results:
  ✓ Application boots: python src/app.py
  ✓ Database initialized: OK
  ✓ Endpoints functional:
    - GET /products → 200
    - GET /users → 200
    - POST /orders → 201
  ✓ No anti-patterns remaining in critical areas

Report saved to: reports/audit-project-1.md

================================
```

### MANDATORY: Save Audit Report

After Phase 3 completes, execute:

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
✓ **MUST** save audit report to `reports/audit-project-{N}.md`
✓ **MUST** validate application boots and endpoints respond
✗ **MUST NOT** modify files before Phase 2 confirmation
✗ **MUST NOT** skip phases

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