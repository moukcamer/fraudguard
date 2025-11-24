# apps/fraud_detection/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class FraudAlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("fraud_alerts", self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({
            "type": "connection",
            "message": "Connecté aux alertes en temps réel"
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("fraud_alerts", self.channel_name)

    async def fraud_alert(self, event):
        await self.send(text_data=json.dumps(event["message"]))