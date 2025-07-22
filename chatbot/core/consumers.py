import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Employee, Special_Question

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
   def connect(self):
      self.employee_id = self.scope['url_route']['kwargs']['employee_id']
      self.room_group_name = f'chat_{self.employee_id}'
      
      #присоединиться к чату
      async_to_sync(self.channel_layer.group_add)(
         self.room_group_name,
         self.channel_name
      )
      self.accept()
   
   def disconnect(self, close_code):
      #покинуть чат
      if hasattr(self, 'channel_layer'):
            async_to_sync(self.channel_layer.group_discard)(
                  self.room_group_name,
                  self.channel_name
            )
   
   def receive(self, text_data):
      print("Получены данные:", text_data)
      text_data_json = json.loads(text_data)
      message = text_data_json['message']
      sender_id = text_data_json['sender_id']
      
      employee = Employee.objects.get(login=sender_id)
      
      if not employee.is_curator:  #если это вопрос от сотрудника
         # создаем новый вопрос
        # Special_Question.objects.create(
         #      name=message,
         #      employee_id=employee.id
         #)
         print("это сотрудник")
         async_to_sync(self.channel_layer.group_send)(
                  self.room_group_name,
                  {
                     'type': 'chat_message',
                     'message': message,
                     'sender_id': sender_id
                  }
            )
      else:  # если это сообщение от куратора
         print("это куратор")
         #находим последнее сообщение от сотрудника
         question = Special_Question.objects.filter(
               employee_id=self.employee_id,
               answer__isnull=True
         ).last()
         if question:
               question.answer = message
               question.save()
      
      #отправляем сообщение
      async_to_sync(self.channel_layer.group_send)(
         self.room_group_name,
         {
            'type': 'chat_message',
            'message': message,
            'sender_id': sender_id
         }
      )
   
   def chat_message(self, event):
      message = event['message']
      sender_id = event['sender_id']
      
      self.send(text_data=json.dumps({
         'message': message,
         'sender_id': sender_id
      }))