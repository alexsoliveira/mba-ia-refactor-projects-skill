class AdminController {
    constructor(reportService) {
        this.reportService = reportService;
    }

    getFinancialReport() {
        return this.reportService.buildFinancialReport();
    }
}

module.exports = AdminController;
