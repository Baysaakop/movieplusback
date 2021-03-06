import string
from django.http import Http404
from django.db.models import Q, Count
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Movie, Platform, PlatformUrl, Rating, Genre, Theater, TheaterUrl
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
        length = self.request.query_params.get('length', None)
        user = self.request.query_params.get('user', None)
        action = self.request.query_params.get('action', None)
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
        if user is not None and action is not None:
            user_obj = User.objects.get(pk=int(user))
            list = []
            if action == "watched":
                for item in reversed(user_obj.profile.films_watched.all()):
                    list.append(item.film)
            elif action == "liked":
                for film in reversed(user_obj.profile.films_liked.all()):
                    list.append(film)
            elif action == "watchlist":
                for film in reversed(user_obj.profile.films_watchlist.all()):
                    list.append(film)
            elif action == "scores":
                for score in reversed(user_obj.profile.film_scores.all()):
                    list.append(score.film)
            elif action == "scoresFromTop":
                for score in user_obj.profile.film_scores.all().order_by('-user_score'):
                    list.append(score.film)
            elif action == "scoresFromBot":
                for score in user_obj.profile.film_scores.all().order_by('user_score'):
                    list.append(score.film)
            queryset = list
        if order is not None:
            queryset = queryset.order_by(order).distinct()
        if length is not None:
            queryset = queryset[0:int(length)]
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
    if 'theater' in request.data:
        theater = Theater.objects.get(id=int(request.data['theater']))
        if 'delete' in request.data:
            theaterurl = movie.theaters.filter(theater=theater)[0]
            movie.theater.remove(theaterurl)
        else:
            theaterurl = TheaterUrl.objects.create(
                theater=theater,
                url=request.data['url']
            )
            movie.theaters.add(theaterurl)
    if 'platform' in request.data:
        platform = Platform.objects.get(id=int(request.data['platform']))
        if 'delete' in request.data:
            platformurl = movie.platforms.filter(platform=platform)[0]
            movie.platforms.remove(platformurl)
        else:
            platformurl = PlatformUrl.objects.create(
                platform=platform,
                url=request.data['url']
            )
            movie.platforms.add(platformurl)
    movie.save()
    return movie
