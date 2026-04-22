# AI Agent Context - Refactoring Architecture System

This file defines the global behavior, rules, and context for AI agents operating in this repository.

It must be respected at all times.

---

# Purpose

This repository is designed to:

* Analyze legacy backend systems
* Detect architectural issues, anti-patterns, and security flaws
* Refactor applications into a clean MVC architecture
* Ensure the application remains functional after changes

The primary mechanism for execution is the `refactor-arch` skill.

---

# Core Principles

## 1. Technology Agnostic Behavior

* The agent MUST work across different stacks (Python, Node.js, etc.)
* Do not assume language-specific patterns unless detected

## 2. Safety First

* NEVER modify files without explicit confirmation (Phase 2 -> Phase 3)
* Preserve application behavior at all times
* Avoid destructive or irreversible changes

## 3. Deterministic Output

* Always provide:

  * File paths
  * Line numbers
  * Explicit reasoning
* Avoid vague statements

## 4. Minimal Assumptions

* Infer architecture from code, not naming conventions alone
* Validate before refactoring

---

# Execution Model

All refactoring workflows MUST follow:

## Phase 1 - Analysis

* Detect:

  * Language
  * Framework
  * Dependencies
  * Architecture type
* Output structured summary

## Phase 2 - Audit

* Identify anti-patterns
* Classify severity:

  * CRITICAL
  * HIGH
  * MEDIUM
  * LOW
* Generate structured report
* STOP and request confirmation

## Phase 3 - Refactoring

* Apply MVC architecture:

  * Models -> data layer
  * Views/Routes -> routing layer
  * Controllers -> business logic
* Remove anti-patterns
* Validate application execution

---

# Severity Model (MANDATORY)

CRITICAL:

* Security flaws (credentials, injections)
* Architecture violations breaking system integrity

HIGH:

* Strong SOLID violations
* Tight coupling / no dependency injection

MEDIUM:

* Performance issues
* Code duplication
* Missing validations

LOW:

* Naming issues
* Readability improvements

---

# Skill Usage Rules

## Primary Skill

* `refactor-arch`

## When to Use

The agent MUST use this skill when:

* User asks to refactor code
* Legacy system is mentioned
* Code smells or bad architecture are identified
* MVC transformation is requested

## Behavior

* Always execute full 3-phase workflow
* Never skip phases
* Never refactor without audit

---

# Repository Structure Awareness

The agent will operate on:

* `code-smells-project/` -> Flask (monolithic)
* `ecommerce-api-legacy/` -> Node.js (Express)
* `task-manager-api/` -> Flask (partially structured)

The agent MUST:

* Adapt strategy per project maturity
* Not over-refactor already structured systems

---

# Validation Requirements

After refactoring, ALWAYS verify:

* Application boots:

  * Python -> `python app.py`
  * Node -> `npm start`

* Endpoints:

  * Must respond correctly
  * Must preserve original behavior

---

# Hard Constraints

* DO NOT:

  * Break APIs
  * Remove features
  * Introduce new dependencies unnecessarily

* MUST:

  * Extract configuration (no hardcoded values)
  * Centralize error handling
  * Maintain clean separation of concerns

---

# Iteration Strategy

If results are insufficient:

* Improve detection heuristics
* Expand anti-pattern catalog
* Refine refactoring playbook

Repeat execution (2-4 iterations expected)

---

# Important Notes

* Skills provide execution capability
* This file provides behavior and rules

Both MUST work together.

---

# Acceptance Alignment (README)

To stay fully aligned with `README.md`, the agent MUST also enforce:

* Execute the workflow on all 3 target projects:
  * `code-smells-project/`
  * `ecommerce-api-legacy/`
  * `task-manager-api/`
* During Phase 2, include deprecated API detection when applicable.
* During Phase 2, produce at least 5 findings per project.
* During Phase 2, include at least 1 finding of severity CRITICAL or HIGH.
* During Phase 3, preserve endpoint behavior and ensure application boot succeeds.
* Save Phase 2 audit outputs in:
  * `reports/audit-project-1.md`
  * `reports/audit-project-2.md`
  * `reports/audit-project-3.md`

---

# Final Rule

When in doubt:

1. Analyze first
2. Validate assumptions
3. Prefer safe refactoring
4. Preserve system behavior
