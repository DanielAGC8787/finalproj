# from channels.consumer import SyncConsumer

# class EchoConsumer():
#     def websocket_connect(self, event):
#         print('Connect event is called')
    
#     def websocket_receive(self, event):
#         print("new event is received")
#         print(event)


import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        # self.send(text_data=json.dumps({
        #     'type' : 'connection_established',
        #     'message' : 'You are now connected!'
        # }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        self.send(text_data = json.dumps({
            'type': 'chat',
            'message': message,
            'sender': sender
        }))

#         # print('Message', message)

#         # #send message back to client whenever we receive a message
#         # self.send(text_data=json.dumps({
#         #     'type': 'chat', 
#         #     'message': message
#         # }))