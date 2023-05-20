from src.model.BankAccount import BankAccount


class AccountRepository:

    @staticmethod
    def save(user_id):
        BankAccount.create(user=user_id)

    @staticmethod
    def remove(user_id):
        account = BankAccount.get(user=user_id)
        account.delete_instance()

    @staticmethod
    def update(account):
        account.save()

    @staticmethod
    def get_by_owner(user_id):
        return BankAccount.get_or_none(BankAccount.user == user_id)
