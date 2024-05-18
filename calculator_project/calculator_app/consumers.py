import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ProUser,Message
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']  # Отримуємо ім'я користувача з повідомлення
        room_name = text_data_json.get('room_name')
        user = self.scope["user"]
        await sync_to_async(Message.objects.create)(user=user, room_name=room_name, message=message)

        await self.channel_layer.group_send(
            room_name,{
                'type': 'chat_message',
                'message': message,
                'username': username,  # Передаємо ім'я користувача разом з повідомленням
                'room_name': room_name
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']  # Отримуємо ім'я користувача з події
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username  # Передаємо ім'я користувача разом з повідомленням
        }))

online_users = set()

class OnlineUsersConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope["user"].username
        online_users.add(self.username)

        await self.channel_layer.group_add("online_users", self.channel_name)
        
        await self.accept()

        await self.send_online_users()

    async def disconnect(self, close_code):
        online_users.discard(self.username)
        
        await self.channel_layer.group_discard("online_users", self.channel_name)

        await self.send_online_users()

    async def send_online_users(self):
        online_users_list = list(online_users)
        await self.channel_layer.group_send(
            "online_users",
            {
                "type": "user_list",
                "online_users": online_users_list,
            }
        )

    async def user_list(self, event):
        await self.send(text_data=json.dumps({
            "online_users": event["online_users"]
        }))


