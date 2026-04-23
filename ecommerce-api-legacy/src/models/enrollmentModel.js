const { run, all } = require('../config/database');

class EnrollmentModel {
    constructor(db) {
        this.db = db;
    }

    create({ userId, courseId }) {
        return run(this.db, 'INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)', [userId, courseId]);
    }

    findAllWithUsersAndPaymentsByCourseId(courseId) {
        return all(
            this.db,
            `SELECT
                enrollments.id AS enrollmentId,
                users.name AS userName,
                users.email AS userEmail,
                payments.amount AS amount,
                payments.status AS paymentStatus
             FROM enrollments
             LEFT JOIN users ON users.id = enrollments.user_id
             LEFT JOIN payments ON payments.enrollment_id = enrollments.id
             WHERE enrollments.course_id = ?
             ORDER BY enrollments.id`,
            [courseId]
        );
    }
}

module.exports = EnrollmentModel;
