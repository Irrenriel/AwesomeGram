from sys import argv

from pydantic import BaseSettings


class Config(BaseSettings):
    # == Development == #
    # Debug Mode:
    debug: bool = "--debug" in argv

    # Variables to connect:
    # Aiogram Bot
    BOT_TOKEN: str = '1543643507:AAENsC1_-yISvqi2mdBzIMoMTPEXwsgVyEk' if debug else \
        '1291992166:AAEQiPPG0S6Lf3Fl-FU3Jgc3U07SYevm14Y'
    PARSE_MODE: str = 'HTML'

    # Databases
    USER = 'linnotir'  # 'postgres'
    BRIEF_USER = 'brief'
    PASSWORD = '29otelep'  # 'ql123456lp'
    DATABASE = 'owlfesya_db'  # 'FesyaDatabase'
    HOST = '45.143.139.64'  # '127.0.0.1'

    POSTGRES_DB = ('main', USER, PASSWORD, DATABASE, HOST)
    BRIEF_DB = ('main', BRIEF_USER, PASSWORD, DATABASE, HOST)

    # Telethon
    SESSION_NAME = 'OwlFesya_session_test' if debug else 'OwlFesya_session_work'
    BRIEF_SESSION_NAME = 'Brief_session_test' if debug else 'Brief_session_work'
    API_ID = 1209411
    API_HASH = '32583db8454ca7feb52a4a5d48289519'

    TELETHON_VARS = (SESSION_NAME, API_ID, API_HASH)
    BRIEF_TELETHON_VARS = (BRIEF_SESSION_NAME, API_ID, API_HASH)

    # Other variables:
    # Roles
    ADMINS_IDS: list = [560877161, 394557686]
    WORKBENCH_MEMBERS_IDS = []

    # Global constants:
    APP_VERSION = "1.0"
    CW_BOT_ID = 408101137
    KIND_SPY_CHANNEL = -1001372385475
    CHAT_WARS_DIGEST = -1001108112459
    MY_TESTING_CHANNEL = 1150780350


config = Config()
