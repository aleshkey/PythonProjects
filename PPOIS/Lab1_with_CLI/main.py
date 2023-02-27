import click
from src.cash_machine import CashMachine

cash_machine = CashMachine()


@click.group()
def cli():
    pass


@click.command()
@click.option('--password', help='password of your card.')
@click.argument('password')
def authorization(password):
    cash_machine.authorization(password)


@click.command()
@click.argument('money', nargs=1)
@click.argument('password', nargs=1)
def add_money(money, password):
    cash_machine.add_money(cash_machine.get_card_id_now(), float(money), password)


@click.command()
def exit():
    cash_machine.exit()


@click.command()
@click.argument('money', nargs=1)
@click.argument('password', nargs=1)
def withdraw_money(money, password):
    cash_machine.withdraw_money(cash_machine.get_card_id_now(), float(money), password)


@click.command()
@click.argument('money', nargs=1)
@click.argument('card_id', nargs=1)
@click.argument('password', nargs=1)
def transfer_money(money, card_id, password):
    cash_machine.transfer(cash_machine.get_card_id_now(), card_id, money, password)


@click.command()
@click.argument('password', nargs=1)
def get_balance(password):
    print(cash_machine.get_balance(password))


@click.command()
@click.argument('money', nargs=1)
@click.argument('phone_number', nargs=1)
@click.argument('password', nargs=1)
def transfer_to_phone_number(money, phone_number, password):
    cash_machine.transfer_to_phone_number(phone_number, money, password)


@click.command()
@click.argument('name', nargs=1)
@click.argument('surname, nargs=1')
def register_new_card(name, surname):
    cash_machine.registration(name, surname)


cli.add_command(authorization)
cli.add_command(add_money)
cli.add_command(exit)
cli.add_command(withdraw_money)
cli.add_command(transfer_money)
cli.add_command(get_balance)
cli.add_command(transfer_to_phone_number)
cli.add_command(register_new_card)


if __name__ == '__main__':
    cli()
