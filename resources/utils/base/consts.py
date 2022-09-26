MODULE_HANDLER_CONTENT = '''\
{header}from aiogram import Dispatcher

from modules.{name}.functions import {name}_func


async def register_{name}_handlers(dp: Dispatcher):
    """
    For comfortable writing handlers, you should follow the format:
    
    1) The first line in the handler is the function to run
    2) The following lines in the handler are the initialization of filters
    3) The last two lines in the handler are an indication of the state and its variability
    
    ↓       ↓       ↓       ↓       ↓

    from aiogram.dispatcher.filters import Command, ChatTypeFilter
    from aiogram.types import ChatType

    dp.register_..._handler(
        trigger_func, ← the function to run
        Command('start'), ChatTypeFilter(ChatType.PRIVATE), ← the initialization of filters
        state='*' ← an indication of the state
        # State: '*' -> StateOn.Example (by if) ← and state variability
    )

    """
    dp.register_message_handler(
        {name}_func
    )

'''