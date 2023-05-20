import peewee
import sqlite3
import psycopg2

from src.util.DatabaseConnection import DatabaseConnection


class User(peewee.Model):
    class Meta:
        database = DatabaseConnection().db
        table_name = 'users'

    id = peewee.IntegerField(column_name='id', unique=True, null=False)
    name = peewee.TextField(column_name='name', null=False)
    username = peewee.TextField(column_name='username', null=True)
    is_authorized = peewee.BooleanField(column_name='is_authorized', default=False)
