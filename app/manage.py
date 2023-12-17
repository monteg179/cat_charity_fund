import asyncio
from argparse import ArgumentParser

import uvicorn

from app.core.init_db import create_user


class Parsing:

    CREATE_SUPER_USER = 'createsuperuser'
    RUN_SERVER = 'runserver'

    DEFAULT_PORT = 8000

    def __init__(self) -> None:
        self.__parser = ArgumentParser(
            description='<Описание>',
            exit_on_error=False
        )
        commands = self.__parser.add_subparsers(
            dest='command',
        )
        create_superuser_parser = commands.add_parser(
            name=Parsing.CREATE_SUPER_USER,
            help='создание суперпользователя'
        )
        create_superuser_parser.add_argument(
            '--email',
            required=True,
            help='email пользователя'
        )
        create_superuser_parser.add_argument(
            '--password',
            required=True,
            help='пароль пользователя'
        )
        run_server_parser = commands.add_parser(
            name=Parsing.RUN_SERVER,
            help='запуск сервера'
        )
        run_server_parser.add_argument(
            '--port',
            type=int,
            default=Parsing.DEFAULT_PORT,
            help='порт сервера'
        )

    def __call__(self, *args, **kwargs) -> None:
        self.__args = self.__parser.parse_args()
        if self.__args.command == Parsing.CREATE_SUPER_USER:
            self.create_superuser()
        elif self.__args.command == Parsing.RUN_SERVER:
            self.run_server()
        else:
            self.__parser.print_usage()

    def create_superuser(self) -> None:
        asyncio.run(
            create_user(
                email=self.__args.email,
                password=self.__args.password,
                is_superuser=True
            )
        )

    def run_server(self) -> None:
        uvicorn.run('app.main:app', reload=True)


def main():
    try:
        parsing = Parsing()
        parsing()
    except Exception as error:
        print(f'error: {type(error)} = {error}')


if __name__ == '__main__':
    main()
