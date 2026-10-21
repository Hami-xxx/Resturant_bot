import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv

from config import settings

from handlers import user, order, product, admin

load_dotenv()

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(user.router)
dp.include_router(product.router)
dp.include_router(order.router)
dp.include_router(admin.router)

async def main():
    print("BOT STARTING...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())