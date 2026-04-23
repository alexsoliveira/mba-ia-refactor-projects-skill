const { settings } = require('./config/settings');
const CacheService = require('./services/cacheService');
const { hashPassword } = require('./services/authService');

const cacheService = new CacheService();

function logAndCache(key, data) {
    console.log(`[LOG] Salvando no cache: ${key}`);
    cacheService.save(key, data);
}

function secureCrypto(password) {
    return hashPassword(password);
}

module.exports = {
    config: settings,
    logAndCache,
    secureCrypto,
    cacheService
};
