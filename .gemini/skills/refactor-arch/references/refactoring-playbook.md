# Refactoring Playbook

## Objetivo

Este playbook define **padrões concretos de refatoração** para transformar codebases legadas em uma arquitetura **MVC (Model-View-Controller)**, eliminando anti-patterns e melhorando qualidade, segurança e manutenibilidade.

Cada padrão contém:

* Sinais de detecção
* Estratégia de refatoração
* Exemplo antes/depois

---

# 1. God Class → Separação em MVC

## Sinais

* Arquivo com múltiplas responsabilidades:

  * lógica de negócio
  * acesso a banco
  * rotas/endpoints

## Estratégia

* Extrair:

  * Models → acesso a dados
  * Controllers → regras de negócio
  * Routes/Views → endpoints

## Antes (Python Flask)

```python
# models.py
def criar_usuario(data):
    conn.execute("INSERT INTO users ...")
    return {"status": "ok"}

@app.route("/users", methods=["POST"])
def route():
    return criar_usuario(request.json)
```

## Depois

```python
# models/user_model.py
def insert_user(data):
    conn.execute("INSERT INTO users ...")

# controllers/user_controller.py
def create_user(data):
    insert_user(data)
    return {"status": "ok"}

# routes/user_routes.py
@app.route("/users", methods=["POST"])
def create():
    return create_user(request.json)
```

---

# 2. Hardcoded Credentials → Configuração Centralizada

## Sinais

* Senhas, tokens ou chaves no código

## Estratégia

* Extrair para arquivo de config/env
* Usar variáveis de ambiente

## Antes

```python
SECRET_KEY = "123456"
DB_URL = "postgres://user:pass@localhost"
```

## Depois

```python
# config/settings.py
import os

SECRET_KEY = os.getenv("SECRET_KEY")
DB_URL = os.getenv("DB_URL")
```

---

# 3. Business Logic em Controller → Service Layer

## Sinais

* Controllers com regras complexas

## Estratégia

* Criar camada de serviço

## Antes

```javascript
app.post("/order", (req, res) => {
  if(req.body.total > 100){
    // desconto
  }
});
```

## Depois

```javascript
// services/orderService.js
function processOrder(data){
  if(data.total > 100){
    // desconto
  }
}

// controller
app.post("/order", (req, res) => {
  processOrder(req.body);
});
```

---

# 4. SQL Inline → Model Abstraction

## Sinais

* Queries SQL espalhadas

## Estratégia

* Centralizar em models

## Antes

```python
def get_users():
    return conn.execute("SELECT * FROM users")
```

## Depois

```python
# models/user_model.py
def find_all():
    return conn.execute("SELECT * FROM users")

# controller
def get_users():
    return find_all()
```

---

# 5. Falta de Error Handling → Middleware Global

## Sinais

* try/catch repetido ou inexistente

## Estratégia

* Criar handler central

## Antes

```python
@app.route("/users")
def get_users():
    try:
        ...
    except:
        return "error"
```

## Depois

```python
# middlewares/error_handler.py
def handle_error(e):
    return {"error": str(e)}, 500
```

---

# 6. Rotas Misturadas → Modularização de Routes

## Sinais

* Todas rotas em um único arquivo

## Estratégia

* Separar por domínio

## Antes

```python
@app.route("/users")
@app.route("/orders")
@app.route("/products")
```

## Depois

```
routes/
  user_routes.py
  order_routes.py
  product_routes.py
```

---

# 7. Estado Global Mutável → Injeção de Dependência

## Sinais

* Variáveis globais compartilhadas

## Estratégia

* Passar dependências explicitamente

## Antes

```python
db = Database()
```

## Depois

```python
def create_user(db, data):
    db.insert(data)
```

---

# 8. APIs Deprecated → Substituição Moderna

## Sinais

* Uso de APIs obsoletas

## Estratégia

* Substituir por versão atual

## Antes (Flask antigo)

```python
from flask.ext.sqlalchemy import SQLAlchemy
```

## Depois

```python
from flask_sqlalchemy import SQLAlchemy
```

---

# 9. Código Duplicado → Funções Reutilizáveis

## Sinais

* Blocos repetidos

## Estratégia

* Extrair função comum

## Antes

```python
if not user:
    return {"error": "not found"}
```

## Depois

```python
def validate_user(user):
    if not user:
        raise Exception("not found")
```

---

# 10. Falta de Entry Point → Composition Root

## Sinais

* Inicialização espalhada

## Estratégia

* Criar ponto único de inicialização

## Depois (estrutura final)

```
src/
  config/
  models/
  controllers/
  routes/
  middlewares/
  app.py
```

---

# 11. Callback Hell → Async/Await (Node.js/Express)

## Sinais

* Callbacks aninhados (pyramid of doom)
* Error handling repetido em cada nível
* Difícil rastrear fluxo de execução

## Estratégia

* Converter para async/await ou Promises
* Centralizar error handling

## Antes (Node.js)

```javascript
app.post('/enroll', (req, res) => {
    db.get('SELECT * FROM users WHERE id = ?', req.body.userId, (err, user) => {
        if (err) return res.status(500).json({error: err});
        
        db.run('INSERT INTO enrollments ...', (err) => {
            if (err) return res.status(500).json({error: err});
            
            sendEmail(user.email, (err) => {
                if (err) return res.status(500).json({error: err});
                res.json({success: true});
            });
        });
    });
});
```

## Depois (Node.js)

