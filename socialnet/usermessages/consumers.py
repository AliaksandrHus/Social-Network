import json
from channels.generic.websocket import WebsocketConsumer

from account.models import Profile
from usermessages.models import Messages, Dialog


# class ChatConsumer(WebsocketConsumer):
#
#     def connect(self):
#     # принять соединение
#         self.accept()
#
#     def disconnect(self, close_code):
#         pass
#
#     def receive(self, text_data):
#
        # message = Messages()
        # message.dialog = Dialog.objects.get(id=text_data['dialog'])
        # message.author = Profile.objects.get(profile_id=text_data['user'])
        # message.content = text_data['message']
        # message.save()
#
#         print(text_data)
#
#         json_data = json.dumps(text_data)
#         self.send(text_data=json_data)
#
#
#     def send(self, text_data):
#
#         print('SEND - !!!!!!!')


# from channels.generic.websocket import AsyncWebsocketConsumer
#
# class PushNotificationConsumer(AsyncWebsocketConsumer):
#
#     async def connect(self):
#         print('connect')
#         await self.accept()
#
#
#     async def receive(self, text_data):
#         # Обработка полученного сообщения
#         print('receive - +++++', text_data)
#         await self.send(text_data="Received: {}".format(text_data))
#
#     async def send(self, text_data):
#
#         print('SEND - !!!!!!!')
#
#
#     async def disconnect(self, close_code):
#         pass


from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):

    def connect(self):

        self.room_name = self.scope["url_route"]["kwargs"]["dialog_id"]
        self.room_group_name = "chat_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    def chat_message(self, event):

        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))