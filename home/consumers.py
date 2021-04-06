from channels.generic.websocket import AsyncWebsocketConsumer






class CommentConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        self.file_id = self.scope['url_route']['kwargs']['id']
        self.group_name = "file_%s" % (self.file_id)
        user = self.scope['user']
        await self.channel_layer.group_add(self.group_name,self.channel_name)


        await self.accept()
    

    async def disconnect(self):
        await self.channel_layer.group_discard(self.group_name,self.channel_name)
    
    