import peewee
import sqlite3
import psycopg2

from src.model.User import User
from src.util.DatabaseConnection import DatabaseConnection


class Card (peewee.Model):
    class Meta:
        database = DatabaseConnection().db
        table_name = 'cards'

    id = peewee.AutoField(column_name='id')
    password = peewee.TextField(column_name='password', null=False)
    user = peewee.ForeignKeyField(User, related_name='cards', on_delete='cascade')

