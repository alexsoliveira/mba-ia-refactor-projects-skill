const { PAYMENT_STATUS } = require('../config/settings');

class HttpError extends Error {
    constructor(statusCode, message) {
        super(message);
        this.statusCode = statusCode;
    }
}

class CheckoutService {
    constructor(dependencies) {
        this.userModel = dependencies.userModel;
        this.courseModel = dependencies.courseModel;
        this.enrollmentModel = dependencies.enrollmentModel;
        this.paymentModel = dependencies.paymentModel;
        this.auditLogModel = dependencies.auditLogModel;
        this.cacheService = dependencies.cacheService;
        this.hashPassword = dependencies.hashPassword;
    }

    async checkout(payload) {
        const { userName, email, password, courseId, cardNumber } = payload;

        if (!userName || !email || !courseId || !cardNumber) {
            throw new HttpError(400, 'Bad Request');
        }

        const course = await this.courseModel.findActiveById(courseId);
        if (!course) {
            throw new HttpError(404, 'Curso nao encontrado');
        }

        const status = cardNumber.startsWith('4') ? PAYMENT_STATUS.PAID : PAYMENT_STATUS.DENIED;
        if (status === PAYMENT_STATUS.DENIED) {
            throw new HttpError(400, 'Pagamento recusado');
        }

        let user = await this.userModel.findByEmail(email);
        if (!user) {
            const createdUser = await this.userModel.create({
                name: userName,
                email,
                passwordHash: this.hashPassword(password || '123456')
            });

            user = { id: createdUser.lastID, name: userName, email };
        }

        const enrollment = await this.enrollmentModel.create({
            userId: user.id,
            courseId
        });

        await this.paymentModel.create({
            enrollmentId: enrollment.lastID,
            amount: course.price,
            status
        });

        await this.auditLogModel.create(`Checkout curso ${courseId} por ${user.id}`);
        this.cacheService.save(`last_checkout_${user.id}`, course.title);

        return {
            msg: 'Sucesso',
            enrollment_id: enrollment.lastID
        };
    }
}

module.exports = {
    CheckoutService,
    HttpError
};
