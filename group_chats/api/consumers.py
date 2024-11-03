from accounts.models import CustomUser
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from group_chats.models import GroupChat, Message
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group_name = f'chat_{self.group_id}'

        # Add the user to the chat group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Remove the user from the chat group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        sender_id = data.get('sender_id')

        # Retrieve sender and group info
        sender = await sync_to_async(CustomUser.objects.get)(id=sender_id)
        group_chat = await sync_to_async(GroupChat.objects.get)(id=self.group_id)

        # Save message to database
        new_message = await sync_to_async(Message.objects.create)(
            group_chat=group_chat,
            sender=sender,
            comment=message
        )

        # Broadcast message to the group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.email,
                'timestamp': str(new_message.timestamp)
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp']
        }))
        print('Message sent successfully================ ')