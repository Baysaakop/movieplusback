import string
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Artist
from .serializers import ArtistSerializer
from rest_framework import viewsets


class ArtistViewSet(viewsets.ModelViewSet):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all().order_by('-created_at')

    def get_queryset(self):
        queryset = Artist.objects.all().order_by('-created_at')
        name = self.request.query_params.get('name', None)
        occupation = self.request.query_params.get('occupation', None)
        order = self.request.query_params.get('order', None)
        if name is not None:
            queryset = queryset.filter(Q(name__icontains=name) | Q(
                name__icontains=string.capwords(name))).distinct()
        if occupation is not None:
            queryset = queryset.filter(occupation__id=occupation)
        if order is not None:
            if (order == 'created_at'):
                queryset = queryset.order_by('-created_at')
            elif (order == 'birthday'):
                queryset = queryset.order_by('-birthday')
            elif (order == 'name'):
                queryset = queryset.order_by('name')
            elif (order == 'views'):
                queryset = queryset.order_by('-views')
            elif (order == 'likes'):
                queryset = queryset.order_by('-likes')
            elif (order == 'follows'):
                queryset = queryset.order_by('-follows')
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count = instance.view_count + 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.data['token']).user
        artist = Artist.objects.create(
            name=request.data['name'],
            created_by=user
        )
        updateArtist(artist, request)
        serializer = ArtistSerializer(artist)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        artist = self.get_object()
        user = Token.objects.get(key=request.data['token']).user
        artist.updated_by = user
        updateArtist(artist, request)
        serializer = ArtistSerializer(artist)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


def updateArtist(artist, request):
    if 'name' in request.data:
        artist.name = request.data['name']
    if 'firstname' in request.data:
        artist.firstname = request.data['firstname']
    if 'lastname' in request.data:
        artist.lastname = request.data['lastname']
    if 'biography' in request.data:
        artist.biography = request.data['biography']
    if 'birthdate' in request.data:
        artist.birthdate = request.data['birthdate']
    if 'gender' in request.data:
        artist.gender = request.data['gender']
    if 'avatar' in request.data:
        artist.avatar = request.data['avatar']
    if 'occupations' in request.data:
        artist.occupations.clear()
        arr = str(request.data['occupations']).split(',')
        for item in arr:
            artist.occupations.add(int(item))
    if 'facebook_channel' in request.data:
        artist.facebook_channel = request.data['facebook_channel']
    if 'instagram_channel' in request.data:
        artist.instagram_channel = request.data['instagram_channel']
    if 'twitter_channel' in request.data:
        artist.twitter_channel = request.data['twitter_channel']
    if 'youtube_channel' in request.data:
        artist.youtube_channel = request.data['youtube_channel']
    artist.save()
    return artist
