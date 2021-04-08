from sys import executable
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

from django.contrib.auth.models import User
from .models import *
from account.models import *
from datetime import datetime

@database_sync_to_async
def comment_save_to_db(**data):
    for value in data.values():
        if value == "":
            return False
    
    user = CustomUser.objects.get(username=data['user'])  
    comment = Comment.objects.create(user=user,file_id =data['file'],text=data['text'])
    return comment



class CommentConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        self.file_id = self.scope['url_route']['kwargs']['id']
        self.group_name = "file_%s" % (self.file_id)
        user = self.scope['user']
        await self.channel_layer.group_add(self.group_name,self.channel_name)


        await self.accept()
    

    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(self.group_name,self.channel_name)
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        comment = await comment_save_to_db(user=data['user'],file=data['file'],text=data['text'])
        if comment:
            await self.channel_layer.group_send(self.group_name,
            {
                'type':'send_comment',
                'comment_id':comment.id,
                'user':data['user'],
                'text':data['text'],
                'date':datetime.now().strftime("%m/%d/%Y, %H:%M")



            })
        else:
            await self.channel_layer.send(self.channel_name,
            {
                'type':'error',
                'text':'Xeta bas verdi'
            })
    

    async def send_comment(self,event):
        data = {'status':'created','user':event['user'],'comment_id':event['comment_id'],'text':event['text'],'date':event['date']}
        await self.send(json.dumps(data))

    
    async def error(self,event):
        data = {'status':'error','text':event['text']}
        await self.send(json.dumps(data))



    