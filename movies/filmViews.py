import string
from django.http import Http404
from django.db.models import Q, Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Movie, Rating, Genre
from .serializers import MovieSerializer
from rest_framework import viewsets


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all().order_by('-created_at')

    def get_queryset(self):
        queryset = Movie.objects.all().order_by('-created_at')
        title = self.request.query_params.get('title', None)
        search = self.request.query_params.get('search', None)
        genre = self.request.query_params.get('genre', None)
        yearfrom = self.request.query_params.get('yearfrom', None)
        yearto = self.request.query_params.get('yearto', None)
        scorefrom = self.request.query_params.get('scorefrom', None)
        scoreto = self.request.query_params.get('scoreto', None)
        order = self.request.query_params.get('order', None)
        if title is not None:
            queryset = queryset.filter(Q(title__icontains=title) | Q(
                title__icontains=string.capwords(title))).distinct()
        if search is not None:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(title__icontains=string.capwords(search)) |
                Q(tags__name__icontains=search) |
                Q(tags__name__icontains=string.capwords(search))).distinct()
        if genre is not None:
            queryset = queryset.filter(genres__id=genre).distinct()
        if yearfrom is not None:
            queryset = queryset.filter(
                releasedate__year__gte=yearfrom).distinct()
        if yearto is not None:
            queryset = queryset.filter(
                releasedate__year__lte=yearto).distinct()
        if scorefrom is not None:
            queryset = queryset.filter(avg_score__gte=scorefrom).distinct()
        if scoreto is not None:
            queryset = queryset.filter(avg_score__lte=scoreto).distinct()
        if order is not None:
            queryset = queryset.order_by(order).distinct()
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
        # if 'comment' in request.data:
        #     comment = request.data['comment']
        #     comment_obj = Comment.objects.create(
        #         user=user,
        #         comment=comment
        #     )
        #     movie.comments.add(comment_obj)
        # else:
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
    if 'in_theater' in request.data:
        if request.data['in_theater'] == "true":
            movie.in_theater = True
        else:
            movie.in_theater = False
    if 'rating' in request.data:
        rating = Rating.objects.get(id=int(request.data['rating']))
        movie.rating = rating
    if 'productions' in request.data:
        movie.productions.clear()
        productions = request.data['productions'].split(",")
        for item in productions:
            movie.productions.add(int(item))
    if 'genres' in request.data:
        movie.genres.clear()
        genres = request.data['genres'].split(",")
        for item in genres:
            movie.genres.add(int(item))
    if 'tags' in request.data:
        movie.tags.clear()
        tags = request.data['tags'].split(",")
        for item in tags:
            movie.tags.add(int(item))
    if 'theaters' in request.data:
        movie.theaters.clear()
        theaters = request.data['theaters'].split(",")
        for item in theaters:
            movie.theaters.add(int(item))
    if 'platforms' in request.data:
        movie.platforms.clear()
        platforms = request.data['platforms'].split(",")
        for item in platforms:
            movie.platforms.add(int(item))
    movie.save()
    return movie
