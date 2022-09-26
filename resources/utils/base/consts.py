MODULE_HANDLERS_CONTENT = '''\
{header}\
from aiogram import Dispatcher

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

MODULE_STATES_CONTENT = '''\
{header}\
from aiogram.dispatcher.filters.state import StatesGroup, State


class {title}States(StatesGroup):
    First = State()
'''

MODULES_HANDLERS_CONTENT = '''\
{header}\
import logging

from aiogram import Dispatcher

{rows}


async def register_handlers(dp: Dispatcher):
    logging.info('▻ Installing a handlers...')
    
{handlers}
'''

HANDLERS_PATTERN = '''\
    await register_{name}_handlers(dp)
    logging.info('▻ {upper} handlers was successful installed!')
'''

IMPORT_CONTENT = '''\
{header}\
{rows}
'''

MODULE_FUNCTION_CONTENT = '''\
{header}\
from aiogram.types import Message
from aiogram.dispatcher import FSMContext


async def {name}_func(mes: Message, state: FSMContext):
    """
    Description: Echo bot function.
    """
    await mes.answer(mes.text, reply=True)
'''