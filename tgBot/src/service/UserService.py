from src.repository.UserRepository import UserRepository


class UserService:

    @staticmethod
    def check_user_in_db(id):
        user = UserRepository.get(id)
        return user is not None

    @staticmethod
    def get_user(id):
        return UserRepository.get(id)

    @staticmethod
    def register_user(id, name, surname):
        UserRepository.save(id, name, surname)

    @staticmethod
    def remove_user(id):
        UserRepository.remove(id)

    @staticmethod
    def is_authorized(user_id):
        return UserRepository.get(user_id).is_authorized
