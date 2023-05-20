import peewee
import sqlite3
import psycopg2

from src.model.User import User
from src.util.DatabaseConnection import DatabaseConnection


class BankAccount (peewee.Model):
    class Meta:
        database = DatabaseConnection().db
        table_name = 'bank_accounts'

    id = peewee.AutoField(column_name='id')
    balance = peewee.FloatField(column_name='balance', default=0)
    user = peewee.ForeignKeyField(User, related_name='accounts', on_delete='cascade', unique=True)
