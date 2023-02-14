import psycopg2
from jproperties import Properties
from psycopg2 import OperationalError

from src.card import Card
from src.user import User


class CashMachine:
    def __init__(self):
        configs = Properties()
        with open('D:\python\practice\pythonProject\PPOIS\Lab1\properties\Application.properties', 'rb') as config_file:
            configs.load(config_file)
        сonnection = None
        try:
            self.connection = psycopg2.connect(
                database=configs.get("name").data,
                user=configs.get("user").data,
                password=configs.get("password").data,
                host=configs.get("host").data,
                port=configs.get("port").data,
            )
        except OperationalError as e:
            print(e)
        self.cursor = self.connection.cursor()
        self.kod = -1
        self.balance = self.execute_read_query(self.connection, "SELECT * FROM cash_machine")[0][0]
        self.admin_login = self.execute_read_query(self.connection, "SELECT * FROM cash_machine")[0][1]
        self.admin_password = self.execute_read_query(self.connection, "SELECT * FROM cash_machine")[0][2]
        self.get_cards()
        self.get_users()

    def get_cards(self):
        cards_in_db = self.execute_read_query(self.connection, "SELECT * FROM card_bd")
        self.cards = []
        for card in cards_in_db:
            self.cards.append(Card(card[0], card[1], card[2]))

    def get_users(self):
        users_in_db = self.execute_read_query(self.connection, "SELECT * FROM user_bd")
        self.users = []
        for user in users_in_db:
            self.users.append(User(user[0], user[1], user[2]))

    def execute_read_query(self, query):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except OperationalError as e:
            print(f"The error '{e}' occurred")

    def work(self):
        self.authorization()
        while self.kod != 0:
            self.print_menu()

    def print_menu(self):
        if (self.authorization()):
            while (self.kod != 0):
                self.kod = input(
                                 "0 - exit\n"
                                 "1 - check balance\n"
                                 "2 - transfer to the card\n"
                                 "3 - transfer to the phone number\n"
                                 "4 - withdraw money\n"
                                 "5 - register new card\n"
                                )
                self.choose_operation()
            self.cursor.close()
            self.connection.close()


    def authorization(self):
        counter = 0
        while (counter < 3):
            password = input("enter password\n")
            card_in_db = self.execute_read_query("SELECT * FROM bank_bd WHERE password=" + password)
            if (len(card_in_db) != 0):
                self.get_index_of_card_now(card_in_db)
                return True
            counter += 1
        return False

    def get_index_of_card_now(self, card_in_db):
        for i in range(len(self.cards)):
            if self.cards[i].card_id == card_in_db[0][0]:
                self.index_of_card_now = i

    def exist_account_in_db(self, card_id):
        card_in_db = self.get_bank_info_in_db_by_card_id(card_id)
        if (len(card_in_db) != 0):
            return True
        return False

    def get_bank_info_in_db_by_card_id(self, card_id):
        return self.execute_read_query("SELECT * FROM bank_bd WHERE card_id = " + card_id)

    def choose_operation(self):
        if self.kod == 1:
            print(self.card_now.get_balance(self.connection))
        elif self.kod == 2:  # second operation is ready
            money_to_transfer = input("enter money to transfer")
            card_id_to_transfer = input("enter card id")
            while (not self.exist_account_in_db(card_id_to_transfer)):
                print("there is no such card id")
                card_id_to_transfer = input("enter card id")

            bank_info = self.get_bank_info_in_db_by_card_id(self.cards[self.index_of_card_now].card_id)
            bank_info[0][1] -= money_to_transfer
            self.save_to_bank(bank_info)
            bank_info_about_card = self.cursor.execute("select * from bank_bd")

            for info in bank_info_about_card:
                if info[0] == card_id_to_transfer:
                    info[1] += money_to_transfer
                    self.save_to_bank(info)

    def save_to_bank(self, bank_info):
        if self.exist_account_in_db(bank_info[0]):
            self.cursor.execute("UPDATE bank_db SET balance = %s WHERE card_id = " + bank_info[0], (bank_info[1]))


