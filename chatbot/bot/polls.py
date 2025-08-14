from datetime import timedelta
import os
import django
import sys
from asgiref.sync import sync_to_async

sys.path.append('C:/chat-bot/chatbot')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')
django.setup()

from core.models import Poll, Question

async def initialize_poll_data(poll_name):
    # poll = await sync_to_async(Poll.objects.get)(name=poll_name)
    # questions = await sync_to_async(list)(Question.objects.filter(poll=poll))
    # return [q.name for q in questions]
    poll_after_1_month = Poll(
        name = "Опрос через месяц",
        submission_date = timedelta(days = 30)
    )
    poll_after_3_month = Poll(
        name = "Опрос через 3 месяца",
        submission_date = timedelta(days = 90)
    )
    poll_after_6_month = Poll(
        name = "Опрос через 6 месяцев",
        submission_date = timedelta(days = 180)
    )
    poll_after_12_month = Poll(
        name = "Опрос через 12 месяцев",
        submission_date = timedelta(days = 180)
    )
    await sync_to_async(poll_after_1_month.save)()
    await sync_to_async(poll_after_3_month.save)()
    await sync_to_async(poll_after_6_month.save)()
    await sync_to_async(poll_after_12_month.save)()
    poll_after_1_month = await sync_to_async(Poll.objects.get)(name = "Опрос через месяц")
    poll_after_3_month = await sync_to_async(Poll.objects.get)(name = "Опрос через 3 месяца")
    poll_after_6_month = await sync_to_async(Poll.objects.get)(name = "Опрос через 6 месяцев")
    poll_after_12_month = await sync_to_async(Poll.objects.get)(name = "Опрос через 12 месяцев")
    questions_for_poll_1_data = [
        "Как дела?", 
        "Удалось пройти трек по адаптации в ГИД?",
        "Был ли полезным и информативным для тебя трек в приложении?",
        "Расскажи, что больше всего заинтересовало?",
        "Есть ли такая информация, которой не хватило?",
        "Ты уже подписал(а) все необходимые документы?",
        "А обходной лист прошел(а)?",
        "Прошел(а) инструктажи? Какие, расскажешь?",
        "Расскажи про рабочее место. Какое оно у тебя?",
        "Все ли необходимое для работы есть в нем?",
        "Все ли доступы для работы имеются у тебя? ПК, пропуск? Каких не хватает?",
        "Тебе рассказали про твои функциональные обязанности?",
        "Они совпадают с тем, что заявляли на этапе собеседования?",
        "В каком формате получаешь трудовые задачи?",
        "Назначен ли куратор/наставник?",
        "Вы уже начали работу с ним? Опишите в пару словах формат работы. Возможно план работы уже у вас составлен.",
        "Была ли встреча с председателем совета молодежи филиала?",
        "Уже принял(а) участие в каких-либо мероприятиях филиала?",
        "Есть ли у тебя вопросы?"
    ]
    questions_for_poll_3_data = [
        "Как обстоят дела в производственной среде?",
        "Как часто встречаешься со своим руководителем?",
        "Комфортно ли тебе взаимодействовать с руководителем?",
        "В каком формате ты получаешь задачи?",
        "Дают ли тебе обратную связь?",
        "Как часто её даёт тебе руководитель? А наставник?",
        "Положительная или отрицательная обратная связь?",
        "Всегда ли руководитель и наставник дают тебе обратные ответы на вопросы?",
        "Полезен ли закрепленный за тобой наставник?",
        "Удалось ли принять участие в мероприятиях филиала?",
        "Чего тебе не хватает для улучшения реализации трудовой деятельности?",
        "Может есть волнующие моменты, которые тебя беспокоят?"
    ]
    questions_for_poll_6_data = [
        "Как обстоят дела в производственной среде?",
        "Как часто встречаешься со своим руководителем?",
        "Комфортно ли тебе взаимодействовать с руководителем?",
        "Всегда ли руководитель и наставник дают тебе обратные ответы на вопросы?",
        "Удалось ли принять участие в мероприятиях филиала?",
        "Чего тебе не хватает для улучшения реализации трудовой деятельности?",
        "Может есть волнующие моменты, которые тебя беспокоят?"
    ]
    questions_for_poll_12_data = [
        "Как обстоят дела в производственной среде?",
        "Какой самый значимый успех ты достиг за этот год и почему именно он особенно важен для тебя?Какой самый значимый успех ты достиг за этот год и почему именно он особенно важен для тебя?",
        "Есть ли ощущение комфорта и уверенности в рабочих процессах на сегодняшний день?",
        "Достаточны ли знания и навыки для выполнения поставленных задач?",
        "Комфортно ли тебе взаимодействовать с руководителем?",
        "Устраивает ли тебя нынешняя организация твоего рабочего места? Комфортно ли тебе там находиться и продуктивно работать?",
        "Может есть волнующие моменты, которые тебя беспокоят?"
    ]
    for question_text in questions_for_poll_1_data:
        question = Question(
            name = question_text,
            poll_id = poll_after_1_month.id
        )
        await sync_to_async(question.save)()
    for question_text in questions_for_poll_3_data:
        question = Question(
            name=question_text,
            poll_id = poll_after_3_month.id
        )
        await sync_to_async(question.save)()
    for question_text in questions_for_poll_6_data:
        question = Question(
            name=question_text,
            poll_id = poll_after_6_month.id
        )
        await sync_to_async(question.save)()
    for question_text in questions_for_poll_12_data:
        question = Question(
            name=question_text,
            poll_id = poll_after_12_month.id
        )
        await sync_to_async(question.save)()
