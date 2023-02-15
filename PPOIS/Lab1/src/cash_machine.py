import random
from decimal import Decimal

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
        self.index_of_card_now = -1
        self.get_cards()
        self.get_users()
        machine = self.execute_read_query("SELECT * FROM cash_machine_db")
        self.balance = machine[0][0]
        self.admin_login = machine[0][1]
        self.admin_password = machine[0][2]

    def get_cards(self):
        cards_in_db = self.execute_read_query("SELECT * FROM card_bd")
        self.cards = []
        for card in cards_in_db:
            self.cards.append(Card(card[0], card[1], card[2]))

    def get_users(self):
        users_in_db = self.execute_read_query("SELECT * FROM user_bd")
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
        self.print_menu()

    def print_menu(self):
        if (self.authorization()):
            while (self.kod != '0'):
                self.kod = input(
                                 "0 - exit\n"
                                 "1 - check balance\n"
                                 "2 - transfer to the card\n"
                                 "3 - transfer to the phone number\n"
                                 "4 - withdraw money\n"
                                 "5 - add money\n"
                                 "6 - register new card\n"
                                )
                self.choose_operation()
            self.cursor.close()
            self.connection.close()


    def authorization(self):
        counter = 0
        while (counter < 3):
            password = input("enter password\n")
            card_in_db = self.execute_read_query("SELECT * FROM bank_bd WHERE password='" + password+"'")
            if (len(card_in_db) != 0):
                self.set_index_of_card_now(card_in_db)
                return True
            counter += 1
        return False

    def set_index_of_card_now(self, card_in_db):
        for i in range(len(self.cards)):
            if self.cards[i].card_id == card_in_db[0][0]:
                self.index_of_card_now = i

    def exist_account_in_db(self, card_id):
        card_in_db = self.get_bank_info_in_db_by_card_id(card_id)
        if (len(card_in_db) != 0):
            return True
        return False

    def get_bank_info_in_db_by_card_id(self, card_id):
        return self.execute_read_query("SELECT * FROM bank_bd WHERE card_id = " + str(card_id))

    def choose_operation(self):
        if self.kod == '1':
            print(self.cards[self.index_of_card_now].get_balance(self.connection))
        elif self.kod == '2':  # second operation is ready
            money_to_transfer = input("enter money to transfer\n")
            card_id_to_transfer = input("enter card id\n")
            while (not self.exist_account_in_db(card_id_to_transfer)):
                print("there is no such card id")
                card_id_to_transfer = input("enter card id\n")

            self.withdraw_money(self.cards[self.index_of_card_now].card_id, money_to_transfer)
            self.add_money(card_id_to_transfer, money_to_transfer)
        elif self.kod == '3':
            money_to_transfer = input("enter money to transfer")
            phone_number_to_transfer = input("enter phone number\n")
            self.withdraw_money(self.cards[self.index_of_card_now].card_id, money_to_transfer)
        elif self.kod == '4':
            money_to_transfer = input("enter money to transfer\n")
            self.withdraw_money(self.cards[self.index_of_card_now].card_id, money_to_transfer)
        elif self.kod == '5':
            money_to_add = input("enter money to add\n")
            self.add_money(self.cards[self.index_of_card_now].card_id, money_to_add)
        elif self.kod == '6':
            self.registration()

    def save_to_bank(self, bank_info):
        if self.exist_account_in_db(bank_info[0]):
            self.cursor.execute(f"UPDATE bank_bd SET balance = {bank_info[1]} WHERE card_id = {bank_info[0]}")
        else:
            self.cursor.execute(f"insert into bank_bd (balance, password, owner_id) values ({bank_info[0]}, '{bank_info[1]}', {bank_info[2]})")
        self.connection.commit()

    def withdraw_money(self, card_id, money):
        bank_info = self.get_bank_info_in_db_by_card_id(self.cards[self.index_of_card_now].card_id)
        buf_tuple = (bank_info[0][0], Decimal(bank_info[0][1]) - Decimal(money), bank_info[0][2], bank_info[0][3])
        self.save_to_bank(buf_tuple)

    def add_money(self, card_id, money):
        bank_info_about_card = self.execute_read_query("select * from bank_bd")

        for info in bank_info_about_card:
            if info[0] == int(card_id):
                buf_tuple = (info[0], Decimal(info[1]) + Decimal(money), info[2], info[3])
                info = buf_tuple
                self.save_to_bank(info)

    def exist_in_users(self, name, surname):
        if (len(self.execute_read_query(f"select * from user_bd where name='{name}' and surname='{surname}'")) != 0):
            return True
        else:
            return False


    def registration(self):
        name = input("enter your name\n")
        surname = input("enter your surname\n")
        if (not self.exist_in_users(name, surname)):
            self.cursor.execute(f"insert into user_bd (name, surname) values ('{name}', '{surname}')")
        password = self.get_random_number(4)
        print(f"password: {password}")
        self.get_users()
        bank_info = (0, password, self.users[len(self.users)-1].id)
        self.save_to_bank(bank_info)
        cvv = self.get_random_number(3)
        print(f"cvv: {cvv}")
        card = (self.execute_read_query(f"select * from bank_bd where password='{password}'")[0][0], cvv)
        self.cursor.execute(f"insert into card_bd (card_id, cvv) values ('{card[0]}', '{card[1]}')")
        self.connection.commit()


    def get_random_number(self, r):
        password = ""
        for i in range(r):
            digit = random.randrange(9)
            password += str(digit)
        return password
