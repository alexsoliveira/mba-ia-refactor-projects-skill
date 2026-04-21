# Anti-Patterns Catalog — Refactor Arch Skill

This document defines a catalog of software anti-patterns used during Phase 2 (Audit).

Each anti-pattern includes:

* Description
* Detection signals
* Severity
* Impact
* Refactoring strategy

---

# CRITICAL ANTI-PATTERNS

---

## 1. God Class / God Object

### Description

A single class handles multiple responsibilities (business logic, DB access, routing).

### Detection Signals

* File > 300 lines
* Multiple unrelated responsibilities
* Direct DB queries + business logic + routing together

### Severity

CRITICAL

### Impact

* Impossible to test
* High coupling
* Breaks MVC separation

### Refactoring

* Split into:

  * Models (data)
  * Controllers (logic)
  * Routes (exposure)

---

## 2. Hardcoded Credentials

### Description

Sensitive data directly embedded in code.

### Detection Signals

* Strings like:

  * SECRET_KEY
  * password
  * API_KEY
* Values inside source files

### Severity

CRITICAL

### Impact

* Security breach risk
* Credential leakage

### Refactoring

* Move to config/env variables
* Use `.env` or config module

---

## 3. SQL Injection Vulnerability

### Description

Unsafe query construction using string concatenation.

### Detection Signals

* Queries like:

  * `"SELECT * FROM users WHERE id=" + userId`
* No parameter binding

### Severity

CRITICAL

### Impact

* Data breach
* System compromise

### Refactoring

* Use parameterized queries / ORM

---

## 4. Big Ball of Mud

### Description

System without clear architecture or modularization.

### Detection Signals

* No folder structure
* Everything in few files
* No separation of concerns

### Severity

CRITICAL

### Impact

* High technical debt
* Difficult to scale and maintain

### Refactoring

* Introduce MVC structure
* Separate layers explicitly

---

# HIGH ANTI-PATTERNS

---

## 5. Business Logic in Routes / Controllers

### Description

Heavy logic inside route handlers.

### Detection Signals

* Long route methods
* Business rules inside controllers

### Severity

HIGH

### Impact

* Hard to test
* Violates separation of concerns

### Refactoring

* Move logic to service/controller layer

---

## 6. Tight Coupling (No Dependency Injection)

### Description

Classes directly instantiate dependencies.

### Detection Signals

* `new` inside business logic
* No abstraction/interfaces

### Severity

HIGH

### Impact

* Hard to test
* Hard to replace components

### Refactoring

* Introduce DI pattern
* Use interfaces/abstractions

---

## 7. Global Mutable State

### Description

Shared mutable variables across application.

### Detection Signals

* Global variables
* Shared state without control

### Severity

HIGH

### Impact

* Race conditions
* Unpredictable behavior

### Refactoring

* Encapsulate state
* Use scoped services

---

# MEDIUM ANTI-PATTERNS

---

## 8. N+1 Query Problem

### Description

Multiple DB queries inside loops.

### Detection Signals

* Query inside `for/loop`
* Repeated DB calls

### Severity

MEDIUM

### Impact

* Performance degradation

### Refactoring

* Use joins / eager loading

---

## 9. Code Duplication (DRY Violation)

### Description

Same logic repeated in multiple places.

### Detection Signals

* Copy-paste code blocks
* Similar functions

### Severity

MEDIUM

### Impact

* Hard maintenance
* Bug propagation

### Refactoring

* Extract reusable functions/services

---

## 10. Missing Input Validation

### Description

No validation on API inputs.

### Detection Signals

* No validation middleware
* Direct usage of request data

### Severity

MEDIUM

### Impact

* Security vulnerabilities
* Runtime errors

### Refactoring

* Add validation layer (schema/middleware)

---

## 11. Weak Cryptography / Insecure Hashing

### Description

Using cryptographically broken algorithms for password hashing or data encryption (MD5, SHA1, Base64).

### Detection Signals

* `hashlib.md5()` in Python
* `Buffer.from(pwd).toString('base64')` in Node.js
* `crypto.createHash('sha1')` anywhere
* Non-salted hash functions
* Custom encryption implementations

### Severity

CRITICAL

### Impact

* Password breach via rainbow tables
* Hash collision attacks
* System compromise
* Compliance violations (GDPR, PCI-DSS)

### Refactoring

* Replace with bcrypt, argon2, or PBKDF2
* Use library-provided functions, not custom crypto

---

## 12. Deprecated APIs

### Description

Using outdated or deprecated versions of libraries and APIs.

### Detection Signals

