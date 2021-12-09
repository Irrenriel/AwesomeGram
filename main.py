from aiogram import executor, Dispatcher
from resources.models import dp, loop, db

# The most important to write this import!
from src import handlers


async def startup_func(dp: Dispatcher):
    # con = await db.connect()
    # if not con:
    #     raise Exception('Can not connect to Database')
    print('< < < Bot is working! > > >')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, loop=loop)