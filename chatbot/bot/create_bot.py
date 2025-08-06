import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
from decouple import config
from config import ADMINS 
import asyncio
from asgiref.sync import sync_to_async
import django
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')
django.setup()
from core.models import Employee


media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
async def get_curators_telegram_ids():
   def sync_get():
      return list(Employee.objects.filter(is_curator=True, telegram_id__isnull=False).values_list('telegram_id', flat=True))
   
   return await sync_to_async(sync_get)()
 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
