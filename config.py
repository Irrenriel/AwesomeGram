from sys import argv

from pydantic import BaseSettings


class Config(BaseSettings):
    # == Development == #
    # Debug Mode:
    debug: bool = "--debug" in argv

    # Creating a module for Linux with the header LINUX_HEADER if True:
    LINUX_MODE = False
    LINUX_HEADER = '# -*- coding: utf-8 -*-'

    # Variables to connect:
    # Aiogram Bot
    BOT_TOKEN: str = 'BOT TOKEN'
    PARSE_MODE: str = 'HTML'

    # Databases
    # To use PostgreSQL database
    # USER: str = 'USER'
    # PASSWORD: str = 'PASSWORD'
    # DATABASE: str = 'DB NAME'
    # HOST: str = 'IP HOST'
    #
    # POSTGRES_DB = ('main', USER, PASSWORD, DATABASE, HOST)

    # To use SQLite3 database
    # SQLITE_DB_PATH: str = 'resources/Example.db'

    # Telethon
    # To Use Telethon
    # SESSION_NAME: str = 'SESSION_NAME_test' if debug else 'SESSION_NAME_work'  # Example how to user debug mode
    # API_ID: int = 1111111
    # API_HASH: str = 'API_HASH'
    #
    # TELETHON_VARS = (SESSION_NAME, API_ID, API_HASH)

    # Other variables:
    # Roles
    ADMINS_ID: list[int] = []

    # Global constants:
    CURRENT_VERSION = "0.0"


config = Config()
