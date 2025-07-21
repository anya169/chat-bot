import asyncio
from create_bot import bot, dp
from handlers.start import start_router
from handlers.question import question_router
from handlers.registration import registration_router
from handlers.after_1_month import after_1_month_router
from handlers.after_3_month import after_3_month_router
from handlers.after_6_month import after_6_month_router
from polls import initialize_poll_data
from bot.utils import get_bot
from scheduler import schedule_polls

async def main():
    bot = get_bot()
    # await initialize_poll_data() # использовать функцию только при первом запуске, потом нужно закомментировать
    dp.include_router(start_router)
    dp.include_router(question_router)
    dp.include_router(registration_router)
    dp.include_router(after_1_month_router)
    dp.include_router(after_3_month_router)
    dp.include_router(after_6_month_router)
    await bot.delete_webhook(drop_pending_updates = True)
    asyncio.create_task(schedule_polls())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())