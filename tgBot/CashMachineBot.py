import telebot

from src.error.errors import *
from src.service.AccountService import AccountService
from src.service.CardService import CardService
from src.service.UserService import UserService
from src.util.Util import Util

Util.create_tables()

bot = telebot.TeleBot(Util.get_properties().get("token").data)


@bot.message_handler(commands=['start'], content_types=['text'])
def start(message):
    print(message.from_user.id)
    if UserService.check_user_in_db(message.from_user.id):
        bot.send_message(message.from_user.id, "You have already registered")
    else:
        UserService.register_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
        bot.send_message(message.from_user.id, f"Hello, {message.from_user.first_name}")


@bot.message_handler(commands=['remove'], content_types=['text'])
def remove(message):
    if not UserService.check_user_in_db(message.from_user.id):
        bot.send_message(message.from_user.id, "You have already deleted this bot")
    else:
        UserService.remove_user(message.from_user.id)
        bot.send_message(message.from_user.id, f"Goodbye, {message.from_user.first_name}")


@bot.message_handler(commands=['register_new_card'], content_types=['text'])
def register_new_card(message):
    password = CardService.register_card(message.from_user.id)
    bot.send_message(message.from_user.id, f"password: {password}")


@bot.message_handler(commands=['authorization'], content_types=['text'])
def authorization(message):
    bot.send_message(message.from_user.id, "Enter password: ")
    bot.register_next_step_handler(message, check_password)


def check_password(message):
    try:
        CardService.authorization(message.from_user.id, message.text)
        if UserService.get_user(message.from_user.id).is_authorized:
            bot.send_message(message.from_user.id, "Logged in")
        else:
            bot.send_message(message.from_user.id, "Incorrect password")
    except NoRegisteredCardError:
        bot.send_message(message.from_user.id, "First register the card")


@bot.message_handler(commands=['exit'], content_types=['text'])
def exit(message):
    CardService.exit(message.from_user.id)
    bot.send_message(message.from_user.id, "Logged out")


@bot.message_handler(commands=['add_money', 'withdraw_money'], content_types=['text'])
def request_to_change_balance(message):
    global command
    command = message.text
    bot.send_message(message.from_user.id, "Enter the amount:")
    bot.register_next_step_handler(message, change_balance)


def change_balance(message):
    try:
        sign = ""
        if command == "/add_money":
            sign = "+"
        else:
            sign = "-"
        AccountService.change_balance(message.from_user.id, message.text, sign)
        bot.send_message(message.from_user.id, "Completed!")
    except AuthorizationError:
        bot.send_message(message.from_user.id, "You haven't logged in")
    except NotNumberError:
        bot.send_message(message.from_user.id, "It's not a number")
    except NotEnoughMoneyError:
        bot.send_message(message.from_user.id, "Not enough money")


@bot.message_handler(commands=['get_balance'], content_types=['text'])
def get_balance(message):
    try:
        bot.send_message(message.from_user.id, str(AccountService.get_balance(message.from_user.id)))
    except AuthorizationError:
        bot.send_message(message.from_user.id, "You haven't logged in")


@bot.message_handler(commands=['help'], content_types=['text'])
def help(message):
    help_message = "Привет! Я бот, который может помочь тебе управлять своим банковским счетом. Вот список доступных команд: \n " \
                   "/authorization: авторизация пользователя в системе (ввод пароля);\n" \
                   "/register_new_card: регистрация новой банковской карты;\n" \
                   "/get_balance: просмотр баланса на счете;\n" \
                   "/add_money: пополнение баланса на счете;\n" \
                   "/withdraw_money: снятие денег со счета;\n" \
                   "/remove: удаление личных данных;\n" \
                   "/exit: деавторизация."
    bot.send_message(message.from_user.id, help_message)


bot.polling(none_stop=True, interval=1)
