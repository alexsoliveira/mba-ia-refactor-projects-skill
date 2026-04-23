const { PAYMENT_STATUS } = require('../config/settings');

class ReportService {
    constructor(dependencies) {
        this.courseModel = dependencies.courseModel;
        this.enrollmentModel = dependencies.enrollmentModel;
    }

    async buildFinancialReport() {
        const courses = await this.courseModel.listAll();
        const report = [];

        for (const course of courses) {
            const enrollmentRows = await this.enrollmentModel.findAllWithUsersAndPaymentsByCourseId(course.id);
            const courseData = {
                course: course.title,
                revenue: 0,
                students: []
            };

            for (const row of enrollmentRows) {
                if (row.paymentStatus === PAYMENT_STATUS.PAID) {
                    courseData.revenue += row.amount || 0;
                }

                courseData.students.push({
                    student: row.userName || 'Unknown',
                    paid: row.amount || 0
                });
            }

            report.push(courseData);
        }

        return report;
    }
}

module.exports = ReportService;
