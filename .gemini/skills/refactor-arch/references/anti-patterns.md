# Anti-Patterns Catalog — Refactor Arch Skill

This document defines a catalog of software anti-patterns used during Phase 2 (Audit).

Each anti-pattern includes:

* Description
* Detection signals
* Severity
* Impact
* Refactoring strategy

---

# 🔴 CRITICAL ANTI-PATTERNS

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

# 🟠 HIGH ANTI-PATTERNS

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

# 🟡 MEDIUM ANTI-PATTERNS

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

# 🟢 LOW ANTI-PATTERNS

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

# 📌 Detection Strategy (IMPORTANT)

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

# 🧠 Final Rule

Detection must be:

* Deterministic
* Explainable
* Actionable

Avoid generic statements like:
❌ "code is bad"
✔ "query inside loop at file X line Y"
