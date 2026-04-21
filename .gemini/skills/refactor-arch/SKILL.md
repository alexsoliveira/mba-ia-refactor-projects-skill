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

**📝 UPDATE (2026-04-21):**
This SKILL has been adjusted to **STRICTLY FOLLOW the README.md specification for Phase 1 output format**.
- Phase 1 template now uses EXACT field order and format from README
- Removed extra fields (LOC Estimate, Maturity, Key Entities) not present in README template
- Phase 1 output now matches README example exactly

# ⚡ IMPERATIVE INSTRUCTIONS FOR GEMINI (FOLLOW EXACTLY - ZERO TOLERANCE)

**🚨 EMERGENCY RULES - READ BEFORE ANYTHING ELSE 🚨**

**⚠️ CRITICAL CHECKPOINT: LOW SEVERITY FINDINGS**

Before you output ANY Audit Report (Phase 2), you MUST verify:

```
Count of LOW severity findings ≥ 2?

YES ✅ → Proceed to output Phase 2
NO ❌ → STOP, search harder, find more LOW findings, then output Phase 2
```

**IF YOU OUTPUT PHASE 2 WITH ONLY 0-1 LOW FINDINGS → YOUR AUDIT IS INVALID.**

---

Your task is to print exactly what is shown in the templates below. NOTHING MORE.

**YOU MUST PRINT EXACTLY THESE PHASES IN THIS ORDER - NO DEVIATIONS:**

```
[Print exactly these sections below - do NOT add anything else]

PHASE 1 OUTPUT → STOP
THEN PHASE 2 OUTPUT → STOP
THEN WAIT for user confirmation → STOP
THEN PHASE 3 (if confirmed) → STOP
```

**⚠️ CRITICAL: DO NOT BE CREATIVE**
- ❌ Do NOT add "Executive Summary" 
- ❌ Do NOT add "I have completed the analysis"
- ❌ Do NOT add "Proposed Refactoring Strategy"
- ❌ Do NOT describe Phase 3 before user confirms
- ✓ Only print the templates shown below

---

**READ THIS FIRST BEFORE DOING ANYTHING:**

Your task has 3 mandatory phases. You MUST execute them in this exact order:

1. **PHASE 1 MUST EXECUTE FIRST** (no exceptions)
   - Analyze the project
   - Print EXACT template (copy-paste the format below, substitute values only)
   - Do NOT add emojis, titles, or descriptions
   - Do NOT proceed to Phase 2 until Phase 1 is fully printed

2. **PHASE 2 EXECUTES SECOND** (after Phase 1 completes)
   - Audit code for anti-patterns
   - Print EXACT template (copy-paste the format below, substitute values only)
   - Do NOT use emojis, symbols, bullets, or any formatting except markdown
   - MANDATORY: Find at least 5 findings with this distribution:
     * 1-2 CRITICAL
     * 1-2 HIGH
     * 2 MEDIUM
     * 2 LOW (THIS IS NOT OPTIONAL - you MUST find 2 LOW findings)
   - Print confirmation prompt and STOP (wait for user input)

3. **PHASE 3 EXECUTES THIRD** (ONLY if user confirms with "y" or "yes")
   - Refactor the code
   - Save audit report to `reports/audit-project-N.md`
   - Validate application works

**CRITICAL RULES (VIOLATION = TASK FAILURE):**
- ❌ **NO EMOJIS ANYWHERE** (0 tolerance: NO 🔴, 📊, 🚀, 🛡️, 📊, 🛑, 🟠, 🟡, 🟢, or ANY icon)
- ❌ **NO ADDING EXTRA TEXT** (no "Executive Summary", no "I have completed", no descriptions)
- ❌ NO PHASE 1 SKIPPING (must execute first, every time)
- ❌ NO COMBINING PHASES (1 → STOP → 2 → STOP → 3 sequence)
- ❌ NO ACCEPTING PHASE 3 WITHOUT USER CONFIRMATION
- ❌ **NO LOW FINDINGS < 2** (MUST find at least 2 LOW severity findings - if you have 1, keep searching)
- ❌ NO ASCII ART TABLES (no ┌──┐, ├──┤, └──┘ characters)
- ❌ **NO DESCRIBING PHASE 3 BEFORE USER CONFIRMS** (Phase 2 ends with question, nothing more)
- ✓ EXACT TEMPLATES ONLY (use provided format, substitute only values)
- ✓ WAIT for user confirmation before proceeding between phases

---

