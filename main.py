from aiogram import Bot, Dispatcher
from asyncio import get_event_loop, gather
from banedetta_db import DB
from bot.managers.log_manager import logger
from config import config
from dotenv import load_dotenv
from os import getenv

load_dotenv(override = True)

db = DB(
	getenv("host"), getenv("user"), getenv("password"),
	getenv("schema"), int(getenv("port"))
)
bot = Bot(getenv("token"))
dp = Dispatcher()

async def start_bot():
	from bot.routers.tg_router import rt
	dp.include_routers(rt)

	async def on_startup():
		logger.info("Telegram bot is working")

	dp.startup.register(on_startup)
	await bot.delete_webhook(drop_pending_updates = True)
	await dp.start_polling(bot)

async def start_synchronization():
	from bot.synchronization.data_synchronizer import synchronization
	await db.init()
	await synchronization()

async def main():
	await gather(start_bot(), start_synchronization())

if __name__ == "__main__":
	try:
		loop = get_event_loop()
		loop.run_until_complete(main())
	except KeyboardInterrupt:
		logger.info("Shutdown...")