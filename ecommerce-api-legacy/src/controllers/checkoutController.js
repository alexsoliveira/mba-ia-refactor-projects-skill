class CheckoutController {
    constructor(checkoutService) {
        this.checkoutService = checkoutService;
    }

    async checkout(body) {
        return this.checkoutService.checkout({
            userName: body.usr,
            email: body.eml,
            password: body.pwd,
            courseId: body.c_id,
            cardNumber: body.card
        });
    }
}

module.exports = CheckoutController;
