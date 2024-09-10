import json

from channels.generic.websocket import AsyncWebsocketConsumer

from core.utils.console import Console


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        Console().log(self.scope.get("user").phone)
        await self.channel_layer.group_add("chat", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        self.channel_layer.group_discard("chat", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        await self.channel_layer.group_send(
            "chat", {"type": "chat_message", "message": message}
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
