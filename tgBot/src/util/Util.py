import random

from src.model.BankAccount import BankAccount
from src.model.Card import Card
from src.model.User import User
from jproperties import Properties


class Util:
    @staticmethod
    def create_tables():
        User.create_table()
        Card.create_table()
        BankAccount.create_table()

    @staticmethod
    def get_properties():
        configs = Properties()
        with open('src/resources/application.properties', 'rb') as config_file:
            configs.load(config_file)
        return configs

    @staticmethod
    def generate_random_number(size):
        rnd = ""
        for i in range(size):
            rnd = rnd + str(random.randint(0, 9))
        return rnd
