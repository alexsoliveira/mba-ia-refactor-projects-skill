function errorHandler(err, _req, res, _next) {
    const statusCode = err.statusCode || 500;
    const message = statusCode === 500 ? 'Internal Server Error' : err.message;
    res.status(statusCode).send(message);
}

module.exports = errorHandler;
