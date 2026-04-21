# MVC Architecture Guidelines — Refactor Arch Skill

This document defines the **target architecture (MVC)** used during Phase 3 (Refactoring).

The agent MUST transform any codebase into this structure.

---

## Objective

Ensure the application follows:

* Clear separation of concerns
* Maintainable and testable structure
* Decoupled layers
* Predictable data flow

---

## Core Principle

MVC is based on **Separation of Concerns**, where:

* Model: data and business rules
* View: presentation / routing
* Controller: orchestration

Each layer MUST have a **single responsibility**.

---

## MVC Layers Definition

---

## 1. Model Layer

### Responsibility

* Represent application data
* Encapsulate business rules
* Handle persistence (DB interaction)

### MUST DO

* Define entities and data structures
* Perform validation
* Interact with database

### MUST NOT DO

* Handle HTTP requests
* Contain routing logic
* Format responses

---

## 2. View / Routes Layer

### Responsibility

* Handle HTTP requests
* Define endpoints
* Delegate execution to controllers

### MUST DO

* Map routes (GET, POST, etc.)
* Extract request parameters
* Return responses

### MUST NOT DO

* Contain business logic
* Perform DB queries
* Contain complex logic

---

## 3. Controller Layer

### Responsibility

* Orchestrate application flow
* Process user input
* Coordinate between Model and View

### MUST DO

* Call models/services
* Apply business logic
* Return formatted responses

### MUST NOT DO

* Direct DB queries (prefer models)
* Contain UI logic
* Become a "God class"

---

# 🔄 Data Flow (MANDATORY)

1. User → View/Route
2. View → Controller
3. Controller → Model
4. Model → Controller
5. Controller → View
6. View → Response

The Controller acts as the **central coordinator** ([Codecademy][2])

---

# Target Folder Structure

```bash
src/
├── config/
│   └── settings.*
├── models/
│   └── *_model.*
├── controllers/
│   └── *_controller.*
├── views/ or routes/
│   └── routes.*
├── middlewares/
│   └── error_handler.*
└── app.*  (composition root)
```

---

# Configuration Rules

* All configuration MUST be externalized
* No hardcoded values allowed

### Examples:

* Environment variables
* Config modules

---

# 🧩 Naming Conventions

## Models

* `<entity>_model`
* Example: `user_model.py`

## Controllers

* `<entity>_controller`
* Example: `user_controller.js`

## Routes

* `<entity>_routes`
* Example: `user_routes.js`

---

# 🔐 Security Rules

* No hardcoded credentials
* Input validation REQUIRED
* Centralized error handling

---

# 🧪 Testability Rules

* Each layer MUST be independently testable
* Controllers MUST be testable without HTTP layer
* Models MUST be testable without controllers

---

## Anti-Patterns to Avoid (Critical)

* Business logic in routes
* DB queries in controllers
* Mixed responsibilities
* Global state usage

---

# 🔁 Adaptation Rules (IMPORTANT)

The agent MUST adapt based on project maturity:

## Case 1 — Monolithic

* Full restructuring required

## Case 2 — Partial Layered

* Normalize structure
* Fix violations

## Case 3 — Already Structured

* Improve, do NOT over-refactor

---

## Refactoring Rules

* Prefer incremental changes
* Preserve functionality
* Maintain API contracts
* Avoid unnecessary rewrites

---

# 📌 Validation Requirements

After refactoring:

* Application MUST boot
* All endpoints MUST work
* No regression allowed

---

# 🧭 Final Rule

A correct MVC implementation:

✔ Each layer has one responsibility
✔ No cross-layer violations
✔ Clear data flow
✔ Easy to test and maintain

---

## Invalid MVC (Examples)

* Controller querying database directly
* Routes containing business logic
* Model formatting HTTP responses

---

## Valid MVC (Example Flow)

Route → Controller → Model → Controller → Response

---

## Golden Rule

If a file does more than one responsibility:

It is NOT MVC-compliant

[1]: https://www.techtarget.com/whatis/definition/Model-View-ViewModel?utm_source=chatgpt.com "What is model-view-controller (MVC)? | Definition from TechTarget"
[2]: https://www.codecademy.com/article/mvc-architecture-model-view-controller?utm_source=chatgpt.com "MVC Architecture Explained: Model, View, Controller | Codecademy"
