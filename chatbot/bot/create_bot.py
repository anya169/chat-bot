import os
from pathlib import Path
import sys
from decouple import config
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')
from asgiref.sync import sync_to_async

_django_initialized = False

async def setup_django():
   global _django_initialized
   if not _django_initialized:
      import django
    
      BASE_DIR = Path(__file__).resolve().parent.parent
      sys.path.append(str(BASE_DIR))
      os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')
      django.setup()
      _django_initialized = True

async def get_curators_telegram_ids():
   await setup_django()
   from core.models import Employee
   
   def sync_get():
      return list(Employee.objects.filter(
         is_curator=True, 
         telegram_id__isnull=False
      ).values_list('telegram_id', flat=True))
   
   return await sync_to_async(sync_get)()