import asyncio
from create_bot import bot, dp
from handlers.start import start_router
from handlers.question import question_router
from handlers.poll_1 import poll_1_router
from handlers.after_1_month import after_1_month_router
from handlers.after_3_month import after_3_month_router
from handlers.after_6_month import after_6_month_router

async def main():
    dp.include_router(start_router)
    dp.include_router(question_router)
    dp.include_router(poll_1_router)
    dp.include_router(after_1_month_router)
    dp.include_router(after_3_month_router)
    dp.include_router(after_6_month_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())