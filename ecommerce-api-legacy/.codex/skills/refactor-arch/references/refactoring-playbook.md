# Refactoring Playbook

Purpose: concrete Phase 3 transformations with before/after guidance.

Use these patterns to fix Phase 2 findings while preserving behavior.

## 1) Monolith Split into MVC

Before: one module mixes routes, business logic, and SQL.

```python
# app.py
@app.route("/users/<int:user_id>")
def get_user(user_id):
    conn = sqlite3.connect("app.db")
    row = conn.execute(
        "SELECT id, name, email FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    conn.close()

    if not row:
        return {"error": "User not found"}, 404

    return {"id": row[0], "name": row[1], "email": row[2]}
```

After: move route mapping to `routes`, orchestration to `controllers`, SQL to `models`.

```python
# routes/user_routes.py
@user_bp.get("/users/<int:user_id>")
def get_user(user_id):
    return user_controller.get_user(user_id)
```

```python
# controllers/user_controller.py
from models.user_model import find_user_by_id

def get_user(user_id):
    row = find_user_by_id(user_id)
    if not row:
        return {"error": "User not found"}, 404
    return {"id": row["id"], "name": row["name"], "email": row["email"]}
```

```python
# models/user_model.py
from config.database import get_connection

def find_user_by_id(user_id):
    conn = get_connection()
    return conn.execute(
        "SELECT id, name, email FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
```

## 2) Hardcoded Secrets -> Config

Before: secrets and runtime values live directly in source.

```python
app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret-key"
ADMIN_TOKEN = "dev-admin-token"
SMTP_PASSWORD = "123456"
```

After: read from environment-backed config module.

```python
# config/settings.py
import os

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "dev-admin-token")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
```

```python
# app.py
from config.settings import Settings

app = Flask(__name__)
app.config.from_object(Settings)
```

## 3) Raw SQL Concat -> Parameterized Queries

Before: concatenated SQL allows injection and breaks query planning.

```python
def find_product(product_id):
    query = "SELECT * FROM products WHERE id = " + str(product_id)
    return conn.execute(query).fetchone()
```

After: use placeholders with bound values.

```python
def find_product(product_id):
    query = "SELECT * FROM products WHERE id = ?"
    return conn.execute(query, (product_id,)).fetchone()
```

```sql
-- Before
SELECT * FROM users WHERE email = '" + email + "'

-- After
SELECT * FROM users WHERE email = ?
```

## 4) Arbitrary SQL Endpoint -> Remove/Restrict

Before: a generic admin endpoint executes any SQL received from the client.

```js
app.post("/admin/query", async (req, res) => {
  const sql = req.body.sql;
  const rows = await db.all(sql);
  res.json(rows);
});
```

After: replace it with a bounded controller action and explicit query allowlist.

```js
const allowedReports = {
  sales_summary: "SELECT COUNT(*) AS total, SUM(amount) AS revenue FROM orders",
};

app.get("/admin/reports/:reportName", requireAdmin, async (req, res, next) => {
  const sql = allowedReports[req.params.reportName];
  if (!sql) {
    return res.status(404).json({ error: "Report not found" });
  }

  try {
    const rows = await db.all(sql);
    res.json(rows);
  } catch (error) {
    next(error);
  }
});
```

## 5) Business Logic in Routes -> Controller/Service

Before: routes compute discounts, validate stock, and persist side effects inline.

```python
@app.post("/orders")
def create_order():
    payload = request.get_json()
    subtotal = sum(item["price"] * item["quantity"] for item in payload["items"])

    if subtotal > 500:
        subtotal *= 0.9

    for item in payload["items"]:
        conn.execute(
            "UPDATE products SET stock = stock - ? WHERE id = ?",
            (item["quantity"], item["product_id"]),
        )

    conn.execute("INSERT INTO orders(total) VALUES(?)", (subtotal,))
    conn.commit()
    return {"total": subtotal}, 201
```

After: route delegates to controller/service use case.

```python
# routes/order_routes.py
@order_bp.post("/orders")
def create_order():
    return order_controller.create_order(request.get_json())
```

```python
# controllers/order_controller.py
from services.order_service import place_order

def create_order(payload):
    result = place_order(payload)
    return result, 201
```

```python
# services/order_service.py
def place_order(payload):
    subtotal = sum(item["price"] * item["quantity"] for item in payload["items"])
    total = subtotal * 0.9 if subtotal > 500 else subtotal
    reserve_stock(payload["items"])
    save_order(total, payload["items"])
    return {"total": total}
```

## 6) N+1 Queries -> Join/Batch

Before: the code fetches parent records and then opens one query per item.

```python
orders = conn.execute("SELECT id, user_id FROM orders").fetchall()
result = []

for order in orders:
    items = conn.execute(
        "SELECT product_id, quantity FROM order_items WHERE order_id = ?",
        (order["id"],),
    ).fetchall()
    result.append({"id": order["id"], "user_id": order["user_id"], "items": items})
```

