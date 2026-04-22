# Project Analysis Heuristics

Purpose: support Phase 1 output required by `SKILL.md`.

Use these heuristics to infer the 7 mandatory fields:
- Language
- Framework (with version)
- Dependencies
- Domain
- Architecture
- Source files
- DB tables

## 1) Language Detection

Python signals:
- `requirements.txt`
- `.py` files dominate source set
- imports like `from flask import`, `import sqlite3`

Node.js signals:
- `package.json`
- `.js` or `.ts` files dominate source set
- imports like `express`, `sqlite3`, `pg`, `mongoose`

Rule:
- Pick dominant backend language by source files and runtime metadata.

## 2) Framework Detection (with version)

Flask:
- `from flask import` and `Flask(__name__)`
- version from `requirements.txt` or lock metadata

Express:
- `require("express")` or `import express`
- version from `package.json` and lock metadata

Fallback:
- if none detected, return `Custom/None` and version `unknown`.

## 3) Dependencies (top 3-5)

Python:
- from `requirements.txt`

Node.js:
- from `package.json` dependencies

Rule:
- list core runtime packages only; no dev-only tools unless unavoidable.

## 4) Domain Inference

Infer from:
- route names/endpoints
- model/entity names
- README project description

Examples:
- `/produtos`, `/pedidos` => E-commerce API
- `/tasks`, `/users` => Task Manager API
- course/enrollment/checkout => LMS/Commerce API

## 5) Architecture Classification

Monolithic:
- few files, mixed layers in same modules
- routes, DB, business logic tightly coupled

Partially structured:
- has folders (`models`, `routes`, `services`) but with cross-layer leakage

Layered/MVC-like:
- clear boundaries and minimal cross-layer violations

## 6) Source Files Count

Count backend source files analyzed (exclude tests, vendor, node_modules, virtual env).

Counting rules:
- Count only executable backend source files (`.py`, `.js`, `.ts`).
- Exclude non-source artifacts: `README*`, `*.md`, `requirements*.txt`, `package-lock.json`, `*.db`, `*.sqlite`, `.env*`.
- Exclude infra/build folders: `node_modules`, `.venv`, `venv`, `dist`, `build`, `coverage`, `.git`.
- Do not count generated files or migration snapshots unless they are actively executed by the app entrypoint.

Project-specific sanity check:
- For `code-smells-project` baseline (pre-refactor), expected source file count is `4`:
  - `app.py`
  - `controllers.py`
  - `models.py`
  - `database.py`

## 7) DB Tables Detection

SQL projects:
- parse `CREATE TABLE` statements and schema definitions

ORM projects:
- infer entities from model declarations when table names are absent

Output format:
- comma-separated list in the `DB tables` field.

## Output Contract Reminder

The final Phase 1 text must match the literal structure in `SKILL.md`.
Do not add fields or narrative text.
