from os import name
from re import I
from django.urls import path
from .views import *

urlpatterns = [
    path('index',index_view,name='index'),
    path('file/<int:id>',file_single,name='file-single'),
    path('add-file',add_file,name="add-file")
    
]