After: fetch related data in batch and assemble in memory.

```python
orders = conn.execute("SELECT id, user_id FROM orders").fetchall()
order_ids = [order["id"] for order in orders]

items = conn.execute(
    f"SELECT order_id, product_id, quantity FROM order_items WHERE order_id IN ({','.join('?' for _ in order_ids)})",
    tuple(order_ids),
).fetchall()

items_by_order = {}
for item in items:
    items_by_order.setdefault(item["order_id"], []).append(item)

result = [
    {
        "id": order["id"],
        "user_id": order["user_id"],
        "items": items_by_order.get(order["id"], []),
    }
    for order in orders
]
```

## 7) Duplicate Mapping/Validation -> Shared Utilities

Before: row mapping and payload validation are repeated in several handlers.

```python
def serialize_user(row):
    return {"id": row["id"], "name": row["name"], "email": row["email"]}

@app.post("/users")
def create_user():
    payload = request.get_json()
    if "name" not in payload or "email" not in payload:
        return {"error": "Missing required fields"}, 400
    ...

@app.put("/users/<int:user_id>")
def update_user(user_id):
    payload = request.get_json()
    if "name" not in payload or "email" not in payload:
        return {"error": "Missing required fields"}, 400
    ...
```

After: centralize serializers and validators.

```python
# utils/validators.py
def validate_user_payload(payload):
    required = ("name", "email")
    missing = [field for field in required if not payload.get(field)]
    return missing
```

```python
# utils/serializers.py
def serialize_user(row):
    return {"id": row["id"], "name": row["name"], "email": row["email"]}
```

```python
# controllers/user_controller.py
def create_user(payload):
    missing = validate_user_payload(payload)
    if missing:
        return {"error": f"Missing fields: {', '.join(missing)}"}, 400
    ...
```

## 8) Global Mutable State -> Scoped Dependency Management

Before: mutable globals make state unpredictable across requests.

```js
let cachedReport = null;
let dbConnection = null;

function getDb() {
  if (!dbConnection) {
    dbConnection = createConnection();
  }
  return dbConnection;
}

app.get("/report", async (req, res) => {
  if (!cachedReport) {
    cachedReport = await buildReport(getDb());
  }
  res.json(cachedReport);
});
```

After: keep app-level dependencies explicit and request flow stateless.

```js
function createApp({ db, cacheService }) {
  const app = express();

  app.get("/report", async (req, res, next) => {
    try {
      const cached = cacheService.get("report");
      if (cached) {
        return res.json(cached);
      }

      const report = await buildReport(db);
      cacheService.set("report", report);
      res.json(report);
    } catch (error) {
      next(error);
    }
  });

  return app;
}
```

## 9) Magic Strings/Numbers -> Constants/Enums

Before: status literals and thresholds are duplicated inline.

```python
if task["priority"] > 7:
    task["status"] = "urgent"
elif task["priority"] > 3:
    task["status"] = "in_progress"
else:
    task["status"] = "pending"
```

After: centralize constants and reuse the same vocabulary.

```python
# utils/constants.py
STATUS_PENDING = "pending"
STATUS_IN_PROGRESS = "in_progress"
STATUS_URGENT = "urgent"
URGENT_PRIORITY_THRESHOLD = 7
ACTIVE_PRIORITY_THRESHOLD = 3
```

```python
from utils.constants import (
    ACTIVE_PRIORITY_THRESHOLD,
    STATUS_IN_PROGRESS,
    STATUS_PENDING,
    STATUS_URGENT,
    URGENT_PRIORITY_THRESHOLD,
)

if task["priority"] > URGENT_PRIORITY_THRESHOLD:
    task["status"] = STATUS_URGENT
elif task["priority"] > ACTIVE_PRIORITY_THRESHOLD:
    task["status"] = STATUS_IN_PROGRESS
else:
    task["status"] = STATUS_PENDING
```

## 10) Deprecated APIs -> Modern Equivalents

Before: legacy APIs remain in the code after framework upgrades.

```python
from flask import escape

safe_name = escape(user_input)
```

After: replace deprecated imports/methods with supported equivalents.

```python
from markupsafe import escape

safe_name = escape(user_input)
```

```js
// Before
app.del("/users/:id", deleteUser);

// After
app.delete("/users/:id", deleteUser);
```

## Execution Notes

- Apply smallest safe change set first.
- Keep endpoint contract stable.
- Validate boot and key endpoints after each major transformation group.
- After successful validation, synchronize the repository root `README.md` so challenge deliverables and evidence stay consistent with the refactored code and saved audit report.

## Cross-Link

Target design constraints are defined in `references/mvc-guidelines.md`.
