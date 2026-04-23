const { settings } = require('../config/settings');
const { HttpError } = require('../services/checkoutService');

function ensureAdmin(req, _res, next) {
    const token = req.header('x-admin-token');
    if (!token || token !== settings.adminToken) {
        next(new HttpError(403, 'Forbidden'));
        return;
    }

    next();
}

module.exports = ensureAdmin;
