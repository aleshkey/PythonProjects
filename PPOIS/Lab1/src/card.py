import psycopg2 as psycopg2
from jproperties import Properties
from psycopg2 import OperationalError


class Card:
    def __init__(self, card_id, date_of_issue, cvv) -> None:
        super().__init__()
        self.card_id = card_id
        self.date_of_issue = date_of_issue
        self.cvv = cvv

    def execute_read_query(self, connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except OperationalError as e:
            print(f"The error '{e}' occurred")

    def get_balance(self, connection):
        return self.execute_read_query(connection, f"SELECT * FROM bank_bd WHERE card_id={self.card_id}")[0][1]

    def get_owner(self, connection):
        owner_id = self.execute_read_query(connection, f"SELECT * FROM bank_bd WHERE card_id={self.card_id}")[0][3]
        info_about_person = self.execute_read_query(connection, f"SELECT * FROM user_bd WHERE user_id={owner_id}")
        return info_about_person[0][1]+info_about_person[0][2]

    