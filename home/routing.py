from django.urls import path
from .consumers import CommentConsumer

urlpatters = [
    path('ws/file/<int:id>',CommentConsumer)


]
