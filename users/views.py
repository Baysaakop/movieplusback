from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework import viewsets
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from .models import FilmDate, Profile, FilmScore, SeriesScore
from .serializers import UserSerializer, ProfileSerializer
from movies.models import Movie, Artist, Series
from movies.serializers import MovieSerializer, ArtistSerializer, SeriesSerializer
from articles.models import Review


def calculateFilmScore(film):
    scores = FilmScore.objects.filter(film=film)
    # if (scores.count() < 5):
    #     film.avg_score = 0
    #     return
    if (scores.count() == 0):
        film.avg_score = 0
        film.score_count = 0
        film.save()
        return
    sum = 0
    for item in scores:
        sum += item.user_score * 10
    avg = sum / scores.count()
    film.avg_score = round(avg)
    film.score_count = scores.count()
    film.save()


def calculateSeriesScore(series):
    scores = SeriesScore.objects.filter(series=series)
    if (scores.count() == 0):
        series.avg_score = 0
        series.score_count = 0
        series.save()
        return
    sum = 0
    for item in scores:
        sum += item.user_score * 10
    avg = sum / scores.count()
    series.avg_score = round(avg)
    series.score_count = scores.count()
    series.save()


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        film = None
        artist = None
        flag = True
        if 'username' in request.data:
            user.username = request.data['username']
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        if 'description' in request.data:
            user.profile.description = request.data['description']
        if 'phone_number' in request.data:
            user.profile.phone_number = request.data['phone_number']
        if 'facebook_channel' in request.data:
            user.profile.facebook_channel = request.data['facebook_channel']
        if 'instagram_channel' in request.data:
            user.profile.instagram_channel = request.data['instagram_channel']
        if 'twitter_channel' in request.data:
            user.profile.twitter_channel = request.data['twitter_channel']
        if 'youtube_channel' in request.data:
            user.profile.youtube_channel = request.data['youtube_channel']
        if 'avatar' in request.data and user:
            user.profile.avatar = request.data['avatar']
        # FOLLOW
        if 'follow' in request.data:
            target = User.objects.get(pk=int(request.data['user']))
            if target in user.profile.following.all():
                user.profile.following.remove(target)
                target.profile.followers.remove(user)
            else:
                user.profile.following.add(target)
                target.profile.followers.add(user)
            target.save()
        # FILM ACTIONS
        if 'film' in request.data:
            film_id = request.data['film']
            film = Movie.objects.get(id=int(film_id))
            if 'watched' in request.data:
                exists = False
                for item in user.profile.films_watched.all():
                    if item.film == film:
                        exists = True
                        user.profile.films_watched.remove(item)
                        FilmDate.objects.filter(id=item.id).delete()
                        film.watched_count -= 1
                        flag = False
                if exists is False:
                    obj = FilmDate.objects.create(film=film)
                    if 'date' in request.data:
                        date = request.data['date']
                        obj.date = date
                        obj.save()
                    user.profile.films_watched.add(obj)
                    film.watched_count += 1
            if 'like' in request.data:
                if film in user.profile.films_liked.all():
                    user.profile.films_liked.remove(film)
                    film.like_count -= 1
                    flag = False
                else:
                    user.profile.films_liked.add(film)
                    film.like_count += 1
            if 'watchlist' in request.data:
                if film in user.profile.films_watchlist.all():
                    user.profile.films_watchlist.remove(film)
                    film.watchlist_count -= 1
                    flag = False
                else:
                    user.profile.films_watchlist.add(film)
                    film.watchlist_count += 1
            if 'score' in request.data:
                score = int(request.data['score'])
                exists = False
                for item in user.profile.film_scores.all():
                    if item.film == film:
                        exists = True
                        if score > 0:
                            item.user_score = score
                            item.save()
                        else:
                            user.profile.film_scores.remove(item)
                            FilmScore.objects.filter(id=item.id).delete()
                            break
                if exists is False:
                    obj = FilmScore.objects.create(film=film, user_score=score)
                    user.profile.film_scores.add(obj)
                calculateFilmScore(film)
            film.save()
            user.save()
            serializer = UserSerializer(user)
            serializer_film = MovieSerializer(film)
            data = {
                'user': serializer.data,
                'film': serializer_film.data,
                'flag': flag
            }
            headers = self.get_success_headers(serializer.data)
            return Response(data, status=status.HTTP_200_OK, headers=headers)
        # SERIES ACTIONS
        if 'series' in request.data:
            series_id = request.data['series']
            series = Series.objects.get(id=int(series_id))
            if 'like' in request.data:
                if series in user.profile.series_liked.all():
                    user.profile.series_liked.remove(series)
                    series.like_count -= 1
                    flag = False
                else:
                    user.profile.series_liked.add(series)
                    series.like_count += 1
            if 'watched' in request.data:
                if series in user.profile.series_watched.all():
                    user.profile.series_watched.remove(series)
                    series.watched_count -= 1
                    flag = False
                else:
                    user.profile.series_watched.add(series)
                    series.watched_count += 1
            if 'watchlist' in request.data:
                if series in user.profile.series_watchlist.all():
                    user.profile.series_watchlist.remove(series)
                    series.watchlist_count -= 1
                    flag = False
                else:
                    user.profile.series_watchlist.add(series)
                    series.watchlist_count += 1
            if 'score' in request.data:
                score = int(request.data['score'])
                exists = False
                for item in user.profile.series_scores.all():
                    if item.series == series:
                        exists = True
                        if score > 0:
                            item.user_score = score
                            item.save()
                        else:
                            user.profile.series_scores.remove(item)
                            SeriesScore.objects.filter(id=item.id).delete()
                            break
                if exists is False:
                    obj = SeriesScore.objects.create(
                        series=series, user_score=score)
                    user.profile.series_scores.add(obj)
                calculateSeriesScore(series)
            series.save()
            user.save()
            serializer = UserSerializer(user)
            serializer_series = SeriesSerializer(series)
            data = {
                'user': serializer.data,
                'series': serializer_series.data,
                'flag': flag
            }
            headers = self.get_success_headers(serializer.data)
            return Response(data, status=status.HTTP_200_OK, headers=headers)
        # ARTIST ACTIONS
        if 'like_artist' in request.data:
            artist_id = request.data['artist']
            artist = Artist.objects.get(id=int(artist_id))
            if artist in user.profile.artists_liked.all():
                user.profile.artists_liked.remove(artist)
                artist.like_count -= 1
            else:
                user.profile.artists_liked.add(artist)
                artist.like_count += 1
            artist.save()
        if 'follow_artist' in request.data:
            artist_id = request.data['artist']
            artist = Artist.objects.get(id=int(artist_id))
            if artist in user.profile.artists_followed.all():
                user.profile.artists_followed.remove(artist)
                artist.follow_count -= 1
            else:
                user.profile.artists_followed.add(artist)
                artist.follow_count += 1
            artist.save()
        user.save()
        serializer = UserSerializer(user)
        serializer_film = MovieSerializer(film)
        serializer_artist = ArtistSerializer(artist)
        data = {
            'user': serializer.data,
            'film': serializer_film.data,
            'artist': serializer_artist.data
        }
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_200_OK, headers=headers)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    callback_url = 'http://localhost:3000/'
    client_class = OAuth2Client


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:3000/'
    client_class = OAuth2Client
