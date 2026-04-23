const express = require('express');
const AppManager = require('./AppManager');
const errorHandler = require('./middlewares/errorHandler');
const { settings } = require('./config/settings');
const { initializeDatabase } = require('./config/database');

async function start() {
    const app = express();
    app.use(express.json());

    const db = await initializeDatabase();
    const manager = new AppManager(db);
    manager.initDb();
    manager.setupRoutes(app);
    app.use(errorHandler);

    app.listen(settings.port, () => {
        console.log(`Frankenstein LMS rodando na porta ${settings.port}...`);
    });
}

start().catch((err) => {
    console.error('Falha ao iniciar aplicacao', err);
    process.exit(1);
});
