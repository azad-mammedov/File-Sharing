from django.db.models.fields.related import create_many_to_many_intermediary_model
from django.shortcuts import render ,get_object_or_404
import rest_framework
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .serializers import *
from .models import *


class PermissionApi(APIView):
    authentication_classes = [SessionAuthentication,]
    permission_classes = [IsAuthenticated,]


    def post(self,request):
        print(request.data)
        serializer  = PermissionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if Permission.objects.filter(user=serializer.validated_data['user'],file=serializer.validated_data['file']).exists():
                return Response({'message':'This permission already exists'})
            serializer.save()
            return Response({'message':'permission gived'})

    
    def put(self,request,id):
        permission = get_object_or_404(Permission.objects.all(),id=id)
        serializer = PermissionSerializer(permission,request.data,partial=True)
        if serializer.is_valid(raise_exception=True) and request.user == permission.given_from:
            serializer.save()
            return Response({'message':'permission changed'})
        else:
            return Response({'message':'access denied'},status=403)


    def delete(self,request,id):
        permission = get_object_or_404(Permission.objects.all(),id=id)
        if request.user == permission.given_from:
            permission.delete()
            return Response({'message':'permission deleted'})
        else:
            return Response({'message':'access denied'},status=403)
        
        




class CommentApi(APIView):
    authentication_classes = [SessionAuthentication,]
    permission_classes = [IsAuthenticated]
    


    def delete(self,request,file_id,comment_id):
        file = get_object_or_404(File.objects.all(),id=file_id)
        comment = get_object_or_404(Comment.objects.all(),id=comment_id)
        if request.user == file.user or request.user == comment.user:
            
            comment.delete()
            return Response({'comment':'deleted'},status=200)
        else:
            raise PermissionDenied("You dont have permission for this",code=403)





class FileApi(APIView):
    def delete(self,request,file_id):
        file = get_object_or_404(File.objects.all(),id=file_id)
        if request.user == file.user:
            file.delete()
            return  Response({'file':'deleted'},status=200)
        else:
            raise PermissionDenied('You dont have permission for this operation',code=403)