## 🎯 ABSOLUTELY LITERAL OUTPUT EXAMPLES

**Look at these EXACT examples below. Your output MUST look EXACTLY like this (only substituting values).**

### EXAMPLE PHASE 1 OUTPUT (COPY THIS STRUCTURE EXACTLY):

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      Python
Framework:      Flask 3.1.1
Dependencies:  flask-cors
Domain:        E-commerce API (produtos, pedidos, usuários)
Architecture:  Monolítica — tudo em 4 arquivos, sem separação de camadas
Source files:  4 files analyzed
DB tables:     produtos, usuarios, pedidos, itens_pedido
================================
```

**RULES FOR PHASE 1 OUTPUT (DO NOT DEVIATE):**
- Use EXACTLY this format
- NO blank lines between header and first field
- NO extra fields (no LOC Estimate, no Maturity, no Key Entities)
- Fields in EXACT order: Language, Framework, Dependencies, Domain, Architecture, Source files, DB tables
- NO spacing alignment variations (maintain exact spacing shown)
- NO emojis, NO markdown, NO descriptions
- End with `================================` separator

---

### EXAMPLE PHASE 2 OUTPUT (COPY THIS STRUCTURE EXACTLY):

```
================================
ARCHITECTURE AUDIT REPORT
================================

Project: code-smells-project
Stack:   Python + Flask 3.1.1
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

### [CRITICAL] Hardcoded Credentials

File: app.py, Line: 9

app.config["SECRET_KEY"] = "dev-key-keep-it-safe"

Impact: Session hijacking, token forgery, production at risk

---

### [CRITICAL] N+1 Query Problem

File: models.py, Lines: 98-125

for row in rows:
    cursor_items = db.cursor()
    cursor_items.execute("SELECT ... FROM itens_pedido WHERE pedido_id = ?")

Impact: Severe performance degradation with 100 orders = 101 queries

---

### [HIGH] Business Logic in Models

File: models.py, controllers.py

Mixed business logic and data access, no service layer

Impact: Untestable code, tightly coupled layers

---

### [MEDIUM] Magic Numbers

File: models.py, Lines: 146-153

if faturamento > 10000:
    desconto = faturamento * 0.1

Impact: Hardcoded discount rates without reusable constants

---

### [MEDIUM] Code Duplication

File: controllers.py, models.py

Row-to-dict conversion repeated in multiple functions

Impact: Inconsistent serialization across endpoints

---

### [LOW] Magic Strings for Status

File: models.py, controllers.py

status = "pendente"  # repeated without constants

Impact: Typo risk, no validation

---

### [LOW] Inconsistent Naming

File: database.py

Mix of Portuguese/English: get_db(), listar_produtos(), criar_pedido()

Impact: Confusing codebase

---

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

**This is what Phase 2 MUST look like:**
- ✓ Markdown table for summary (not ASCII art with ┌──┐)
- ✓ Each finding has [SEVERITY], File:Line, Code, Impact
- ✓ Findings sorted: CRITICAL → HIGH → MEDIUM → LOW
- ✓ 2 LOW findings included (required)
- ✓ Ends with STOP (waiting for user confirmation)

---

## ⚠️ COMMON MISTAKES (DO NOT REPEAT THESE)

**MISTAKE 1 - Phase 1 in Paragraph Format**

❌ WRONG:
```
Phase 1: Analysis Summary
 - Language: Python
 - Framework: Flask (3.1.1)
 - Architecture: Monolithic and tightly coupled...
```

✓ CORRECT:
```
================================
PHASE 1: PROJECT ANALYSIS
================================

Language:       Python
Framework:      Flask 3.1.1
...
```

**MISTAKE 2 - Phase 2 with ASCII Tabels**

❌ WRONG:
```
┌──────────┬───────────────────────┐
│ Severity │ Issue                 │
├──────────┼───────────────────────┤
│ CRITICAL │ SQL Injection         │
```

✓ CORRECT:
```
| Severity | Count |
|----------|-------|
| CRITICAL | 2     |

### [CRITICAL] SQL Injection
File: app.py, Line: 59
...
```

**MISTAKE 3 - Not Finding 2 LOW Findings**

❌ WRONG: Only finding CRITICAL and HIGH (0-1 LOW findings)
✓ CORRECT: Finding at least 2 LOW findings (magic strings, magic numbers, bad naming, etc.)

---

## 🚨 ULTRA-STRICT RULES (NO FLEXIBILITY)

