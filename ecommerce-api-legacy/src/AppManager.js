const CourseModel = require('./models/courseModel');
const UserModel = require('./models/userModel');
const EnrollmentModel = require('./models/enrollmentModel');
const PaymentModel = require('./models/paymentModel');
const AuditLogModel = require('./models/auditLogModel');
const CacheService = require('./services/cacheService');
const { hashPassword } = require('./services/authService');
const { CheckoutService } = require('./services/checkoutService');
const ReportService = require('./services/reportService');
const CheckoutController = require('./controllers/checkoutController');
const AdminController = require('./controllers/adminController');
const UserController = require('./controllers/userController');
const buildRouter = require('./routes');

class AppManager {
    constructor(db) {
        this.db = db;
    }

    initDb() {
        return this.db;
    }

    setupRoutes(app) {
        const userModel = new UserModel(this.db);
        const courseModel = new CourseModel(this.db);
        const enrollmentModel = new EnrollmentModel(this.db);
        const paymentModel = new PaymentModel(this.db);
        const auditLogModel = new AuditLogModel(this.db);
        const cacheService = new CacheService();

        const checkoutService = new CheckoutService({
            userModel,
            courseModel,
            enrollmentModel,
            paymentModel,
            auditLogModel,
            cacheService,
            hashPassword
        });

        const reportService = new ReportService({
            courseModel,
            enrollmentModel
        });

        app.use(
            buildRouter({
                checkoutController: new CheckoutController(checkoutService),
                adminController: new AdminController(reportService),
                userController: new UserController(userModel)
            })
        );
    }
}

module.exports = AppManager;
