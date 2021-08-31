from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.utils.translation import gettext as _
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Profile
        read_only_fields = ('created_at', 'updated_at', 'role')        
        exclude = ('user',)
     
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'profile'
        )