import string
from django.http import Http404
from django.db.models import Q, Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Movie, Rating, Genre
from .serializers import MovieSerializer
from rest_framework import viewsets


# def filter(queryset, name, genre, yearfrom, yearto, member, actor, user, state, order, movie):
#     if name is not None:
#         queryset = queryset.filter(movie__name__icontains=name).distinct()
#     if genre is not None:
#         queryset = queryset.filter(movie__genre__id=genre).distinct()
#     if yearfrom is not None:
#         queryset = queryset.filter(
#             movie__releasedate__year__gte=yearfrom).distinct()
#     if yearto is not None:
#         queryset = queryset.filter(
#             movie__releasedate__year__lte=yearto).distinct()
#     if member is not None:
#         queryset = queryset.filter(
#             movie__members__artist__id=member).distinct()
#     if actor is not None:
#         queryset = queryset.filter(movie__actors__artist__id=actor).distinct()
#     if user is not None and state is not None:
#         if state == 'like':
#             queryset = queryset.filter(movie__likes__id=user).distinct()
#         elif state == 'check':
#             queryset = queryset.filter(movie__checks__id=user).distinct()
#         elif state == 'watchlist':
#             queryset = queryset.filter(movie__watchlists__id=user).distinct()
#         elif state == 'score':
#             queryset = queryset.filter(movie__scores__user__id=user).distinct()
#     if movie is not None:
#         queryset = queryset.filter(movie__id=movie).distinct()
#     if order is not None:
#         if (order == 'created_at'):
#             queryset = queryset.order_by('-movie__created_at')
#         elif (order == 'releasedate'):
#             queryset = queryset.order_by('-movie__releasedate')
#         elif (order == 'duration'):
#             queryset = queryset.order_by('-movie__duration')
#         elif (order == 'name'):
#             queryset = queryset.order_by('movie__name')
#         elif (order == 'score'):
#             queryset = queryset.order_by('-movie__score')
#         elif (order == 'likes'):
#             queryset = queryset.annotate(likes_count=Count(
#                 'movie__likes')).order_by('-likes_count')
#         elif (order == 'checks'):
#             queryset = queryset.annotate(checks_count=Count(
#                 'movie__checks')).order_by('-checks_count')
#         elif (order == 'watchlists'):
#             queryset = queryset.annotate(watchlists_count=Count(
#                 'movie__watchlists')).order_by('-watchlists_count')
#         elif (order == 'views'):
#             queryset = queryset.order_by('-movie__views')
#     return queryset

class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all().order_by('-created_at')

    def get_queryset(self):
        queryset = Movie.objects.all().order_by('-created_at')
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(Q(title__icontains=title) | Q(
                title__icontains=string.capwords(title))).distinct()
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count = instance.view_count + 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.data['token']).user
        movie = Movie.objects.create(
            title=request.data['title'],
            created_by=user
        )
        updateMovie(movie, request)
        serializer = MovieSerializer(movie)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        movie = self.get_object()
        user = Token.objects.get(key=request.data['token']).user
        movie.updated_by = user
        updateMovie(movie, request)
        serializer = MovieSerializer(movie)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


def updateMovie(movie, request):
    if 'title' in request.data:
        movie.title = request.data['title']
    if 'description' in request.data:
        movie.description = request.data['description']
    if 'plot' in request.data:
        movie.plot = request.data['plot']
    if 'duration' in request.data:
        movie.duration = request.data['duration']
    if 'releasedate' in request.data:
        movie.releasedate = request.data['releasedate']
    if 'trailer' in request.data:
        movie.trailer = request.data['trailer']
    if 'poster' in request.data:
        movie.poster = request.data['poster']
    if 'landscape' in request.data:
        movie.landscape = request.data['landscape']
    if 'is_released' in request.data:
        if request.data['is_released'] == "true":
            movie.is_released = True
        else:
            movie.is_released = False
    if 'is_playing' in request.data:
        if request.data['is_playing'] == "true":
            movie.is_playing = True
        else:
            movie.is_playing = False
    if 'rating' in request.data:
        rating = Rating.objects.get(id=int(request.data['rating']))
        movie.rating = rating
    if 'genre' in request.data:
        movie.genre.clear()
        genres = request.data['genre'].split(",")
        for item in genres:
            movie.genre.add(int(item))
    movie.save()
    return movie
