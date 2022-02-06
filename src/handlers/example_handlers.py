from aiogram import Dispatcher

from resources.tools.cfilters import Command, IsUser
from resources.tools.states import ExampleState
from src.functions import test


async def register_example_handlers(dp: Dispatcher):
    # You should code handlers in such format
    dp.register_message_handler(
        test,  # Function in the first row
        Command('test'), IsUser(is_admin=False),  # Filters in the next rows
        state=None  # The last 2 rows is optional, adding state filter and comments
        # State: None -> ExampleState.First (by if)
    )

    dp.register_message_handler(
        test,  # Function in the first row
        Command('test'), IsUser(is_admin=False),  # Filters in the next rows
        state=ExampleState.First  # The last 2 rows is optional, adding state filter and comments
        # State: ExampleState.First -> None (by if)
    )

    # That`s all what you need to know about handlers!
