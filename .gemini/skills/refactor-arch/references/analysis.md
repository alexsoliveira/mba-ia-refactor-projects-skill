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

# 🗄️ 3. Database Detection

## Heuristics

### SQLite

* `import sqlite3` (Python)
* `require('sqlite3')` (Node.js)
* `*.db` or `*.sqlite` files
* `Database(':memory:')` or `Database('./file.db')`

### PostgreSQL

* `import psycopg2` (Python)
* `const pg = require('pg')` (Node.js)
* Connection strings like `postgresql://user:pass@host:port/db`
* `DATABASE_URL` environment variable

### MongoDB

* `import pymongo` (Python) or `from pymongo import`
* `const mongodb = require('mongodb')` (Node.js)
* `.find()`, `.insert()`, `.update()` patterns
* Connection strings like `mongodb://`

### MySQL/MariaDB

* `import mysql.connector` (Python)
* `const mysql = require('mysql')` (Node.js)
* `CREATE TABLE` SQL with MySQL-specific syntax

### Fallback

* If no database library found: Classify as "No persistent DB" or "In-memory only"

---

# 🏗️ 4. Architecture Detection

## Monolithic (Level 1 - NEEDS REFACTORING)

### Detection Signals

* Everything in few files (< 10 source files)
* No `src/` or `app/` folder structure
* Mixed concerns: routing + logic + data access in same files
* No clear separation of models/controllers/routes
* Single entry point with all logic inline

### Indicators

* `app.py` or `app.js` > 200 lines
* `models.py`, `controllers.py`, `database.py` all mixing concerns
* All routes defined in main app file

---

## Partially Structured (Level 2 - NEEDS IMPROVEMENT)

### Detection Signals

* Some folder structure (`models/`, `routes/`, etc.)
* Partial separation of concerns
* But still lacks clear MVC boundaries
* Some business logic in controllers/routes

### Indicators

* `src/` folder exists
* Has `models/`, `routes/`, or `controllers/` folders
* But some files are still > 300 lines
* Some imports crossing layer boundaries

---

## Properly Layered MVC (Level 3 - WELL STRUCTURED)

### Detection Signals

* Clear `src/` structure with separate folders
* Models isolated from routes
* Controllers orchestrate between models and routes
* Middleware layer for cross-cutting concerns
* No business logic in route handlers

### Indicators

* `src/config/`, `src/models/`, `src/controllers/`, `src/routes/`, `src/middlewares/` exist
* Models < 150 lines each
* Controllers < 100 lines each
* Route files mostly delegate to controllers
* Clear entry point (`app.py` or `app.js`)

---

# 📊 5. Project Maturity Score

Calculate based on:

1. **Language & Framework:** Detected (Y/N)
2. **Database:** Detected (Y/N)
3. **Architecture Level:** 1=Monolith, 2=Partial, 3=Layered
4. **Code Organization:** Count files, LOC, folder depth
5. **Dependency Management:** Has requirements.txt or package.json (Y/N)

### Output

```
Architecture Maturity: Level X
Organization Score: X/10
Refactoring Complexity: Low | Medium | High
```

---

# 🔍 6. Detection Workflow (Phase 1)

### Step 1: Scan File System

```
1. List all files in project
2. Categorize by extension (.py, .js, .json, etc.)
3. Identify folder structure
4. Count LOC estimate
```

### Step 2: Analyze Dependencies

```
1. Read requirements.txt (Python) or package.json (Node.js)
2. Extract framework name
3. Identify ORM, middleware, utilities
```

### Step 3: Code Inspection

```
1. Open main entry point (app.py / app.js)
2. Scan for framework initialization
3. Identify route definitions
4. Look for database connection patterns
5. Check for error handling
```

### Step 4: Infer Architecture

```
1. Is there a src/ folder? → Likely structured
2. Are models/controllers/routes separated? → Level 2+
3. Do route files have business logic? → Level 1
4. Is error handling centralized? → Level 2+
```

### Step 5: Generate Report

```
Language: [Python | Node.js | Other]
Framework: [Flask | Django | Express | Other]
Database: [SQLite | PostgreSQL | MongoDB | Other]
Architecture: Level [1 | 2 | 3]
Maturity Score: [Low | Medium | High]
```

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
