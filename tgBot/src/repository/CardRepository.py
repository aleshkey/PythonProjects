from src.model.Card import Card


class CardRepository:

    @staticmethod
    def save(password, user_id):
        Card.create(user=user_id, password=password)

    @staticmethod
    def remove(password, user_id):
        card = Card.get(Card.password == password, Card.user == user_id)
        card.delete_instance()

    @staticmethod
    def get_by_owner(user_id):
        return Card.get_or_none(Card.user == user_id)
