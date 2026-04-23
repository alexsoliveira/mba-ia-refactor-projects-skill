# ecommerce-api-legacy

LMS API (com fluxo de checkout) em Node.js/Express usada como entrada do desafio `refactor-arch`.

## Como rodar

```bash
npm install
npm start
```

A aplicação sobe em `http://localhost:3000`. O banco SQLite persiste em `data/ecommerce.sqlite`, carrega seeds apenas quando a base ainda está vazia e o endpoint `GET /api/admin/financial-report` exige o header `x-admin-token` (valor padrão local: `dev-admin-token`).

Exemplos de requisições estão em `api.http`.
