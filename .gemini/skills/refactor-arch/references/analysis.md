# Project Analysis Heuristics — Refactor Arch Skill

This document defines the rules and heuristics used in **Phase 1 (Project Analysis)**.

The goal is to:

* Detect language and framework
* Infer architecture
* Identify system structure
* Extract meaningful metadata

---

# 🎯 Analysis Goals

The agent MUST determine:

* Programming language
* Framework (if any)
* Project structure
* Architecture style
* Domain (business context)
* Dependencies
* Database usage

---

# 🧠 Detection Strategy

The agent MUST combine:

* File system inspection
* Code pattern recognition
* Dependency analysis
* Heuristic inference

Never rely on a single signal.

---

# 🔍 1. Language Detection

## Heuristics

### Python

* Presence of:

  * `.py` files
  * `requirements.txt`
  * `app.py`, `wsgi.py`

### Node.js

* Presence of:

  * `package.json`
  * `.js`, `.ts` files
  * `node_modules/`

### General Rule

* Count dominant file extension
* Ignore libraries/vendor folders

---

# ⚙️ 2. Framework Detection

## Python

### Flask

* `from flask import`
* `Flask(__name__)`
* `@app.route`

### Django

* `settings.py`
* `manage.py`
* `urls.py`

---

## Node.js

### Express

* `require('express')` or `import express`
* `app.get(...)`
* `app.use(...)`

---

## Fallback Rule

If no framework is detected:

* Classify as "Vanilla / Custom Framework"

---

# 🧱 3. Architecture Detection

## Heuristics

### Monolithic

* Few files
* Mixed responsibilities
* No folder separation

### Layered (Partial MVC)

* Folders like:

  * models/
  * routes/
  * services/
* Responsibilities partially separated

### Clean / Structured MVC

* Clear separation:

  * models/
  * controllers/
  * views/ or routes/
  * config/
  * middlewares/

---

## Detection Logic

* If all logic in ≤ 5 files → Monolithic
* If partial separation → Layered
* If strict separation → MVC

---

# 🧩 4. Component Identification

The agent MUST classify code into:

## Models

* Data structures
* ORM entities
* DB interaction

## Controllers

* Business logic
* Orchestration

## Views / Routes

* HTTP endpoints
* Request handling

---

## Detection Signals

### Models

* DB queries
* ORM usage
* Entity definitions

### Controllers

* Logic-heavy functions
* Service coordination

### Routes

* HTTP methods:

  * GET, POST, PUT, DELETE

---

# 🗂️ 5. Dependency Analysis

## Python

* `requirements.txt`
* Imports

## Node.js

* `package.json`

---

## Output MUST include:

* Key dependencies
* Framework-related libraries

---

# 🗄️ 6. Database Detection

## Heuristics

* Keywords:

  * `SELECT`, `INSERT`, `UPDATE`
* Libraries:

  * SQLAlchemy
  * mongoose
  * sqlite3
  * psycopg2

---

## Output MUST include:

* DB usage detected (yes/no)
* Possible tables/entities

---

# 🧠 7. Domain Inference

## Strategy

Infer domain from:

* File names
* Variables
* Routes

## Examples

* `/products` → E-commerce
* `/tasks` → Task Manager
* `/checkout` → Payment / LMS

---

## Output MUST include:

* Short domain description

---

# 📊 8. Project Metrics

The agent MUST calculate:

* Number of files
* Approximate LOC
* Folder structure depth

---

# 📌 Output Format (MANDATORY)

================================
PHASE 1: PROJECT ANALYSIS
=========================

Language:
Framework:
Dependencies:
Domain:
Architecture:
Source files:
DB usage:

================================

---

# ⚠️ Important Rules

* Always validate assumptions
* Prefer evidence over guessing
* If uncertain, state:
  "Unable to confidently detect — assuming X based on Y"

---

# 🚀 Advanced Heuristics (Optional)

* Detect layered violations (early signal for Phase 2)
* Detect mixed responsibilities
* Identify architectural drift

---

# 🧭 Final Rule

Analysis must be:

* Deterministic
* Explainable
* Reproducible

Bad:
❌ "Looks like Flask project"

Good:
✔ "Detected Flask due to '@app.route' in app.py"
