from asgiref.sync import sync_to_async
import json 
import jwt 
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from urllib.parse import parse_qs


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connection started...")

        query_string = self.scope['query_string'].decode('utf-8')
        print("Query string:", query_string)
        params = parse_qs(query_string)
        token = params.get('token', [None])[0]
        print("Received token:", token)

        await self.accept()  # TEMPORARY: Accept early for debugging

        if token:
            try:
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                print("Decoded token:", decoded_data)

                self.user = await self.get_user(decoded_data['user_id'])
                print("User found:", self.user)
                self.scope['user'] = self.user
            except jwt.ExpiredSignatureError:
                print("Token expired.")
                await self.close(code=4000)
                return
            except jwt.InvalidTokenError:
                print("Invalid token.")
                await self.close(code=4001)
                return
            except Exception as e:
                print("Unexpected token decode error:", e)
                await self.close(code=4003)
                return
        else:
            print("No token provided.")
            await self.close(code=4002)
            return

        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
        print("Room group:", self.room_group_name)

        # Add channel to the  group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        user_data = await self.get_user_data(self.user)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'online_status',
                'online_users': [user_data],
                'status': 'online',
            }
        )

    async def disconnect(self, close_code):
        print(f"WebSocket disconnected: {close_code}")
        if hasattr(self, 'room_group_name'):
            user_data = await self.get_user_data(self.scope["user"])
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'online_status',
                    'online_users': [user_data],
                    'status': 'offline',
                }
            )
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        print("Message received:", text_data)
        text_data_json = json.loads(text_data)
        event_type = text_data_json.get('type')

        if event_type == 'chat_message':
            message_content = text_data_json.get('message')
            user_id = text_data_json.get('user')
            print("chat_message from:", user_id)

            try:
                user = await self.get_user(user_id)
                conversation = await self.get_conversation(self.conversation_id)
                from .serializers import UserListSerializer
                user_data = UserListSerializer(user).data

                message = await self.save_message(conversation, user, message_content)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message.content,
                        'user': user_data,
                        'timestamp': message.timestamp.isoformat(),
                    }
                )
            except Exception as e:
                print(f"Error saving message: {e}")
        
        elif event_type == 'typing':
            try:
                user_data = await self.get_user_data(self.scope['user'])
                receiver_id = text_data_json.get('receiver')
                print("Typing event from:", user_data)

                if receiver_id is not None:
                    receiver_id = int(receiver_id)
                    if receiver_id != self.scope['user'].id:
                        print(f"{user_data['username']} is typing to {receiver_id}")
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                'type': 'typing',
                                'user': user_data,
                                'receiver': receiver_id,
                            }
                        )
            except Exception as e:
                print(f"Typing event error: {e}")

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'user': event['user'],
            'timestamp': event['timestamp'],
        }))
    
    async def typing(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user': event['user'],
            'receiver': event.get('receiver'),
            'is_typing': True,
        }))

    async def online_status(self, event):
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def get_user(self, user_id):
        from django.contrib.auth import get_user_model
        return get_user_model().objects.get(id=user_id)

    @sync_to_async
    def get_user_data(self, user):
        from .serializers import UserListSerializer
        return UserListSerializer(user).data

    @sync_to_async
    def get_conversation(self, conversation_id):
        from .models import Conversation
        return Conversation.objects.get(id=conversation_id)

    @sync_to_async
    def save_message(self, conversation, user, content):
        from .models import Message
        return Message.objects.create(
            conversation=conversation,
            sender=user,
            content=content
        )
