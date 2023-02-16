import unittest
import cash_machine

import psycopg2
from jproperties import Properties
from psycopg2 import OperationalError


class MyTestCase(unittest.TestCase):

    def get_connection(self):
        configs = Properties()
        with open('D:\python\practice\pythonProject\PPOIS\Lab1\properties\Application.properties', 'rb') as config_file:
            configs.load(config_file)

        self.сonnection = None
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

    def execute_read_query(self, query):
        self.cursor = self.connection.cursor()
        result = None
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except OperationalError as e:
            print(f"The error '{e}' occurred")

    def test_add_money(self):
        self.get_connection()
        machine = cash_machine.CashMachine()
        info_in_bank_start = self.execute_read_query("select * from bank_bd where card_id = 1")
        machine.add_money(1, 50)
        info_in_bank_finish = self.execute_read_query("select * from bank_bd where card_id = 1")
        assert info_in_bank_finish[0][1] - info_in_bank_start[0][1] == 50

    def test_withdraw_money(self):
        self.get_connection()
        machine = cash_machine.CashMachine()
        info_in_bank_start = self.execute_read_query("select * from bank_bd where card_id = 1")
        machine.withdraw_money(1, 50)
        info_in_bank_finish = self.execute_read_query("select * from bank_bd where card_id = 1")
        assert info_in_bank_start[0][1] - info_in_bank_finish[0][1] == 50


    def test_exist_account_in_db_true(self):
        self.get_connection()
        machine = cash_machine.CashMachine()
        flag = machine.exist_account_in_db(1)
        assert flag == True

    def test_exist_account_in_db_false(self):
        self.get_connection()
        machine = cash_machine.CashMachine()
        flag = machine.exist_account_in_db(255)
        assert flag == False

    def test_exist_in_users_true(self):
        self.get_connection()
        machine = cash_machine.CashMachine()
        flag = machine.exist_in_users("Alexey", "Oleshkevich")
        assert flag == True

    def test_exist_in_users_false(self):
        self.get_connection()
        machine = cash_machine.CashMachine()
        flag = machine.exist_in_users("Al", "Ole")
        assert flag == False

    def test_save_to_bank_update(self):
        self.get_connection()
        machine = cash_machine.CashMachine()
        balance = machine.cards[0].get_balance(self.connection)
        machine.save_to_bank((1, 40000000, 1))
        card_info = self.execute_read_query("Select * from bank_bd where card_id = 1")
        assert card_info[0][1] == 40000000
        machine.save_to_bank((1, balance, 1))



if __name__ == '__main__':
    unittest.main()
