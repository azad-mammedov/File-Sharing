from rest_framework import serializers
from account.models import *
from home.models import *

class PermissionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Permission
        fields = "__all__"
        