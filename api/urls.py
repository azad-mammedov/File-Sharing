from django.urls import path
from .views import *

urlpatterns = [
    path('permission/add',PermissionApi.as_view()),
    path('permission/update/<int:id>',PermissionApi.as_view()),
    path('permission/delete/<int:id>',PermissionApi.as_view()),

    path('file/delete/<int:file_id>',FileApi.as_view()),

    path('comment/delete/<int:file_id>/<int:comment_id>',CommentApi.as_view())
    
]
