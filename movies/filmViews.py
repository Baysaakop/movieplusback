from django.http import Http404
from django.db.models import Q, Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Movie
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


# def calculateScore(item):
#     total = 0
#     if (item.scores.count() == 0):
#         return 0
#     for obj in item.scores.all():
#         total = total + obj.score
#     average = int((total * 10) / item.scores.count())
#     return average


# def action(movie, request):
#     user = Token.objects.get(key=request.data['token']).user
#     if 'like' in request.data:
#         if user in movie.likes.all():
#             movie.likes.remove(user)
#         else:
#             movie.likes.add(user)
#     if 'check' in request.data:
#         if user in movie.checks.all():
#             movie.checks.remove(user)
#         else:
#             movie.checks.add(user)
#     if 'watchlist' in request.data:
#         if user in movie.watchlists.all():
#             movie.watchlists.remove(user)
#         else:
#             movie.watchlists.add(user)
#     if 'score' in request.data:
#         score = int(request.data['score'])
#         user_score = movie.scores.filter(user=user).first()
#         if user_score is None:
#             user_score = Score.objects.create(
#                 user=user,
#                 score=score
#             )
#             movie.scores.add(user_score)
#         else:
#             if score == 0:
#                 movie.scores.remove(user_score)
#                 Score.objects.filter(id=user_score.id).delete()
#             else:
#                 user_score.score = score
#                 user_score.save()
#         movie.score = calculateScore(movie)
#     movie.save()
#     return movie


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all().order_by('-created_at')

    def get_queryset(self):
        queryset = Movie.objects.all().order_by('-created_at')
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name).distinct()
        return queryset


# class FilmViewSet(viewsets.ModelViewSet):
#     serializer_class = FilmSerializer
#     queryset = Film.objects.all()

#     def get_queryset(self):
#         queryset = Film.objects.all().order_by('-movie__created_at')
#         name = self.request.query_params.get('name', None)
#         genre = self.request.query_params.get('genre', None)
#         yearfrom = self.request.query_params.get('yearfrom', None)
#         yearto = self.request.query_params.get('yearto', None)
#         member = self.request.query_params.get('member', None)
#         actor = self.request.query_params.get('actor', None)
#         user = self.request.query_params.get('user', None)
#         state = self.request.query_params.get('state', None)
#         order = self.request.query_params.get('order', None)
#         movie = self.request.query_params.get('movie', None)
#         queryset = filter(queryset, name, genre, yearfrom,
#                           yearto, member, actor, user, state, order, movie)
#         return queryset

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.movie.views = instance.movie.views + 1
#         instance.movie.save()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

#     def update(self, request, *args, **kwargs):
#         film = self.get_object()
#         action(film.movie, request)
#         serializer = FilmSerializer(film)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

#     def destroy(self, request, *args, **kwargs):
#         try:
#             instance = self.get_object()
#             movie = instance.movie
#             self.perform_destroy(instance)
#             Movie.objects.filter(id=movie.id).delete()
#         except Http404:
#             pass
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class TempFilmViewSet(viewsets.ModelViewSet):
#     serializer_class = TempFilmSerializer
#     queryset = TempFilm.objects.all().order_by('-movie__created_at')

#     def get_queryset(self):
#         queryset = TempFilm.objects.all().order_by('-movie__created_at')
#         filmid = self.request.query_params.get('filmid', None)
#         if filmid is not None:
#             if filmid == '0':
#                 queryset = TempFilm.objects.filter(
#                     filmid=0).order_by('movie__created_at')
#             else:
#                 queryset = TempFilm.objects.filter(
#                     ~Q(filmid=0)).order_by('movie__created_at')
#         return queryset

#     def create(self, request, *args, **kwargs):
#         user = Token.objects.get(key=request.data['token']).user
#         tempfilm = None
#         # CREATE
#         if 'filmid' not in request.data:
#             movie = Movie.objects.create(
#                 name=request.data['name'],
#                 created_by=user
#             )
#             updateMovie(movie, request)
#             tempfilm = TempFilm.objects.create(movie=movie)
#         # UPDATE
#         else:
#             film = Film.objects.get(pk=int(request.data['filmid']))
#             movie = Movie.objects.create(
#                 name=film.movie.name,
#                 updated_by=user
#             )
#             copyMovie(movie, film.movie)
#             updateMovie(movie, request)
#             tempfilm = TempFilm.objects.create(movie=movie, filmid=film.id)
#         serializer = TempFilmSerializer(tempfilm)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def update(self, request, *args, **kwargs):
#         tempfilm = self.get_object()
#         if 'accept' in request.data:
#             # CREATE
#             if tempfilm.filmid == 0:
#                 film = Film.objects.create(movie=tempfilm.movie)
#                 TempFilm.objects.filter(id=tempfilm.id).delete()
#                 return Response(status=status.HTTP_200_OK)
#             # UPDATE
#             else:
#                 film = Film.objects.get(pk=tempfilm.filmid)
#                 film.movie.name = tempfilm.movie.name
#                 film.movie.updated_by = tempfilm.movie.updated_by
#                 copyMovie(film.movie, tempfilm.movie)
#                 TempFilm.objects.filter(id=tempfilm.id).delete()
#                 Movie.objects.filter(id=tempfilm.movie.id).delete()
#                 return Response(status=status.HTTP_200_OK)
#         elif 'decline' in request.data:
#             TempFilm.objects.filter(id=tempfilm.id).delete()
#             Movie.objects.filter(id=tempfilm.movie.id).delete()
#             return Response(status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# def updateMovie(movie, request):
#     if 'name' in request.data:
#         movie.name = request.data['name']
#     if 'description' in request.data:
#         movie.description = request.data['description']
#     if 'plot' in request.data:
#         movie.plot = request.data['plot']
#     if 'duration' in request.data:
#         movie.duration = request.data['duration']
#     if 'releasedate' in request.data:
#         movie.releasedate = request.data['releasedate']
#     if 'trailer' in request.data:
#         movie.trailer = request.data['trailer']
#     if 'poster' in request.data:
#         movie.poster = request.data['poster']
#     if 'landscape' in request.data:
#         movie.landscape = request.data['landscape']
#     if 'is_released' in request.data:
#         if request.data['is_released'] == "true":
#             movie.is_released = True
#         else:
#             movie.is_released = False
#     if 'is_playing' in request.data:
#         if request.data['is_playing'] == "true":
#             movie.is_playing = True
#         else:
#             movie.is_playing = False
#     if 'rating' in request.data:
#         rating = Rating.objects.get(id=int(request.data['rating']))
#         movie.rating = rating
#     if 'genre' in request.data:
#         movie.genre.clear()
#         genres = request.data['genre'].split(",")
#         for item in genres:
#             movie.genre.add(int(item))
#     movie.save()
#     return movie


# def copyMovie(movie, temp):
#     movie.description = temp.description
#     movie.plot = temp.plot
#     movie.trailer = temp.trailer
#     movie.duration = temp.duration
#     movie.releasedate = temp.releasedate
#     movie.releasedate = temp.releasedate
#     movie.is_released = temp.is_released
#     movie.is_playing = temp.is_playing
#     movie.poster = temp.poster
#     movie.landscape = temp.landscape
#     movie.rating = temp.rating
#     movie.genre.clear()
#     for g in temp.genre.all():
#         movie.genre.add(g)
#     movie.production.clear()
#     for p in temp.production.all():
#         movie.production.add(p)
#     movie.save()
#     return movie
