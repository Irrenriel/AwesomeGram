# Development:
# Switch develop instances by this vars
TestMode: bool = True
LoggingMode: bool = False

# Variables to connect:
# Aiogram Bot
BOT_TOKEN: str = 'bot_token'
PARSE_MODE: str = 'HTML'

# Databases
# !!! Please keep your database files in the config/ folder !!!
# You can create multiple paths and instantiate with them
# To use SQLite3 database
SQLITE_DB_PATH: str = 'config/Example.db'

# To use PostgreSQL database
POSTGRES_DB = ('your_own_session_name', 'user', 'password', 'database', 'host')  # Input data

# Other variables:
# Roles
ADMINS_ID: list[int] = []

# Global constants:
# To import it anywhere or use it to instantiate it into resources / models
