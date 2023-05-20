from src.model.User import User


class UserRepository:

    @staticmethod
    def save(id, name, username):
        print(name)
        User.create(id=id, name=name, username=username)

    @staticmethod
    def update(user):
        user.save()

    @staticmethod
    def remove(id):
        user = User.get(User.id == id)
        user.delete_instance()

    @staticmethod
    def get(id):
        return User.get_or_none(User.id == id)

