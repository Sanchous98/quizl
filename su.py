import click
import main
from db.repositories import User
from db.schemas import UserCreate
from dependencies import database


@click.command()
@click.option('--firstname', '-f')
@click.option('--lastname', '-l')
@click.option('--username', '-u')
@click.option('--email', '-e')
@click.option('--password', '-p')
@click.option('--is_active', '-a')
@click.option('--is_super', '-s')
def main(firstname: str, lastname: str, username: str, email: str, password: str, is_active: bool, is_super: bool):
    user_repo = User(next(database()))
    user_schema = UserCreate(firstname=firstname, lastname=lastname, email=email, username=username, password=password,
                             is_active=is_active, is_super=is_super)
    user_repo.create(user_schema)


if __name__ == '__main__':
    main()