* Old import paths: `from flask.ext.sqlalchemy import`
* Deprecated method calls
* Old library versions in requirements/package.json
* Warnings during package installation
* Old middleware patterns

### Severity

HIGH

### Impact

* Security vulnerabilities (unpatched)
* Missing bug fixes
* Incompatibility with modern code
* Performance issues

### Refactoring

* Update to current API: `from flask_sqlalchemy import`
* Replace deprecated methods with modern equivalents
* Update dependencies to latest stable versions

---

# LOW ANTI-PATTERNS

---

## 11. Magic Numbers / Strings

### Description

Hardcoded values without meaning.

### Detection Signals

* Numbers like `42`, `1000` without context

### Severity

LOW

### Impact

* Poor readability

### Refactoring

* Replace with named constants

---

## 12. Poor Naming

### Description

Unclear variable or function names.

### Detection Signals

* Variables like `x`, `data1`, `tmp`

### Severity

LOW

### Impact

* Low maintainability

### Refactoring

* Use descriptive names

---

## 13. Deprecated API Usage

### Description

Use of outdated or deprecated APIs.

### Detection Signals

* Warnings in logs
* Old library usage

### Severity

MEDIUM / HIGH (depends)

### Impact

* Security risk
* Future incompatibility

### Refactoring

* Replace with modern alternatives

---

# � Python/Flask SPECIFIC DETECTION PATTERNS

This section provides concrete code patterns to detect anti-patterns in Python/Flask projects.

## Magic Numbers/Strings (LOW)

### Pattern Detection

Search for hardcoded numeric or status values without constants:

```python
# BAD - Magic number without context
if faturamento > 10000:
    desconto = faturamento * 0.1

# BAD - Magic string status (repeated multiple times)
status = "pendente"
cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'pendente'")
if novo_status == "aprovado":
    ...
```

### Search Strategy

- Look for `if <var> > <number>` or `if <var> < <number>`
- Look for magic strings: `"pendente"`, `"aprovado"`, `"cancelado"`, etc. appearing 3+ times
- Check for hardcoded thresholds (e.g., 10000, 5000, 1000) without explanation

---

## Code Duplication / DRY Violation (MEDIUM)

### Pattern Detection

Search for repeated logic across files:

```python
# In models.py
for row in rows:
    result.append({
        "id": row["id"],
        "nome": row["nome"],
        "email": row["email"],
    })

# In controllers.py (same logic repeated)
for row in rows:
    result.append({
        "id": row["id"],
        "nome": row["nome"],
        "email": row["email"],
    })
```

### Search Strategy

- Look for identical `dict(row)` conversion patterns
- Search for repeated `result.append({...})` blocks
- Check for identical validation logic in multiple functions
- Look for similar serialization code in different files

---

## Poor Naming / Inconsistency (LOW-MEDIUM)

### Pattern Detection

Search for naming inconsistencies:

```python
# Bad - Mix Portuguese/English
def listar_produtos():  # Portuguese
    pass

def get_usuario_por_id(id):  # Mixed Portuguese/English
    pass

def buscar_pedidos(usuario_id):  # Portuguese
    pass
```

### Search Strategy

- Check if function names mix Portuguese + English
- Look for abbreviations: `cid`, `cc`, `enrId` without clear meaning
- Check for inconsistent naming patterns across a module

---

## N+1 Query Problem (MEDIUM)

### Pattern Detection

Search for database queries inside loops:

```python
# BAD - N+1 Query
cursor.execute("SELECT * FROM pedidos WHERE usuario_id = ?")  # Query 1
rows = cursor.fetchall()
for row in rows:  # Loop
    cursor2 = db.cursor()
    cursor2.execute("SELECT * FROM itens_pedido WHERE pedido_id = ?")  # Query N
    itens = cursor2.fetchall()
    for item in itens:
        cursor3 = db.cursor()
        cursor3.execute("SELECT nome FROM produtos WHERE id = ?")  # Query N+M
```

### Search Strategy

- Look for `cursor.execute()` inside `for` or `while` loops
- Check for nested loops with DB queries
- Look for patterns like: outer query + inner query in loop
- Verify if JOINs could replace the loop logic

---

# �📌 Detection Strategy (IMPORTANT)

The agent MUST:

* Combine:

  * Static pattern detection
  * Heuristics
  * Contextual analysis

* Always return:

  * File path
  * Line number
  * Evidence

* Classify correctly by severity

---

# Final Rule

Detection must be:

* Deterministic
* Explainable
* Actionable

Avoid generic statements like:
AVOID: "code is bad"
✔ "query inside loop at file X line Y"
