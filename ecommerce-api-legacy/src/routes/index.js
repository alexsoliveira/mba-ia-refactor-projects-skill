const express = require('express');
const ensureAdmin = require('../middlewares/adminAuth');

function buildRouter(dependencies) {
    const router = express.Router();
    const { checkoutController, adminController, userController } = dependencies;

    router.post('/api/checkout', async (req, res, next) => {
        try {
            const result = await checkoutController.checkout(req.body || {});
            res.status(200).json(result);
        } catch (err) {
            next(err);
        }
    });

    router.get('/api/admin/financial-report', ensureAdmin, async (_req, res, next) => {
        try {
            const result = await adminController.getFinancialReport();
            res.json(result);
        } catch (err) {
            next(err);
        }
    });

    router.delete('/api/users/:id', async (req, res, next) => {
        try {
            const result = await userController.deleteUser(req.params.id);
            res.send(result);
        } catch (err) {
            next(err);
        }
    });

    return router;
}

module.exports = buildRouter;
