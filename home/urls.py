from os import name
from django.urls import path , re_path
from .views import *

urlpatterns = [
    path('',index_view,name='index'),
    path('file/<int:id>',file_single,name='file-single'),
    path('add-file',add_file,name="add-file"),
    path('shared-with-you',shared_files,name='shared-with-you'),
    path('give-permission',file_permission,name='give-permission'),
    path('permission-list',permission_list,name='permission-list'),



    re_path(r'(?P<file_id>.*)/download/(?P<path>.*)', download_file, name='file-download'),
    re_path(r'(?P<file_id>.*)/view/(?P<path>.*)', view_file, name='file-view')

    
]