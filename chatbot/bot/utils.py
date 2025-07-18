from aiogram import Bot
from decouple import config

bot_instance = None

def get_bot():
    global bot_instance
    if bot_instance is None:
        bot_instance = Bot(token=config('TOKEN'))
    return bot_instance