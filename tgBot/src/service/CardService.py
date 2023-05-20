from src.error.errors import NoRegisteredCardError
from src.repository.CardRepository import CardRepository
from src.repository.UserRepository import UserRepository
from src.service.AccountService import AccountService
from src.util.Util import Util


class CardService:
    @staticmethod
    def register_card(user_id):
        password = Util.generate_random_number(4)
        CardRepository.save(password=password, user_id=user_id)
        if not AccountService.check_account_in_db(user_id):
            AccountService.register_account(user_id)
        return password

    @staticmethod
    def authorization(user_id, password):
        if CardRepository.get_by_owner(user_id=user_id) is not None:
            if password == CardRepository.get_by_owner(user_id=user_id).password:
                user = UserRepository.get(user_id)
                user.is_authorized = True
                UserRepository.update(user)
        else:
            raise NoRegisteredCardError

    @staticmethod
    def exit(user_id):
        user = UserRepository.get(user_id)
        user.is_authorized = False
        UserRepository.update(user)
