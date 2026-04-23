class CacheService {
    constructor() {
        this.cache = new Map();
    }

    save(key, value) {
        this.cache.set(key, value);
    }

    get(key) {
        return this.cache.get(key);
    }
}

module.exports = CacheService;
