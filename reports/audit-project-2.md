================================
ARCHITECTURE AUDIT REPORT
================================

Project: ecommerce-api-legacy
Stack:   Node.js + Express 4.18.2
Files:   3 analyzed | ~180 LOC total

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

### [CRITICAL] Hardcoded production credentials in source

File: src/utils.js, Lines: 1-6

```javascript
const config = {
    dbUser: "admin_master",
    dbPass: "senha_super_secreta_prod_123",
    paymentGatewayKey: "pk_live_1234567890abcdef",
    smtpUser: "no-reply@fullcycle.com.br",
```

Impact: Database and payment secrets are exposed to anyone with source access, enabling credential compromise.

---

### [CRITICAL] Reversible password handling masquerading as crypto

File: src/utils.js, Lines: 18-22

```javascript
    let hash = "";
    for(let i = 0; i < 10000; i++) {
        hash += Buffer.from(pwd).toString('base64').substring(0, 2);
    }
    return hash.substring(0, 10);
```

Impact: Password storage is predictable and reversible enough to make brute-force recovery practical.

---

### [CRITICAL] Unauthenticated financial report endpoint

File: src/AppManager.js, Lines: 80-84

```javascript
        app.get('/api/admin/financial-report', (req, res) => {
            let report = [];

            this.db.all("SELECT * FROM courses", [], (err, courses) => {
                if (err) return res.status(500).send("Erro DB");
```

Impact: Any caller can access administrative revenue data without authentication or authorization checks.

---

### [HIGH] Callback hell in checkout flow

File: src/AppManager.js, Lines: 40-57

```javascript
                this.db.get("SELECT id FROM users WHERE email = ?", [e], (err, user) => {
                    if (err) return res.status(500).send("Erro DB");

                    let processPaymentAndEnroll = (userId) => {

                        console.log(`Processando cartao ${cc} na chave ${config.paymentGatewayKey}`);
```

Impact: Deeply nested async control flow makes failures harder to reason about and increases regression risk in the checkout path.

---

### [HIGH] Payment and enrollment business rules embedded in route setup

File: src/AppManager.js, Lines: 43-60

```javascript
                    let processPaymentAndEnroll = (userId) => {

                        console.log(`Processando cartao ${cc} na chave ${config.paymentGatewayKey}`);
                        let status = cc.startsWith("4") ? "PAID" : "DENIED";

```

Impact: Checkout rules are tightly coupled to HTTP wiring, preventing isolation, reuse, and clean MVC boundaries.

---

### [MEDIUM] Mutable global shared state exported from utilities

File: src/utils.js, Lines: 9-13

```javascript
let globalCache = {};
let totalRevenue = 0;

function logAndCache(key, data) {
    console.log(`[LOG] Salvando no cache: ${key}`);
```

Impact: Shared mutable state creates hidden coupling across requests and makes runtime behavior harder to predict or test.

---

### [MEDIUM] Non-persistent in-memory database for application state

File: src/AppManager.js, Lines: 5-8

```javascript
    constructor() {

        this.db = new sqlite3.Database(':memory:');
    }
```

Impact: All business data is lost on restart, making the API behavior unrealistic and unsafe for any persistent workflow.

---

### [LOW] Abbreviated variable names obscure request intent

File: src/AppManager.js, Lines: 29-33

```javascript
            let u = req.body.usr;
            let e = req.body.eml;
            let p = req.body.pwd;
            let cid = req.body.c_id;
            let cc = req.body.card;
```

Impact: Cryptic identifiers slow review and increase the chance of introducing mistakes during maintenance.

---

### [LOW] Payment statuses encoded as magic strings

File: src/AppManager.js, Lines: 45-48

```javascript
                        console.log(`Processando cartao ${cc} na chave ${config.paymentGatewayKey}`);
                        let status = cc.startsWith("4") ? "PAID" : "DENIED";

                        if (status === "DENIED") return res.status(400).send("Pagamento recusado");
```

Impact: Hardcoded status literals invite drift and typos because the payment state contract is not centralized.

---

================================
PHASE 2 COMPLETE
================================

Total Findings: 9
  - CRITICAL: 3
  - HIGH: 2
  - MEDIUM: 2
  - LOW: 2

================================

Proceed with refactoring (Phase 3)? [y/n]
