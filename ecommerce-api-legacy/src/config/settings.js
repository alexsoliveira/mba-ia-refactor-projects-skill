const path = require('path');

const PAYMENT_STATUS = Object.freeze({
    PAID: 'PAID',
    DENIED: 'DENIED'
});

const settings = {
    port: Number(process.env.PORT || 3000),
    dbPath: process.env.DB_PATH || path.join(__dirname, '..', '..', 'data', 'ecommerce.sqlite'),
    paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || 'sandbox_payment_key',
    smtpUser: process.env.SMTP_USER || 'no-reply@example.local',
    adminToken: process.env.ADMIN_TOKEN || 'dev-admin-token'
};

module.exports = {
    settings,
    PAYMENT_STATUS
};
