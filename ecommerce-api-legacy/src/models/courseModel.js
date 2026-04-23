const { get, all } = require('../config/database');

class CourseModel {
    constructor(db) {
        this.db = db;
    }

    findActiveById(courseId) {
        return get(this.db, 'SELECT * FROM courses WHERE id = ? AND active = 1', [courseId]);
    }

    listAll() {
        return all(this.db, 'SELECT * FROM courses ORDER BY id');
    }
}

module.exports = CourseModel;