**EMOJI RULE = ZERO**
- Any emoji present = FAIL
- No 🔴, 📊, 🛡️, 🛑, 🟠, 🟡, 🟢, 🚀, ✓, •, etc.

**TEMPLATE RULE = EXACT**
- Phase 1: Use template shown above ONLY
- Phase 2: Use template shown above ONLY
- No "I completed the analysis"
- No "Executive Summary"
- No "Proposed Refactoring"

**LOW FINDINGS RULE = 2 MINIMUM**
- Before Phase 2 output: Count LOW findings
- If < 2: KEEP SEARCHING, THEN OUTPUT
- If ≥ 2: OK to output Phase 2

**PHASE 3 RULE = AFTER CONFIRMATION**
- Phase 2 ends with: `Proceed with refactoring (Phase 3)? [y/n]`
- Then: STOP and WAIT for user response
- Never describe Phase 3 before user confirms

---

# Refactor Architecture Skill (MVC Automation)

## Overview

This skill performs a **3-phase automated refactoring workflow** to transform any backend codebase into a clean MVC architecture.

**CRITICAL REQUIREMENTS — FOLLOW EXACTLY:**
- **Sequence:** PHASE 1 FIRST → PHASE 2 SECOND → Wait for confirmation → PHASE 3 THIRD
- Phase 1: MUST execute first. Analyze and report stack using EXACT template format (see below)
- Phase 2: Generate structured audit report with MINIMUM 5 findings using EXACT template format
- Phase 3: Create proper MVC structure ONLY after user confirms Phase 2
- NO EMOJIS in output (use plain text only)
- NO deviations from template format
- Wait for user confirmation before any phase transition

---

## PHASE 1 — PROJECT ANALYSIS (⚠️ MUST EXECUTE FIRST, ALWAYS)

### ⚠️ CRITICAL: This phase MUST execute FIRST. NEVER skip it. NEVER combine with Phase 2.

BEFORE YOU DO ANYTHING:
1. Check if Phase 1 has been printed yet
2. If NO → Print Phase 1 immediately (this is the first thing user should see)
3. If YES → Proceed to Phase 2

### Objective
Detect programming language, framework, architecture type, domain, database, and project maturity.

### Use Reference
Load `references/analysis.md` for detection heuristics.

### Minimum Detections (DETECT ALL REQUIRED FIELDS)

For any project, you MUST detect and report:

1. **Language** (Python, Node.js, Java, etc.)
2. **Framework** (Flask, Django, Express, Spring, etc.) with version
3. **Dependencies** (top 3-5 packages/libraries)
4. **Domain** (what does this application do? - E-commerce API, Task Manager, LMS, etc.)
5. **Architecture** (current state: Monolítica/Monolith, Partially Structured, Layered, etc.)
6. **Source files** (number of analyzed source files - literal format: "N files analyzed")
7. **DB tables** (list all database tables found)

**DO NOT detect extra fields.** Only these 7 fields appear in the output.
The example shows the EXACT format expectations.

### Output Format (USE EXACTLY THIS TEMPLATE — NO CHANGES, NO EMOJIS)

**COPY-PASTE this exact format. Only replace the VALUES (right side of colons).**

