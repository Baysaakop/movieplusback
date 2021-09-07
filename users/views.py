from .models import Profile, Score
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.response import Response
from .serializers import UserSerializer, ProfileSerializer
from rest_framework import viewsets
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings
from movies.models import Movie, Artist
from movies.serializers import MovieSerializer, ArtistSerializer


def calculateScore(film):
    scores = Score.objects.filter(film=film)
    # if (scores.count() < 5):
    #     film.avg_score = 0
    #     return
    if (scores.count() == 0):
        film.avg_score = 0
        return
    sum = 0
    for item in scores:
        sum += item.user_score
    avg = sum / scores.count() * 10
    film.avg_score = round(avg)


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
        if 'username' in request.data and user.username != request.data['username']:
            user.username = request.data['username']
        if 'first_name' in request.data and user.first_name != request.data['first_name']:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data and user.last_name != request.data['last_name']:
            user.last_name = request.data['last_name']
        if 'phone_number' in request.data and user.profile.phone_number != request.data['phone_number']:
            user.profile.phone_number = request.data['phone_number']
        if 'birth_date' in request.data and user.profile.birthday != request.data['birth_date']:
            user.profile.birthday = request.data['birth_date']
        if 'avatar' in request.data and user:
            user.profile.avatar = request.data['avatar']
        if 'like' in request.data:
            film_id = request.data['film']
            film = Movie.objects.get(id=int(film_id))
            if film in user.profile.films_liked.all():
                user.profile.films_liked.remove(film)
                film.like_count -= 1
            else:
                user.profile.films_liked.add(film)
                film.like_count += 1
            film.save()
        if 'watched' in request.data:
            film_id = request.data['film']
            film = Movie.objects.get(id=int(film_id))
            if film in user.profile.films_watched.all():
                user.profile.films_watched.remove(film)
                film.watched_count -= 1
            else:
                user.profile.films_watched.add(film)
                film.watched_count += 1
            film.save()
        if 'watchlist' in request.data:
            film_id = request.data['film']
            film = Movie.objects.get(id=int(film_id))
            if film in user.profile.films_watchlist.all():
                user.profile.films_watchlist.remove(film)
                film.watchlist_count -= 1
            else:
                user.profile.films_watchlist.add(film)
                film.watchlist_count += 1
            film.save()
        if 'score' in request.data:
            score = int(request.data['score'])
            film_id = request.data['film']
            film = Movie.objects.get(id=int(film_id))
            exists = False
            for item in user.profile.scores.all():
                if item.film == film:
                    exists = True
                    if score > 0:
                        item.user_score = score
                        item.save()
                    else:
                        user.profile.scores.remove(item)
                        Score.objects.filter(id=item.id).delete()
                        film.score_count -= 1
                        break
            if exists is False:
                obj = Score.objects.create(film=film, user_score=score)
                user.profile.scores.add(obj)
                film.score_count += 1
            calculateScore(film)
            film.save()
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
