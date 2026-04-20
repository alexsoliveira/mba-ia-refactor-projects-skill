# Audit Report Template — Refactor Arch Skill

This document defines the **standard format** for Phase 2 (Audit) reports.

---

## Report Structure

Every audit report MUST contain:

1. **Header:** Project name, stack, files analyzed
2. **Summary Table:** Severity distribution (CRITICAL, HIGH, MEDIUM, LOW)
3. **Findings:** Ordered by severity, each with file + lines + example
4. **Confirmation:** Wait for user confirmation before Phase 3

---

## Example Report — Python/Flask (code-smells-project)

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

Query inside for loop causing exponential DB queries (1 + N queries per order)

Impact: 100 orders = 101 queries, severe performance degradation

---

### [HIGH] Business Logic in Models

File: models.py, controllers.py

Logic mixed with data access, no dedicated service layer

Impact: Untestable logic, tightly coupled layers

---

### [MEDIUM] Magic Numbers

File: models.py, Lines: 146-153

Discount rates hardcoded (10%, 5%, 2%) without reusable constants

---

### [MEDIUM] Code Duplication

File: controllers.py, models.py

Row serialization logic repeated in multiple functions

---

### [LOW] Magic Strings for Status

File: controllers.py

Order status ("pending", "approved") as plain string literals

---

### [LOW] Inconsistent Naming

File: database.py, controllers.py

Mix of Portuguese/English naming: listar_produtos() vs get_db()

================================
```

---

## Example Report — Node.js/Express (ecommerce-api-legacy)

```
================================
ARCHITECTURE AUDIT REPORT
================================

Project: ecommerce-api-legacy
Stack:   Node.js 18 + Express 4.18
Files:   3 analyzed | ~800 LOC total

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 3     |
| HIGH     | 2     |
| MEDIUM   | 2     |
| LOW      | 2     |

**Total Findings: 9**

---

## Findings

### [CRITICAL] Hardcoded Credentials Exposed

File: src/utils.js, Lines: 1-5

dbPass: "senha_super_secreta_prod_123"
paymentGatewayKey: "pk_live_1234567890abcdef"

Impact: Database exposed, payment gateway compromised if code leaks

---

### [CRITICAL] Weak Cryptography (Base64 as Hash)

File: src/utils.js, Lines: 19-25

function badCrypto(pwd) {
    return Buffer.from(pwd).toString('base64').substring(0, 10);
}

Impact: Passwords reversible, susceptible to rainbow table attacks

---

### [CRITICAL] Missing Authentication on Admin Endpoints

File: src/AppManager.js, Lines: 93-120

app.get('/api/admin/financial-report', (req, res) => {
    // NO AUTH CHECK
    db.query('SELECT SUM(revenue) ...');
});

Impact: Financial data exposed to all users, compliance breach

---

### [HIGH] Callback Hell (Nested Callbacks 4+ Levels)

File: src/AppManager.js, Lines: 20-80

Pyramid of doom with repetitive error handling at each level

Impact: Unreadable code, error propagation broken, untestable

---

### [HIGH] Business Logic Inline in Routes

File: src/AppManager.js, Lines: 20-80

Payment processing, user creation, enrollment all in route handler

Impact: Non-reusable logic, untestable without HTTP setup

---

### [MEDIUM] Global Mutable State

File: src/utils.js, Lines: 7-8

let globalCache = {}; let totalRevenue = 0;

Impact: Race conditions in concurrent requests, test pollution

---

### [MEDIUM] Database In-Memory (Non-Persistent)

File: src/AppManager.js, Line: 11

new sqlite3.Database(':memory:')

Impact: All data lost on restart, inadequate for production

---

### [LOW] Abbreviated Variable Names

File: src/AppManager.js, Lines: 23-25

let u = req.body.usr; let e = req.body.eml; let p = req.body.pwd;

---

### [LOW] Status as Magic Strings

File: src/AppManager.js, Line: 32

status = cc.startsWith("4") ? "PAID" : "DENIED"

================================
```

---

## Format Rules (STRICT)

✅ **MUST HAVE:**
- File + line numbers (exact locations)
- Code snippet (3-5 lines showing problem)
- Impact bullet points (2-3 consequences)
- Actionable recommendation

✅ **ORDERING:**
- Sort by severity: CRITICAL → HIGH → MEDIUM → LOW
- Most impactful findings first

✅ **TONE:**
- Professional, factual, non-judgmental
- Technical impact focused
- Always provide solution

---

## Completion Marker

After last finding, PAUSE and print:

```
================================
PHASE 2 COMPLETE
================================

Total Findings: X
  - CRITICAL: N
  - HIGH: N
  - MEDIUM: N
  - LOW: N

Proceed with refactoring (Phase 3)? [y/n]
```

**STOP HERE.** Wait for user confirmation before executing Phase 3.

---

## Por que esse template está forte (ponto crítico)

Esse modelo não é só “bonito” — ele resolve exatamente o que faz uma skill funcionar bem:

- Segue padrão real de auditoria (summary, scope, findings, recommendations) :contentReference[oaicite:1]{index=1}  
- Força **evidência concreta (arquivo + linha + código)** → essencial para credibilidade técnica :contentReference[oaicite:2]{index=2}  
- Separa claramente:
  - análise
  - auditoria
  - plano de refatoração  
- Já prepara a **Fase 3 automaticamente**
- Inclui **trigger de confirmação obrigatório** (requisito do desafio)

---

## Próximo passo recomendado

Agora que você já tem:

- ✔ analysis.md  
- ✔ anti-patterns.md  
- ✔ mvc-guidelines.md  
- ✔ report-template.md  

Falta o mais estratégico:

👉 **refactoring-playbook.md (o coração da Fase 3)**

Se quiser, eu posso :contentReference[oaicite:4]{index=4}:
- 8+ transformações reais (God Class → MVC, Controller fat → Service, etc.)
- exemplos before/after em Python e Node
- regras agnósticas (como você pediu)

Quer seguir para isso?
::contentReference[oaicite:3]{index=3}