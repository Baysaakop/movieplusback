from django.http import Http404
from django.db.models import Q, Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import (
    Artist, Genre, Tag, Theater, Comment,
    Platform, Movie, Rating, Production,
    Occupation, CastMember, CrewMember
)
from .serializers import (
    CommentSerializer, GenreSerializer, TagSerializer, TheaterSerializer,
    PlatformSerializer, RatingSerializer, ProductionSerializer,
    OccupationSerializer, CastMemberSerializer, CrewMemberSerializer
)
from rest_framework import viewsets


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all().order_by('-created_at')

    def get_queryset(self):
        queryset = Comment.objects.all().order_by('-created_at')
        film = self.request.query_params.get('film', None)
        if film is not None:
            film = Movie.objects.get(id=int(film))
            queryset = film.comments.all().order_by('-created_at')
        return queryset

    def create(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.data['token']).user
        comment = Comment.objects.create(
            user=user,
            comment=request.data['comment'],
        )
        if 'film' in request.data:
            film = Movie.objects.get(id=int(request.data['film']))
            film.comments.add(comment)
        comment.save()
        serializer = CommentSerializer(comment)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def update(self, request, *args, **kwargs):
    #     member = self.get_object()
    #     user = Token.objects.get(key=request.data['token']).user
    #     if 'is_lead' in request.data:
    #         if request.data['is_lead'] == "true":
    #             member.is_lead = True
    #         else:
    #             member.is_lead = False
    #     if 'role_name' in request.data:
    #         member.role_name = request.data['role_name']
    #     member.updated_by = user
    #     member.save()
    #     serializer = CastMemberSerializer(member)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all().order_by('name')


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all().order_by('name')


class ProductionViewSet(viewsets.ModelViewSet):
    serializer_class = ProductionSerializer
    queryset = Production.objects.all().order_by('name')


class OccupationViewSet(viewsets.ModelViewSet):
    serializer_class = OccupationSerializer
    queryset = Occupation.objects.all().order_by('name')


class CastMemberViewSet(viewsets.ModelViewSet):
    serializer_class = CastMemberSerializer
    queryset = CastMember.objects.all().order_by('film__id')

    def get_queryset(self):
        queryset = CastMember.objects.all().order_by('film__id')
        film = self.request.query_params.get('film', None)
        artist = self.request.query_params.get('artist', None)
        if film is not None:
            queryset = queryset.filter(
                film__id=int(film))
        if artist is not None:
            queryset = queryset.filter(
                artist__id=int(artist))
        return queryset

    def create(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.data['token']).user
        artist = Artist.objects.get(id=int(request.data['artist']))
        film = Movie.objects.get(id=int(request.data['film']))
        member = CastMember.objects.create(
            artist=artist,
            film=film,
            created_by=user
        )
        if 'is_lead' in request.data:
            member.is_lead = True
        if 'role_name' in request.data:
            member.role_name = request.data['role_name']
        member.save()
        serializer = CastMemberSerializer(member)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        member = self.get_object()
        user = Token.objects.get(key=request.data['token']).user
        if 'is_lead' in request.data:
            if request.data['is_lead'] == "true":
                member.is_lead = True
            else:
                member.is_lead = False
        if 'role_name' in request.data:
            member.role_name = request.data['role_name']
        member.updated_by = user
        member.save()
        serializer = CastMemberSerializer(member)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class CrewMemberViewSet(viewsets.ModelViewSet):
    serializer_class = CrewMemberSerializer
    queryset = CrewMember.objects.all().order_by('film__id')

    def get_queryset(self):
        queryset = CrewMember.objects.all().order_by('film__id')
        film = self.request.query_params.get('film', None)
        artist = self.request.query_params.get('artist', None)
        if film is not None:
            queryset = queryset.filter(
                film__id=int(film))
        if artist is not None:
            queryset = queryset.filter(
                artist__id=int(artist))
        return queryset

    def create(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.data['token']).user
        artist = Artist.objects.get(id=int(request.data['artist']))
        film = Movie.objects.get(id=int(request.data['film']))
        member = CrewMember.objects.create(
            artist=artist,
            film=film,
            created_by=user
        )
        if 'roles' in request.data:
            arr = str(request.data['roles']).split(',')
            for item in arr:
                member.roles.add(int(item))
        serializer = CrewMemberSerializer(member)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        member = self.get_object()
        user = Token.objects.get(key=request.data['token']).user
        if 'roles' in request.data:
            member.roles.clear()
            arr = str(request.data['roles']).split(',')
            for item in arr:
                member.roles.add(int(item))
        member.updated_by = user
        serializer = CrewMemberSerializer(member)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
