from accounts.models import CustomUser
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from group_chats.models import GroupChat, Message
from asgiref.sync import sync_to_async
import logging

logger = logging.getLogger(__name__)


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
        # Check for empty or malformed JSON message
        if not text_data:
            await self.send(text_data=json.dumps({"error": "Empty message received"}))
            return

        try:
            # Parse the JSON data
            data = json.loads(text_data)
            message = data.get('message')
            sender_id = data.get('sender_id')

            if not message or not sender_id:
                await self.send(text_data=json.dumps({"error": "Invalid message or sender_id"}))
                return

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

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON format"}))
            logger.error(f"Failed to decode JSON: {text_data}")  # Logs the problematic input
        except CustomUser.DoesNotExist:
            await self.send(text_data=json.dumps({"error": "Sender does not exist"}))
            logger.error(f"Sender with ID {sender_id} does not exist")
        except GroupChat.DoesNotExist:
            await self.send(text_data=json.dumps({"error": "Group chat does not exist"}))
            logger.error(f"Group chat with ID {self.group_id} does not exist")
        except Exception as e:
            await self.send(text_data=json.dumps({"error": "An unexpected error occurred"}))
            logger.error(f"Unexpected error: {e}")

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp']
        }))
