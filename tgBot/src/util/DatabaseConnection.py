import peewee
from jproperties import Properties



class DatabaseConnection:
    _instance = None

    @staticmethod
    def get_properties():
        configs = Properties()
        with open('src/resources/application.properties', 'rb') as config_file:
            configs.load(config_file)
        return configs

    __config = {
        'user'    : get_properties().get("user").data,
        'password': get_properties().get("password").data,
        'host'    : get_properties().get("host").data,
        'port'    : get_properties().get("port").data,
        'database': get_properties().get("database").data
    }

    def __new__(cls):
        print(1)
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db = peewee.PostgresqlDatabase(**cls.__config)
        return cls._instance