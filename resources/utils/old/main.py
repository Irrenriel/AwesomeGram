from logging import info

from aiogram import executor, Dispatcher

from resources.utils.old.config import config


async def startup_func(dp: Dispatcher):
    info('= = = Starting a bot! = = =')
    info(f'Current version: {config.CURRENT_VERSION}')

    # Skip updates
    await dp.skip_updates()

    # Handlers
    await run_handlers(dp)

    info('= = = = = = = = =')

    # Connecting to databases
    # await db.connect()

    info('= = = = = = = = =')

    # Middlewares
    await installing_middlewares(dp)

    info('= = = Bot is working! = = =')


if __name__ == '__main__':
    # Logging:
    bot_logging.set_logging(config.debug)

    executor.start_polling(dp, loop=loop, on_startup=startup_func)
