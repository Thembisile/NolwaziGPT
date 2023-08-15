# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # This is where you'd plug in your model to get a response
#         # Pseudo-code example:
#         for partial_response in model.generate(message, stream=True):
#             await self.send(text_data=json.dumps({
#                 'message': partial_response
#             }))
