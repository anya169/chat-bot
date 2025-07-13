from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import admins
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# инлайн клавиатура с филиалами
def branches_kb() -> InlineKeyboardMarkup:
    # список с филиалами
    branches = [
        "Администрация",
        "Алданское ЛПУМГ",
        "Александровское ЛПУМГ",
        "Алтайское ЛПУМГ",
        "Амурское ЛПУМГ",
        "Барабинское ЛПУМГ",
        "Инженерно-технический центр",
        "Иркутское ЛПУМГ",
        "Камчатское ЛПУМГ",
        "Кемеровское ЛПУМГ",
        "Корпоративный институт",
        "Ленское ЛПУМГ",
        "Магистральное ЛПУМГ",
        "Нерюнгринское ЛПУМГ",
        "Новокузнецкое ЛПУМГ",
        "Новосибирское ЛПУМГ",
        "Омское ЛПУМГ",
        "Приморское ЛПУМГ",
        "Сахалинское ЛПУМГ",
        "Свободненское ЛПУМГ",
        "Сковородинское ЛПУМГ",
        "Томское ЛПУМГ",
        "Управление АВР",
        "Управление АВР №2",
        "Управление МТСиК",
        "Управление ТТиСТ",
        "Юргинское ЛПУМГ",
        "Хабаровское ЛПУМГ"
    ]
    buttons = [
        InlineKeyboardButton(text = branch, callback_data = f"branch_{branch}") 
        for branch in branches
    ]
    return InlineKeyboardMarkup(inline_keyboard = [[button] for button in buttons])

# клавиатура с кнопкой "Рассказать о себе"
def tell_about_myself_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text = "Рассказать о себе")]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text = "Создать опрос")]) # кнопка, которая видна только админу
    keyboard = ReplyKeyboardMarkup(
        keyboard = kb_list,
        resize_keyboard = True, # автоматически подгоняет размер кнопок под экран
        one_time_keyboard = True # клавиатура скроется после нажатия
    )
    return keyboard

# клавиатура с кнопкой "Я не знаю свой табельный номер"
def service_number_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text = "Я не знаю свой табельный номер")]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text = "Создать опрос")]) # кнопка, которая видна только админу
    keyboard = ReplyKeyboardMarkup(
        keyboard = kb_list,
        resize_keyboard = True, # автоматически подгоняет размер кнопок под экран
        one_time_keyboard = True # клавиатура скроется после нажатия
    )
    return keyboard

# клавиатура с кнопкой "Ознакомился(ась)"
def reviewed_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text = "Ознакомился(ась)")]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text = "Создать опрос")]) # кнопка, которая видна только админу
    keyboard = ReplyKeyboardMarkup(
        keyboard = kb_list,
        resize_keyboard = True, # автоматически подгоняет размер кнопок под экран
        one_time_keyboard = True # клавиатура скроется после нажатия
    )
    return keyboard

# клавиатура с кнопкой "Задание"
def task_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text = "Задание")]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text = "Создать опрос")]) # кнопка, которая видна только админу
    keyboard = ReplyKeyboardMarkup(
        keyboard = kb_list,
        resize_keyboard = True, # автоматически подгоняет размер кнопок под экран
        one_time_keyboard = True # клавиатура скроется после нажатия
    )
    return keyboard

# клавиатура с кнопкой "Я заполнил(а)"
def done_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text = "Я заполнил(а)")]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text = "Создать опрос")]) # кнопка, которая видна только админу
    keyboard = ReplyKeyboardMarkup(
        keyboard = kb_list,
        resize_keyboard = True, # автоматически подгоняет размер кнопок под экран
        one_time_keyboard = True # клавиатура скроется после нажатия
    )
    return keyboard

# клавиатура с кнопкой "Получить рекомендации"
def recommendations_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text = "Получить рекомендации")]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text = "Создать опрос")]) # кнопка, которая видна только админу
    keyboard = ReplyKeyboardMarkup(
        keyboard = kb_list,
        resize_keyboard = True, # автоматически подгоняет размер кнопок под экран
        one_time_keyboard = True # клавиатура скроется после нажатия
    )
    return keyboard

# клавиатура с кнопкой "Хочу задать вопрос"
def question_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text = "Хочу задать вопрос")]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text = "Создать опрос")]) # кнопка, которая видна только админу
    keyboard = ReplyKeyboardMarkup(
        keyboard = kb_list,
        resize_keyboard = True, # автоматически подгоняет размер кнопок под экран
        one_time_keyboard = True # клавиатура скроется после нажатия
    )
    return keyboard