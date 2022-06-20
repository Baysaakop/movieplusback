from django.http import Http404
from django.db.models import Q, Count
from rest_framework import status, pagination
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from users.serializers import UserSerializer
from .models import (
    Artist, Genre, Series, Tag, Theater, Review,
    Platform, Movie, Rating, Production,
    Occupation, CastMember, CrewMember
)
from .serializers import (
    ReviewSerializer, GenreSerializer, TagSerializer, PlatformSerializer, RatingSerializer, ProductionSerializer,
    OccupationSerializer, CastMemberSerializer, CrewMemberSerializer
)
from rest_framework import viewsets


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all().order_by('-created_at')

    def get_queryset(self):
        queryset = Review.objects.all().order_by('-created_at')
        film = self.request.query_params.get('film', None)
        series = self.request.query_params.get('series', None)
        if film is not None:
            film = Movie.objects.get(id=int(film))
            queryset = film.reviews.all().order_by('-created_at')
        if series is not None:
            series = Series.objects.get(id=int(series))
            queryset = series.reviews.all().order_by('-created_at')
        return queryset

    def create(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.data['token']).user
        spoiler = False
        if request.data['is_spoiler'] == "true":
            spoiler = True
        review = Review.objects.create(
            user=user,
            title=request.data['title'],
            is_spoiler=spoiler,
            comment=request.data['comment'],
        )
        if 'film' in request.data:
            film = Movie.objects.get(id=int(request.data['film']))
            film.reviews.add(review)
        if 'series' in request.data:
            series = Series.objects.get(id=int(request.data['series']))
            series.reviews.add(review)
        review.save()
        serializer = ReviewSerializer(review)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        review = self.get_object()
        user = Token.objects.get(key=request.data['token']).user
        if 'is_spoiler' in request.data:
            if request.data['is_spoiler'] == "true":
                review.is_spoiler = True
            else:
                review.is_spoiler = False
        if 'title' in request.data:
            review.title = request.data['title']
        if 'comment' in request.data:
            review.comment = request.data['comment']
        if 'like' in request.data:
            if review in user.profile.reviews_liked.all():
                user.profile.reviews_liked.remove(review)
                review.like_count -= 1
            else:
                user.profile.reviews_liked.add(review)
                review.like_count += 1
            user.profile.save()
            review.save()
            serializer = ReviewSerializer(review)
            user_serializer = UserSerializer(user)
            headers = self.get_success_headers(serializer.data)
            return Response({'review': serializer.data, 'user': user_serializer.data}, status=status.HTTP_200_OK, headers=headers)
        if 'dislike' in request.data:
            if review in user.profile.reviews_disliked.all():
                user.profile.reviews_disliked.remove(review)
                review.dislike_count -= 1
            else:
                user.profile.reviews_disliked.add(review)
                review.dislike_count += 1
            user.profile.save()
            review.save()
            serializer = ReviewSerializer(review)
            user_serializer = UserSerializer(user)
            headers = self.get_success_headers(serializer.data)
            return Response({'review': serializer.data, 'user': user_serializer.data}, status=status.HTTP_200_OK, headers=headers)
        # if 'edit' in request.data:
        #     if user == comment.user:
        #         comment.comment = request.data['comment']
        #     else:
        #         return Response(None, status=status.HTTP_403_FORBIDDEN)
        review.save()
        serializer = ReviewSerializer(review)
        user = UserSerializer(user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


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


class PlatformViewSet(viewsets.ModelViewSet):
    serializer_class = PlatformSerializer
    queryset = Platform.objects.all().order_by('name')


class MemberPagination(pagination.PageNumberPagination):
    page_size = 100


class CastMemberViewSet(viewsets.ModelViewSet):
    serializer_class = CastMemberSerializer
    queryset = CastMember.objects.all().order_by('-created_by')
    pagination_class = MemberPagination

    def get_queryset(self):
        queryset = CastMember.objects.all().order_by('-created_by')
        film = self.request.query_params.get('film', None)
        series = self.request.query_params.get('series', None)
        artist = self.request.query_params.get('artist', None)
        is_lead = self.request.query_params.get('is_lead', None)
        type = self.request.query_params.get('type', None)
        if film is not None:
            queryset = queryset.filter(
                film__id=int(film))
        if series is not None:
            queryset = queryset.filter(
                series__id=int(series))
        if artist is not None:
            queryset = queryset.filter(
                artist__id=int(artist))
        if is_lead is not None:
            if is_lead == 'true':
                queryset = queryset.filter(is_lead=True)
            else:
                queryset = queryset.filter(is_lead=False)
        if type is not None:
            if type == "film":
                queryset = queryset.filter(
                    film__isnull=False)
            if type == "series":
                queryset = queryset.filter(series__isnull=False)
        return queryset

    def create(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.data['token']).user
        artist = Artist.objects.get(id=int(request.data['artist']))
        member = CastMember.objects.create(
            artist=artist,
            created_by=user
        )
        if 'film' in request.data:
            film = Movie.objects.get(id=int(request.data['film']))
            member.film = film
        if 'series' in request.data:
            series = Series.objects.get(id=int(request.data['series']))
            member.series = series
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
    pagination_class = MemberPagination

    def get_queryset(self):
        queryset = CrewMember.objects.all().order_by('film__id')
        film = self.request.query_params.get('film', None)
        series = self.request.query_params.get('series', None)
        artist = self.request.query_params.get('artist', None)
        type = self.request.query_params.get('type', None)
        if film is not None:
            queryset = queryset.filter(
                film__id=int(film))
        if series is not None:
            queryset = queryset.filter(
                series__id=int(series))
        if artist is not None:
            queryset = queryset.filter(
                artist__id=int(artist))
        if type is not None:
            if type == "film":
                queryset = queryset.filter(
                    film__isnull=False)
            if type == "series":
                queryset = queryset.filter(series__isnull=False)
        return queryset

    def create(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.data['token']).user
        artist = Artist.objects.get(id=int(request.data['artist']))
        member = CrewMember.objects.create(
            artist=artist,
            created_by=user
        )
        if 'film' in request.data:
            film = Movie.objects.get(id=int(request.data['film']))
            member.film = film
        if 'series' in request.data:
            series = Series.objects.get(id=int(request.data['series']))
            member.series = series
        if 'roles' in request.data:
            arr = str(request.data['roles']).split(',')
            for item in arr:
                member.roles.add(int(item))
        member.save()
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
        member.save()
        serializer = CrewMemberSerializer(member)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
