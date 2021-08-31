from .models import Profile
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer, ProfileSerializer
from rest_framework import viewsets
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):           
        print(request.data)
        user = self.get_object()                      
        if 'username' in request.data and user.username != request.data['username']:            
            user.username=request.data['username']                                     
        if 'first_name' in request.data and user.first_name != request.data['first_name']:
            user.first_name=request.data['first_name'] 
        if 'last_name' in request.data and user.last_name != request.data['last_name']:
            user.last_name=request.data['last_name']   
        if 'phone_number' in request.data and user.profile.phone_number != request.data['phone_number']:
            user.profile.phone_number=request.data['phone_number']    
        if 'birth_date' in request.data and user.profile.birthday != request.data['birth_date']:
            user.profile.birthday=request.data['birth_date']    
        if 'avatar' in request.data and user:
            user.profile.avatar=request.data['avatar']                
        user.save()
        serializer = UserSerializer(user)
        headers = self.get_success_headers(serializer.data)        
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    callback_url = 'http://localhost:3000/'
    client_class = OAuth2Client

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:3000/'
    client_class = OAuth2Client