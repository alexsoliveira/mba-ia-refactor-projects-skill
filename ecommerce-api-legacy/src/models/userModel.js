const { get, run } = require('../config/database');

class UserModel {
    constructor(db) {
        this.db = db;
    }

    findByEmail(email) {
        return get(this.db, 'SELECT id, name, email, pass FROM users WHERE email = ?', [email]);
    }

    create({ name, email, passwordHash }) {
        return run(this.db, 'INSERT INTO users (name, email, pass) VALUES (?, ?, ?)', [name, email, passwordHash]);
    }

    deleteById(id) {
        return run(this.db, 'DELETE FROM users WHERE id = ?', [id]);
    }
}

module.exports = UserModel;
