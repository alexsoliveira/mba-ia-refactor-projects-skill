const sqlite3 = require('sqlite3').verbose();
const { settings, PAYMENT_STATUS } = require('./settings');

function run(db, sql, params = []) {
    return new Promise((resolve, reject) => {
        db.run(sql, params, function onRun(err) {
            if (err) {
                reject(err);
                return;
            }

            resolve({
                lastID: this.lastID,
                changes: this.changes
            });
        });
    });
}

function get(db, sql, params = []) {
    return new Promise((resolve, reject) => {
        db.get(sql, params, (err, row) => {
            if (err) {
                reject(err);
                return;
            }

            resolve(row || null);
        });
    });
}

function all(db, sql, params = []) {
    return new Promise((resolve, reject) => {
        db.all(sql, params, (err, rows) => {
            if (err) {
                reject(err);
                return;
            }

            resolve(rows || []);
        });
    });
}

async function ensureSchema(db) {
    await run(db, 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, pass TEXT)');
    await run(db, 'CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY, title TEXT, price REAL, active INTEGER)');
    await run(db, 'CREATE TABLE IF NOT EXISTS enrollments (id INTEGER PRIMARY KEY, user_id INTEGER, course_id INTEGER)');
    await run(db, 'CREATE TABLE IF NOT EXISTS payments (id INTEGER PRIMARY KEY, enrollment_id INTEGER, amount REAL, status TEXT)');
    await run(db, 'CREATE TABLE IF NOT EXISTS audit_logs (id INTEGER PRIMARY KEY, action TEXT, created_at DATETIME)');
}

async function ensureSeedData(db) {
    const userCount = await get(db, 'SELECT COUNT(*) AS count FROM users');
    if (userCount && userCount.count > 0) {
        return;
    }

    await run(db, 'INSERT INTO users (name, email, pass) VALUES (?, ?, ?)', ['Leonan', 'leonan@fullcycle.com.br', 'seed-user-password']);
    await run(db, 'INSERT INTO courses (title, price, active) VALUES (?, ?, ?)', ['Clean Architecture', 997.0, 1]);
    await run(db, 'INSERT INTO courses (title, price, active) VALUES (?, ?, ?)', ['Docker', 497.0, 1]);
    await run(db, 'INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)', [1, 1]);
    await run(db, 'INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)', [1, 997.0, PAYMENT_STATUS.PAID]);
}

async function initializeDatabase() {
    const db = new sqlite3.Database(settings.dbPath);
    await ensureSchema(db);
    await ensureSeedData(db);
    return db;
}

module.exports = {
    initializeDatabase,
    run,
    get,
    all
};
