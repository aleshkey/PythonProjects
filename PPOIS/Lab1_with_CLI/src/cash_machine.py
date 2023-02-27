import datetime
import random
from sqlite3 import OperationalError

from jproperties import Properties
import psycopg2 as psycopg2
from _decimal import Decimal


class CashMachine:

    def __init__(self):
        configs = Properties()
        with open('D:\python\practice\pythonProject\PPOIS\Lab1_with_CLI\properties\Application.properties',
                  'rb') as config_file:
            configs.load(config_file)
        self.connection = None
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
        self.is_authorized = self.execute_read_query("select * from info_of_client_now")[0][0]

    def execute_read_query(self, query):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except OperationalError as e:
            print(f"The error '{e}' occurred")

    def authorization(self, password):
        if not self.is_authorized:
            card_in_db = self.execute_read_query(f"SELECT * FROM bank_bd WHERE password='{password}'")
            if len(card_in_db) != 0:
                self.cursor.execute(
                    f"update info_of_client_now set is_authorized = true, id_of_card_now = {card_in_db[0][0]} ")
                self.connection.commit()
        else:
            print("you have already authorized")

    def same_password(self, password):
        card_id_now = self.execute_read_query("select * from info_of_client_now ")[0][1]
        right_password = self.execute_read_query(f"select * from bank_bd where card_id = {card_id_now}")[0][2]
        if right_password == password:
            return True
        else:
            return False

    def get_card_id_now(self):
        return self.execute_read_query("select * from info_of_client_now ")[0][1]

    def add_money(self, card_id, money, password):
        if self.same_password(password):
            bank_info_about_card = self.execute_read_query("select * from bank_bd")
            for info in bank_info_about_card:
                if info[0] == int(card_id):
                    buf_tuple = (info[0], Decimal(info[1]) + Decimal(money), info[2], info[3])
                    info = buf_tuple
                    self.save_to_bank(info)

    def save_to_bank(self, bank_info):
        if self.exist_account_in_db(bank_info[0]):
            self.cursor.execute(f"UPDATE bank_bd SET balance = {bank_info[1]} WHERE card_id = {bank_info[0]}")
        else:
            self.cursor.execute(
                f"insert into bank_bd (balance, password, owner_id) values ({bank_info[0]}, '{bank_info[1]}', {bank_info[2]})")
        self.connection.commit()

    def exist_account_in_db(self, card_id):
        card_in_db = self.get_bank_info_in_db_by_card_id(card_id)
        if len(card_in_db) != 0:
            return True
        return False

    def get_bank_info_in_db_by_card_id(self, card_id):
        return self.execute_read_query("SELECT * FROM bank_bd WHERE card_id = " + str(card_id))

    def withdraw_money(self, card_id, money, password):
        if self.same_password(password):
            bank_info = self.get_bank_info_in_db_by_card_id(self.get_card_id_now())
            buf_tuple = (bank_info[0][0], Decimal(bank_info[0][1]) - Decimal(money), bank_info[0][2], bank_info[0][3])
            self.save_to_bank(buf_tuple)

    def exist_in_users(self, name, surname):
        if len(self.execute_read_query(f"select * from user_bd where name='{name}' and surname='{surname}'")) != 0:
            return True
        else:
            return False

    def transfer(self, card_id_from, card_id_to, money, password):
        if self.same_password(password):
            self.add_money(card_id_to, money, password)
            self.withdraw_money(card_id_from, money, password)

    def get_balance(self, password):
        if self.same_password(password):
            balance = self.execute_read_query(f"select * from bank_bd where card_id = {self.get_card_id_now()}")[0][1]
            return balance

    def exit(self):
        self.cursor.execute(f"update info_of_client_now set is_authorized = false, id_of_card_now = null where id = 1")
        self.connection.commit()

    def transfer_to_phone_number(self, phone_number, money,  password):
        self.withdraw_money(self.get_card_id_now(), money, password)

    def get_random_number(self, r):
        password = ""
        for i in range(r):
            digit = random.randrange(9)
            password += str(digit)
        return password

    def registration(self, name, surname):
        name = input("enter your name\n")
        surname = input("enter your surname\n")
        if not self.exist_in_users(name, surname):
            self.cursor.execute(f"insert into user_bd (name, surname) values ('{name}', '{surname}')")
        password = self.get_random_number(4)
        print(f"password: {password}")
        person_id = self.execute_read_query(f"select * from user_bd where name = {name} and surname = {surname}")[0][0]
        bank_info = (0, password, person_id)
        self.save_to_bank(bank_info)
        cvv = self.get_random_number(3)
        print(f"cvv: {cvv}")
        date_issue = str(datetime.date.day) + str(datetime.date.month) + str(datetime.date.year + 5)
        card = (self.execute_read_query(f"select * from bank_bd where password='{password}'")[0][0], cvv)
        self.cursor.execute(f"insert into card_bd (card_id, date_issue, cvv)"
                            f"             values ('{card[0]}', '{date_issue}','{card[1]}')")
        self.connection.commit()
