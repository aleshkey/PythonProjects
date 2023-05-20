from src.error.errors import *
from src.repository.AccountRepository import AccountRepository
from src.repository.UserRepository import UserRepository
from src.service.UserService import UserService


class AccountService:

    @staticmethod
    def check_account_in_db(id):
        user = AccountRepository.get_by_owner(id)
        return user is not None

    @staticmethod
    def get_balance(user_id):
        if UserService.is_authorized(user_id):
            return AccountRepository.get_by_owner(user_id=user_id).balance
        else:
            raise AuthorizationError

    @staticmethod
    def register_account(user_id):
        AccountRepository.save(user_id=user_id)

    @staticmethod
    def change_balance(user_id, money, sign):
        if money.isdigit():
            if UserService.is_authorized(user_id):
                account = AccountRepository.get_by_owner(user_id)
                if sign == "+":
                    account.balance = account.balance + float(money)
                if sign == "-":
                    account.balance = account.balance - float(money)
                    if account.balance < 0:
                        raise NotEnoughMoneyError
                AccountRepository.update(account)
            else:
                raise AuthorizationError
        else:
            raise NotNumberError