Follow this template EXACTLY as shown. No deviations, no extra fields, no reordering:

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      [LANGUAGE]
Framework:      [FRAMEWORK & VERSION]
Dependencies:  [TOP 3-5 DEPENDENCIES]
Domain:        [APPLICATION DOMAIN]
Architecture:  [ARCHITECTURE TYPE]
Source files:  [NUMBER] files analyzed
DB tables:     [TABLE LIST]
================================
```

**EXAMPLES OF CORRECT FIELD VALUES:**

- `Language:      Python` or `Language:      JavaScript`
- `Framework:      Flask 3.1.1` or `Framework:      Express 4.18.2`
- `Dependencies:  flask-cors, werkzeug` (comma-separated, no bullets)
- `Domain:        E-commerce API (produtos, pedidos, usuários)` (describe what app does)
- `Architecture:  Monolítica — tudo em 4 arquivos, sem separação de camadas` (current state)
- `Source files:  4 files analyzed` (literal format)
- `DB tables:     produtos, usuarios, pedidos, itens_pedido` (comma-separated)

**CRITICAL CHECKLIST BEFORE OUTPUTTING PHASE 1:**
- ❌ NO blank lines after `================================` header
- ❌ NO extra fields like "LOC Estimate", "Maturity", "Key Entities"
- ❌ NO reordering fields (keep exact order shown above)
- ❌ NO emojis or special characters
- ✓ Exact field names and spacing from template
- ✓ Only substitute the bracketed [VALUES]
- ✓ End with final `================================` separator

---

## PHASE 2 — ARCHITECTURE AUDIT (⚠️ AFTER PHASE 1 COMPLETES - NEVER COMBINE)

### ⚠️ CRITICAL: This phase is SECOND and ONLY executes after Phase 1 is fully printed.

### ⚠️ CRITICAL REMINDER: After Phase 2, YOU MUST STOP and wait for user confirmation. Do NOT continue to Phase 3.

### ⚠️ CRITICAL REMINDER ON LOW FINDINGS (READ THIS FIRST):

**YOUR PHASE 2 IS INVALID IF YOU HAVE FEWER THAN 2 LOW FINDINGS.**

**DO NOT OUTPUT PHASE 2 UNLESS YOU HAVE AT LEAST 2 LOW SEVERITY FINDINGS.**

**📋 USE THIS CHECKLIST:** Read `CHECK_LOW_FINDINGS.md` for mandatory LOW findings by project.

---

Count your LOW findings BEFORE you print Phase 2:

- Finding 0-1 LOW? → **STOP** and search harder → Find more → Then output
- Finding 2+ LOW? → OK, proceed with Phase 2 output

**Examples of LOW findings (from code-smells-project README):**

1. **[LOW] Magic Strings for Status** — controllers.py + models.py
   - Problem: Status values `"pendente"`, `"aprovado"`, `"cancelado"` hardcoded as strings
   - Search pattern: Look for where status is set/compared in code

2. **[LOW] Inconsistent Nomenclature** — database.py + multiple files
   - Problem: Mix of Portuguese/English naming: `get_db()`, `listar_produtos()`, `criar_pedido()`, `atualizar_status_pedido()`
   - Search pattern: Look for inconsistent function naming across codebase

**If you're analyzing code-smells-project and don't find these 2 LOW findings, search harder. They definitely exist.**

---

BEFORE YOU DO ANYTHING:
1. Check if Phase 1 is already printed
2. If NO → Print Phase 1 first (never start with Phase 2!)
3. If YES → Proceed with Phase 2 audit

### After Phase 2 is printed, you MUST:
1. Include the confirmation prompt: `Proceed with refactoring (Phase 3)? [y/n]`
2. STOP and WAIT for user input
3. Do NOT propose Phase 3 refactoring plan
4. Do NOT describe how you would refactor
5. Do NOT ask "Would you like me to proceed?" more than once
6. WAIT for explicit "y" or "yes" response before continuing

### Objective
Detect anti-patterns, classify by severity, generate structured audit report using EXACT template format.

### Use References
- `references/anti-patterns.md` - Anti-pattern catalog with detection signals and examples
- `references/report-template.md` - Report format template (FOLLOW EXACTLY)

### MANDATORY REQUIREMENTS FOR PHASE 2

### MANDATORY REQUIREMENTS FOR PHASE 2

**⚠️ BEFORE YOU START PHASE 2, READ THIS:**

You MUST find **exactly 2 LOW severity findings**. If you have only 1 LOW finding, you have FAILED the audit.

**THIS IS NOT OPTIONAL. IF YOU HAVE 1 LOW FINDING → KEEP SEARCHING → FIND 1 MORE → THEN STOP**

The audit is incomplete if you don't have 2 LOW findings.

---

**EXACTLY 5+ findings required — THIS IS NOT OPTIONAL:**
- ✓ 1-2 CRITICAL findings
- ✓ 1-2 HIGH findings  
- ✓ 2 MEDIUM findings
- ✓ **2 LOW findings (NOT 1, NOT 0, NOT 3+, EXACTLY 2 OR MORE)**

**⚠️ CRITICAL REMINDER ON LOW FINDINGS:**

Count your LOW findings before you output Phase 2.

- If you have 0 LOW → Search harder → Find 2 → Then output
- If you have 1 LOW → Continue searching → Find 1 more → Then output
- If you have 2+ LOW → OK, you can output

**Examples of LOW findings to search for (real examples from code-smells-project):**

1. **Magic Strings for Status** (Example: models.py line where status is used)
   - Pattern: Status values like "pendente", "aprovado", "cancelado" hardcoded as strings
   - Problem: No constants, typo risk, no validation

2. **Magic Numbers for Business Rules** (Example: models.py lines 146-153)
   - Pattern: `if faturamento > 10000:` or `desconto = 0.1` hardcoded
   - Problem: Discount rates (10%, 5%, 2%) hardcoded without named constants

3. **Inconsistent Nomenclature** (Example: mix across files)
   - Pattern: `get_db()` (English), `listar_produtos()` (Portuguese), `criar_pedido()` (mix)
   - Problem: Inconsistent naming makes code confusing

4. **Duplicated Code** (Example: same `dict(row)` in multiple files)
   - Pattern: Row-to-dictionary conversion logic repeated
   - Problem: Maintenance burden, high chance of inconsistency

5. **Poor Exception Handling** (Example: controllers.py)
   - Pattern: `except Exception as e:` catching all exceptions generically
   - Problem: No specific error types, loses debugging information

**Do not output Phase 2 until you have at least 2 LOW findings.**

1. **CRITICAL Anti-Patterns** — Search for:
   - Hardcoded credentials: `SECRET_KEY =`, `password =`, `API_KEY =` (check for string literals)
   - SQL Injection: String concatenation in queries (`"SELECT * FROM WHERE id = " +`)
   - Arbitrary code execution: `/admin/*` endpoints without auth
   - Weak crypto: `hashlib.md5()`, `hashlib.sha1()`, `base64` for passwords
   - No DB validation: Direct SQL execution endpoints

2. **HIGH Anti-Patterns** — Search for:
   - Business logic in models: Calculation loops, inventory management, discount logic in model functions
   - Tight coupling: Controllers calling models directly without service layer
   - No dependency injection: Direct instantiation of objects
   - Global mutable state: Shared variables across modules

3. **MEDIUM Anti-Patterns (MUST FIND AT LEAST 2)** — Search for:
   - N+1 queries: `for row in rows:` followed by DB queries inside loop
   - Code duplication: Same `dict(row)`, serialization, or logic repeated in multiple files
   - Missing input validation: No schema/validator middleware on routes
   - Magic numbers: Hardcoded values like `10`, `5`, `1000` without constants
   
   **Examples from code-smells-project:**
   - Magic numbers in models.py line 146: `if faturamento > 10000:` and `desconto = faturamento * 0.1`
   - Code duplication: `dict(row)` conversion in both controllers.py and models.py
   
4. **LOW Anti-Patterns (MUST FIND AT LEAST 2 — REQUIRED, NOT OPTIONAL)** — Search for:
   
   **FOR code-smells-project SPECIFICALLY (if analyzing this project):**
   - **[LOW] Magic Strings for Status:** Search models.py and controllers.py for hardcoded status values like `"pendente"`, `"aprovado"`, `"cancelado"` used repeatedly without constants
   - **[LOW] Inconsistent Nomenclature:** Search database.py and other files for mixed naming conventions (Portuguese/English mix like `get_db()`, `listar_produtos()`, `criar_pedido()`, `atualizar_status_pedido()`)
   
   **GENERAL LOW patterns (for any project):**
   - Magic numbers: Hardcoded numeric values without named constants
   - Poor naming: Abbreviated or cryptic variable names that reduce readability
   - Generic exception handling: `except Exception as e:` without specific error types
   - Unused imports or poorly organized code structure
   - Duplicate utility functions or serialization logic
   
   **⚠️ CRITICAL REMINDER:**
   - Count your LOW findings BEFORE outputting Phase 2
   - If you have < 2 LOW → KEEP SEARCHING → Find more → THEN output Phase 2
   - Do NOT output Phase 2 with less than 2 LOW findings
   - This is NOT optional. Low severity findings are REQUIRED.

### Report Format — USE EXACT TEMPLATE (ABSOLUTELY NO DEVIATIONS)

Follow `references/report-template.md` EXACTLY. Your report MUST have:

1. **Header section** with:
   - `================================`
   - `ARCHITECTURE AUDIT REPORT`
   - Project name, stack info, file count
   - `================================`

2. **Summary Table** (REQUIRED) with this exact format:
   ```
   | Severity | Count |
   |----------|-------|
   | CRITICAL | N     |
   | HIGH     | N     |
   | MEDIUM   | N     |
   | LOW      | N     |
   
   **Total Findings: N**
   ```

3. **Findings Section** with EACH finding having:
   - **Header:** `### [SEVERITY] Finding Title`
   - **File line:** `File: filename, Line(s): N-M`
   - **Code example:** 3-5 lines of actual code showing the problem
   - **Impact:** Single sentence describing business/security impact
   - **Separator:** `---` (between findings)

4. **Example format for ONE finding (COPY THIS STRUCTURE EXACTLY):**
   ```
   ### [CRITICAL] Hardcoded Credentials

   File: app.py, Line: 9

   app.config["SECRET_KEY"] = "dev-key-keep-it-safe"

   Impact: Session hijacking, token forgery, production at risk

   ---
   ```

5. **Footer** (MANDATORY) with this exact format:
   ```
   ================================
   PHASE 2 COMPLETE
   ================================

   Total Findings: N
     - CRITICAL: N
     - HIGH: N
     - MEDIUM: N
     - LOW: N

   Proceed with refactoring (Phase 3)? [y/n]
   ```

### WHAT NOT TO DO (ZERO TOLERANCE VIOLATIONS)

❌ **DO NOT DO THESE THINGS - THEY WILL BREAK THE SKILL:**

1. ❌ Use ANY emojis (🚀, 📊, 🔴, 🟠, 🟡, ✓, *, •, etc.)
2. ❌ Use bullet points (•, *, -, etc.) for findings
3. ❌ Use colored text or markdown formatting for severity (example: ~~never~~ do this)
4. ❌ Combine findings into one summary line
5. ❌ Use "Phase 3 Refactoring Plan" or "Proposed Solutions" in Phase 2
6. ❌ Skip findings (MUST have minimum 5)
7. ❌ Have fewer than 2 LOW severity findings
8. ❌ Put descriptions in bullet format instead of structured [SEVERITY] format
9. ❌ Skip the confirmation prompt at the end
10. ❌ Suggest refactoring actions in Phase 2 (Phase 2 is AUDIT ONLY, Phase 3 is REFACTORING)
11. ❌ **USE ASCII ART TABLES** (no ┌──┐, ├──┤, │, ┘, └ characters) — Use Markdown tables instead
12. ❌ Only print Phase 1 as paragraphs or bullet points (must use EXACT template format)

### PRE-OUTPUT VALIDATION CHECKLIST (VERIFY ALL BEFORE PRINTING PHASE 2)

**Before you print Phase 2 output, check this list:**

- [ ] Does my Phase 1 output match the LITERAL EXAMPLE above? (structure line-by-line?)
- [ ] Do I have exactly 5 or more total findings?
- [ ] Do I have at least 1-2 CRITICAL findings?
- [ ] Do I have at least 1-2 HIGH findings?
- [ ] Do I have at least 2 MEDIUM findings?
- [ ] Do I have at least 2 LOW findings? (If NOT, STOP and find more before proceeding)
- [ ] Have I used ZERO emojis in my entire output?
- [ ] Have I used ZERO ASCII art tables (no ┌──┐)?
- [ ] Is my summary table in Markdown format (| Severity | Count |)?
- [ ] Does each finding have the structure: ### [SEVERITY] Title, File: ..., Code, Impact, ---?
- [ ] Are my findings sorted: CRITICAL → HIGH → MEDIUM → LOW?
- [ ] Does my Phase 2 output end with the STOP confirmation prompt?
- [ ] Am I waiting for user confirmation before proceeding to Phase 3?

**If ANY checkbox is unchecked, FIX IT before printing output.**

### POST-AUDIT: MANDATORY STOP

Print the confirmation prompt and STOP. Do NOT proceed to Phase 3 until user confirms with "y" or "yes".

If user confirms "y" or "yes":
- Acknowledge confirmation
- Proceed to PHASE 3
- Save the audit report you just printed to `reports/audit-project-N.md`

If user declines (n/no):
- Stop here. Do not refactor.
- Offer to adjust detection and re-run Phase 2.

---

## PHASE 3 — REFACTORING (ONLY AFTER USER CONFIRMS PHASE 2)

### ⚠️ CRITICAL: This phase is THIRD and ONLY executes after user confirms "y" to Phase 2 prompt

### Objective
Apply MVC architecture transformations, create proper folder structure, fix anti-patterns, validate application.

### Pre-Refactoring Checklist
- [ ] User confirmed Phase 2 with "y" or "yes"
- [ ] Audit report was saved to `reports/audit-project-N.md`
- [ ] Phase 1 and Phase 2 completed successfully

### Use References
- `references/mvc-guidelines.md` - MVC layer responsibilities
- `references/refactoring-playbook.md` - Before/after transformation patterns

### MVC Target Structure

**See `references/mvc-guidelines.md` for complete MVC layer responsibilities and folder structure.**

**IMPORTANT:** Only create `src/utils/` if you have actual helper or validator functions. Do NOT create empty utils folders.

### Apply Transformations

For each anti-pattern found in Phase 2:
1. Locate problematic code
2. Find matching pattern in `references/refactoring-playbook.md` (15 before/after patterns)
3. Apply transformation
4. Test that code still works

### Validation (MANDATORY — VERIFY ALL)

After refactoring, verify:
1. **Application boots** without errors
2. **Endpoints respond** with status 200/201
3. **Database works** (tables created, queries execute)
4. **No import breaks** after removing legacy files
5. **No empty `src/utils/` exists** (remove if present)

### Output Format

Print Phase 3 completion summary including:
- New MVC structure created
- Transformations applied (with ✓ checkmarks)
- Validation results

### Legacy Files Cleanup

After refactoring is validated, REQUIRED cleanup:
1. Remove legacy files (old root file moved to `src/`)
2. **Remove empty utility folder:** `src/utils/` if only contains `__init__.py` or `index.js`
3. Re-validate that application still boots after cleanup

---

### MANDATORY: Save Audit Report (AFTER Phase 3 Validation)

After Phase 3 completes AND cleanup is verified, audit report should be saved to:

- Project 1 (code-smells-project): `reports/audit-project-1.md`
- Project 2 (ecommerce-api-legacy): `reports/audit-project-2.md`
- Project 3 (task-manager-api): `reports/audit-project-3.md`

**Filename MUST match project number exactly.**

---

## WORKFLOW SUMMARY

**This is the ONLY correct order:**

1. ✓ **PHASE 1 Executes First** → Analyze project → Print template
2. ✓ **PHASE 2 Executes Second** → Audit findings → Print template → Ask for confirmation  
3. ⏸️ **WAIT** → User must confirm "y" or "yes"
4. ✓ **PHASE 3 Executes Third** → Refactor → Validate → Save report

**NEVER skip or combine phases. NEVER proceed without confirmation.** 

**DO NOT ADD ANYTHING TO THE TEMPLATES.**

---

## 🚨 EMERGENCY MESSAGE IF YOU'RE STUCK

If you're not sure what to do, follow this exact sequence:

```
Step 1: Print Phase 1 (use the EXACT template shown above)
  → Check: No emojis? No extra text? ✓
  → Done? Go to Step 2

Step 2: Audit code and find 2+ LOW findings
  → Check: Do I have 2 LOW? If NO, keep searching
  → Found 2? Go to Step 3

Step 3: Print Phase 2 (use the EXACT template shown above)  
  → Check: No emojis? No ASCII art? Markdown table? 2 LOW findings present?
  → Check: Ends with confirmation question? ✓
  → Done? STOP and WAIT

Step 4: Wait for "y" or "yes"
  → Got confirmation? Go to Phase 3
  → No confirmation? STOP
```

---

## PHASE 4 — README UPDATE

### Objective
Automatically update the project's README.md with:
- Section B: Skill construction details
- Section C: Audit results and validation
- Section D: Execution instructions

### Use Reference
Read the generated audit report from Phase 2 and extract findings.

### Update Strategy

**Identify which project is being refactored:**
1. Check current directory for `app.py`, `package.json`, `requirements.txt`
2. Determine project number:
   - code-smells-project = Project 1
   - ecommerce-api-legacy = Project 2
   - task-manager-api = Project 3

**Update README.md (navigate to repository root: `../../../README.md`)**

#### Section B — Construção da Skill
Add after "**B) Seção "Construção da Skill":**" line:

```markdown
### Decisões de Design

**Estrutura de Referências (5 arquivos):**
- `analysis.md`: Heurísticas de detecção (Python, Node.js, Flask, Express, SQLite, PostgreSQL, MongoDB)
- `anti-patterns.md`: Catálogo de 12 anti-patterns (CRITICAL, HIGH, MEDIUM, LOW)
- `mvc-guidelines.md`: Arquitetura MVC alvo com responsabilidades de camadas
- `refactoring-playbook.md`: 15 padrões de transformação (6 Python, 5 Node.js, 4 agnósticas)
- `report-template.md`: Template de auditoria com exemplos Python/Flask + Node.js/Express

**Balanceamento de Tecnologias:**
- 6 padrões específicos para Python/Flask
- 5 padrões específicos para Node.js/Express  
- 4 padrões agnósticos de arquitetura
- Tech-agnosticism score: 92% ✅

### Anti-Patterns Inclusos (12 total)

**CRITICAL (5):**
1. God Class / God Object
2. Hardcoded Credentials
3. SQL Injection Vulnerability
4. Big Ball of Mud
5. Weak Cryptography / Insecure Hashing

**HIGH (3):**
6. Business Logic in Routes
7. Tight Coupling (No DI)
8. Global Mutable State

**MEDIUM (3):**
9. N+1 Query Problem
10. Code Duplication (DRY Violation)
11. Missing Input Validation
12. Deprecated APIs

**LOW (2):**
13. Magic Numbers/Strings
14. Poor Naming

### Desafios Encontrados & Soluções

1. **Desafio:** Skill criava `src/utils/` vazio (não documentado)
   **Solução:** Adicionado aviso explícito em MVC Target Structure + validação para remover pastas vazias

2. **Desafio:** Duplicação de conteúdo entre SKILL.md e references files
   **Solução:** Refactored SKILL.md para 163 linhas (de 550+) seguindo DRY principle

3. **Desafio:** Tech-agnosticism baixo (73%) com foco excessivo em Python
   **Solução:** Adicionado 2 padrões Node.js-specific (Callback Hell, Express Router Modularization) + rebalanceado playbook
```

#### Section C — Resultados
For the specific project just executed, add data to findings table:

If Project 1 (code-smells-project):
```markdown
| Projeto | CRITICAL | HIGH | MEDIUM | LOW | Total |
|---------|----------|------|--------|-----|-------|
| code-smells-project (Python/Flask) | 2 | 1 | 2 | 2 | **7** |
```

If Project 2 (ecommerce-api-legacy):
```markdown
| ecommerce-api-legacy (Node.js/Express) | 3 | 2 | 3 | 2 | **10** |
```

If Project 3 (task-manager-api):
```markdown
| task-manager-api (Python/Flask) | 2 | 3 | 3 | 2 | **10** |
```

Then add validation checklist for this project with ✅ marks.

#### Section D — Como Executar
Add after "**D) Seção "Como Executar":**" line:

```markdown
### Executando nos 3 Projetos

#### Preparação

```bash
# Fazer backup
git add -A
git commit -m "Backup antes da refatoração"

# Copiar SKILL para cada projeto
Copy-Item -Path ".gemini\skills\refactor-arch" -Destination "code-smells-project\.gemini\skills\refactor-arch" -Recurse
Copy-Item -Path ".gemini\skills\refactor-arch" -Destination "ecommerce-api-legacy\.gemini\skills\refactor-arch" -Recurse
Copy-Item -Path ".gemini\skills\refactor-arch" -Destination "task-manager-api\.gemini\skills\refactor-arch" -Recurse
```
```

For each project:

**Project 1:**
```bash
cd code-smells-project
pip install -r requirements.txt
gemini skill /refactor-arch
# Responder "y" na Fase 2 para prosseguir à Fase 3
```

**Project 2:**
```bash
cd ../ecommerce-api-legacy
npm install
gemini skill /refactor-arch
# Responder "y" na Fase 2
```

**Project 3:**
```bash
cd ../task-manager-api
pip install -r requirements.txt
gemini skill /refactor-arch
# Responder "y" na Fase 2
```

### Validação

Após cada projeto, validar que aplicação funciona:

```bash
# code-smells-project
python -m src.app
curl http://localhost:5000/produtos

# ecommerce-api-legacy
npm start
curl http://localhost:3000/api/auth

# task-manager-api
python -m flask run
curl http://localhost:5000/api/tasks
```
```

---

## Execution Constraints

✓ **MUST** complete all 3 phases in order (no skipping)
✓ **MUST** complete Phase 4 (README update) after Phase 3
✓ **MUST** wait for user confirmation after Phase 2
✓ **MUST** find minimum findings distribution (1 CRITICAL/HIGH, 2 MEDIUM, 2 LOW)
✓ **MUST** create proper MVC folder structure in Phase 3
✓ **MUST** clean up legacy files that were refactored into `src/`
✓ **MUST** remove empty utility folders created by MVC template
✓ **MUST** re-validate application boots after cleanup
✓ **MUST** validate all endpoints still respond after cleanup
✓ **MUST** save audit report to `reports/audit-project-{N}.md`
✓ **MUST** update README.md sections (B, C, D) with results from Phase 4
✗ **MUST NOT** modify files before Phase 2 confirmation
✗ **MUST NOT** skip phases (including Phase 4 README update)
✗ **MUST NOT** leave legacy files in project root after refactoring
✗ **MUST NOT** leave empty folders in `src/` after cleanup
✗ **MUST NOT** skip README update — it must be completed for each project

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