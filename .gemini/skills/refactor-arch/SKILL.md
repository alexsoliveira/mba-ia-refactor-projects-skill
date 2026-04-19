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

It follows **progressive disclosure**:
- This file = orchestration (what to do)
- `/references/*` = domain knowledge (how to do)

Only load reference files when necessary.

---

## Table of Contents

1. Execution Model  
2. Phase 1 — Analysis  
3. Phase 2 — Audit  
4. Phase 3 — Refactoring  
5. Conditional Execution (Project Maturity)  
6. Reference Files  

---

## Execution Model

Follow phases strictly in order:

1. **Analyze project**
2. **Audit architecture**
3. **Ask for confirmation**
4. **Refactor**
5. **Validate**

DO NOT skip phases.

---

# PHASE 1 — PROJECT ANALYSIS

## Objectives:
- Detect:
  - Programming language
  - Framework
  - Dependencies
  - Architecture type
  - Domain
- Count files and estimate size
- Identify database usage

## Actions

- Scan project structure
- Identify key files (entry point, routes, models)
- Estimate:
  - number of files
  - approximate LOC
- Infer architecture:
  - monolith
  - layered
  - partially structured

## Use Reference

- [references/analysis.md](references/analysis.md)

## Output Format:
Print structured summary:

================================
PHASE 1: PROJECT ANALYSIS
================================

---

# PHASE 2 — ARCHITECTURE AUDIT

## Objectives:

- Detect anti-patterns using references
- Classify severity:
  - CRITICAL
  - HIGH
  - MEDIUM
  - LOW

## Rules

Each finding MUST include:

- File path
- Line numbers
- Description
- Impact
- Recommendation

## Requirements

- Minimum 5 findings
- Must include:
  - at least 1 CRITICAL or HIGH
  - deprecated API detection

## Use References

- [references/anti-patterns.md](references/anti-patterns.md)
- [references/report-template.md](references/report-template.md)

## Output:
ARCHITECTURE AUDIT REPORT

## STOP RULE (MANDATORY)

After generating the report:

"Proceed with refactoring (Phase 3)? [y/n]"

- WAIT for confirmation
- DO NOT MODIFY FILES BEFORE CONFIRMATION

---

# PHASE 3 — REFACTORING

## Objectives:
- Apply MVC architecture:

### Models:
- Data abstraction
- DB access isolation

### Views / Routes:
- Routing only
- No business logic

### Controllers:
- Business logic orchestration

## Transformations:

Apply refactoring patterns from:

- [references/refactoring-playbook.md](references/refactoring-playbook.md)
- [references/mvc-guidelines.md](references/mvc-guidelines.md)

Key actions:

- Remove anti-patterns
- Extract configuration
- Eliminate hardcoded values
- Separate responsibilities
- Modularize by domain

## Validation:
- Application must boot:
  - Python → `python app.py`
  - Node → `npm start`
- Endpoints must respond correctly

## Output:
================================
PHASE 3: REFACTORING COMPLETE
================================

- New structure
- Validation results
- Remaining issues (if any)

---

# Constraints

- Must be technology agnostic
- Must preserve functionality
- Must not break endpoints
- Must adapt based on project maturity

---

# Behavior Rules

- Be deterministic
- Be explicit (file + line)
- Prefer safe transformations
- Avoid unnecessary rewrites