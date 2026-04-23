class UserController {
    constructor(userModel) {
        this.userModel = userModel;
    }

    async deleteUser(userId) {
        await this.userModel.deleteById(userId);
        return 'Usuario deletado, mas as matriculas e pagamentos ficaram sujos no banco.';
    }
}

module.exports = UserController;