```javascript
// controllers/enrollmentController.js
async function enrollUser(userId) {
    const user = await db.get('SELECT * FROM users WHERE id = ?', userId);
    await db.run('INSERT INTO enrollments ...');
    await sendEmail(user.email);
    return {success: true};
}

// routes/enrollmentRoutes.js
router.post('/enroll', async (req, res) => {
    try {
        const result = await enrollUser(req.body.userId);
        res.json(result);
    } catch(err) {
        errorHandler(err, res);
    }
});
```

---

# 12. Database Connection Inline → Persistent Connection (Node.js)

## Sinais

* Banco de dados em memória (`:memory:`)
* Nova conexão por requisição
* Sem pooling de conexões

## Estratégia

* Criar persistent database connection
* Usar pool para múltiplas requisições
* Externalizar configuração

## Antes (Node.js)

```javascript
// app.js
const sqlite3 = require('sqlite3');

app.post('/users', (req, res) => {
    const db = new sqlite3.Database(':memory:');  // ❌ Nova conexão a cada request!
    db.run('INSERT INTO users ...', (err) => {
        res.json({ok: true});
    });
});
```

## Depois (Node.js)

```javascript
// config/database.js
const sqlite3 = require('sqlite3');
const db = new sqlite3.Database('./app.db');  // ✅ Persistent, single instance

module.exports = db;

// controllers/userController.js
const db = require('../config/database');

async function createUser(data) {
    return new Promise((resolve, reject) => {
        db.run('INSERT INTO users ...', (err) => {
            if(err) reject(err);
            resolve({ok: true});
        });
    });
}

module.exports = { createUser };
```

---

# 13. Route Handlers com Lógica Inline → Express Router Modularizado (Node.js)

## Sinais

* Todas as rotas em um único arquivo
* app.get/app.post espalhado
* Sem separação por domínio

## Estratégia

* Usar express.Router() para modularizar
* Separar por domínio (users, products, orders)
* Importar blueprints no app.js

## Antes (Node.js)

```javascript
// app.js
const express = require('express');
const app = express();

app.get('/users', (req, res) => { ... });
app.post('/users', (req, res) => { ... });
app.get('/products', (req, res) => { ... });
app.post('/products', (req, res) => { ... });
app.get('/orders', (req, res) => { ... });
app.post('/orders', (req, res) => { ... });
```

## Depois (Node.js)

```javascript
// routes/userRoutes.js
const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');

router.get('/', userController.listUsers);
router.post('/', userController.createUser);

module.exports = router;

// routes/productRoutes.js (similar structure)
// routes/orderRoutes.js (similar structure)

// app.js
const express = require('express');
const userRoutes = require('./routes/userRoutes');
const productRoutes = require('./routes/productRoutes');
const orderRoutes = require('./routes/orderRoutes');

const app = express();
app.use('/users', userRoutes);
app.use('/products', productRoutes);
app.use('/orders', orderRoutes);
```

---

# 14. Weak Cryptography → Bcrypt/Argon2

## Sinais

* MD5, SHA1, Base64 para senhas
* Sem salt
* Custom crypto implementations

## Estratégia

* Usar bcrypt ou argon2
* Extrair para função centralizada

## Antes (Python)

```python
import hashlib

def set_password(self, pwd):
    self.password = hashlib.md5(pwd.encode()).hexdigest()
```

## Depois (Python)

```python
import bcrypt

def set_password(self, pwd):
    salt = bcrypt.gensalt()
    self.password = bcrypt.hashpw(pwd.encode(), salt).decode()
```

## Antes (Node.js)

```javascript
function badCrypto(pwd) {
    let hash = "";
    for(let i = 0; i < 10000; i++) {
        hash += Buffer.from(pwd).toString('base64').substring(0, 2);
    }
    return hash.substring(0, 10);
}
```

## Depois (Node.js)

```javascript
const bcrypt = require('bcrypt');

async function hashPassword(pwd) {
    const salt = await bcrypt.genSalt();
    return await bcrypt.hash(pwd, salt);
}
```

---

# 15. Deprecated APIs → Modern Equivalents

## Sinais

* `from flask.ext.sqlalchemy` (deprecated)
* Old middleware patterns
* Obsolete library versions

## Estratégia

* Update imports
* Use current API versions
* Replace old patterns

## Antes (Python/Flask)

```python
from flask.ext.sqlalchemy import SQLAlchemy  # ❌ Deprecated
from flask.ext.cors import CORS              # ❌ Deprecated
```

## Depois (Python/Flask)

```python
from flask_sqlalchemy import SQLAlchemy  # ✅ Current
from flask_cors import CORS              # ✅ Current
```

---

# Regras Gerais de Refatoração

* Nunca quebrar contratos de API existentes
* Preservar endpoints originais
* Refatorar incrementalmente
* Validar após cada mudança
* Priorizar problemas CRITICAL → LOW

---

# Checklist de Aplicação

Antes de finalizar:

* [ ] Nenhuma lógica de negócio em routes
* [ ] Nenhuma query SQL fora de models
* [ ] Configuração externalizada
* [ ] Controllers organizados por domínio
* [ ] Error handling centralizado
* [ ] Estrutura MVC aplicada
* [ ] Código duplicado removido

---

# Resultado Esperado

Uma codebase com:

* Separação clara de responsabilidades
* Alta coesão e baixo acoplamento
* Estrutura previsível e escalável
* Pronta para testes e evolução
