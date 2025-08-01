import os
import django
import sys
from asgiref.sync import sync_to_async

sys.path.append('C:/chat-bot/chatbot')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')
django.setup()

from core.models import Filial

async def initialize_filials_data():
    return await sync_to_async(list)(Filial.objects.all())
    # # Список филиалов для добавления в базу
    # branches_data = [
    #     "Администрация",
    #     "Алданское ЛПУМГ",
    #     "Александровское ЛПУМГ",
    #     "Алтайское ЛПУМГ",
    #     "Амурское ЛПУМГ",
    #     "Барабинское ЛПУМГ",
    #     "Инженерно-технический центр",
    #     "Иркутское ЛПУМГ",
    #     "Камчатское ЛПУМГ",
    #     "Кемеровское ЛПУМГ",
    #     "Корпоративный институт",
    #     "Ленское ЛПУМГ",
    #     "Магистральное ЛПУМГ",
    #     "Нерюнгринское ЛПУМГ",
    #     "Новокузнецкое ЛПУМГ",
    #     "Новосибирское ЛПУМГ",
    #     "Омское ЛПУМГ",
    #     "Приморское ЛПУМГ",
    #     "Сахалинское ЛПУМГ",
    #     "Свободненское ЛПУМГ",
    #     "Сковородинское ЛПУМГ",
    #     "Томское ЛПУМГ",
    #     "Управление АВР",
    #     "Управление АВР №2",
    #     "Управление МТСиК",
    #     "Управление ТТиСТ",
    #     "Юргинское ЛПУМГ",
    #     "Хабаровское ЛПУМГ"
    # ]
    # for branch_name in branches_data:
    #     filial = Filial(
    #         name = branch_name
    #     )
    #     await sync_to_async(filial.save)()