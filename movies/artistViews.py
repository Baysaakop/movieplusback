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
            queryset = queryset.filter(name__icontains=name)
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
        instance.views = instance.views + 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# class TempArtistViewSet(viewsets.ModelViewSet):
#     serializer_class = TempArtistSerializer
#     queryset = TempArtist.objects.all().order_by('-created_at')

#     def get_queryset(self):
#         queryset = TempArtist.objects.all().order_by('-created_at')
#         artistid = self.request.query_params.get('artistid', None)
#         if artistid is not None:
#             if artistid == '0':
#                 queryset = TempArtist.objects.filter(artistid=0).order_by('created_at')
#             else:
#                 queryset = TempArtist.objects.filter(~Q(artistid=0)).order_by('created_at')
#         return queryset

#     def create(self, request, *args, **kwargs):
#         user = Token.objects.get(key=request.data['token']).user
#         tempartist = None
#         # CREATE
#         if 'artistid' not in request.data:
#             tempartist = TempArtist.objects.create(
#                 name=request.data['name'],
#                 created_by=user
#             )
#             updateArtist(tempartist, request)
#         # UPDATE
#         else:
#             artist = Artist.objects.get(pk=int(request.data['artistid']))
#             tempartist = TempArtist.objects.create(
#                 name=artist.name,
#                 updated_by=user,
#                 artistid=artist.id
#             )
#             copyArtist(tempartist, artist)
#             updateArtist(tempartist, request)
#         serializer = TempArtistSerializer(tempartist)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def update(self, request, *args, **kwargs):
#         tempartist = self.get_object()
#         if 'accept' in request.data:
#             # CREATE
#             if tempartist.artistid == 0:
#                 artist = Artist.objects.create(
#                     name=tempartist.name,
#                     created_by=tempartist.created_by,
#                 )
#                 copyArtist(artist, tempartist)
#                 TempArtist.objects.filter(id=tempartist.id).delete()
#                 return Response(status=status.HTTP_200_OK)
#             # UPDATE
#             else:
#                 artist = Artist.objects.get(pk=tempartist.artistid)
#                 artist.name=tempartist.name
#                 artist.updated_by=tempartist.updated_by
#                 copyArtist(artist, tempartist)
#                 TempArtist.objects.filter(id=tempartist.id).delete()
#                 return Response(status=status.HTTP_200_OK)
#         elif 'decline' in request.data:
#             TempArtist.objects.filter(id=tempartist.id).delete()
#             return Response(status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)

# def updateArtist(artist, request):
#     if 'name' in request.data:
#         artist.name=request.data['name']
#     if 'firstname' in request.data:
#         artist.firstname=request.data['firstname']
#     if 'lastname' in request.data:
#         artist.lastname=request.data['lastname']
#     if 'biography' in request.data:
#         artist.biography=request.data['biography']
#     if 'birthday' in request.data:
#         artist.birthday=request.data['birthday']
#     if 'gender' in request.data:
#         artist.gender=request.data['gender']
#     if 'avatar' in request.data:
#         artist.avatar=request.data['avatar']
#     if 'occupation' in request.data:
#         artist.occupation.clear()
#         arr = str(request.data['occupation']).split(',')
#         for item in arr:
#             artist.occupation.add(int(item))
#     if 'cast' in request.data:
#         cast = request.data['cast']
#         for work in cast:
#             film = work['film']
#             role_name = work['role_name']
#             film_obj = Film.objects.get(pk=int(film['id']))
#             actor = Actor.objects.create(artist=artist, role_name=role_name)
#             film_obj.movie.actors.add(actor)
#     artist.save()
#     return artist

# def copyArtist(artist, temp):
#     artist.firstname=temp.firstname
#     artist.lastname=temp.lastname
#     artist.biography=temp.biography
#     artist.birthday=temp.birthday
#     artist.gender=temp.gender
#     artist.avatar=temp.avatar
#     artist.occupation.clear()
#     for o in temp.occupation.all():
#         artist.occupation.add(o)
#     artist.save()
#     return artist
