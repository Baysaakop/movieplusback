from re import T
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.utils.translation import gettext as _
from .models import Profile, FilmDate, FilmScore, SeriesScore


class FilmDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmDate
        fields = (
            'id', 'film', 'date'
        )


class FilmScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmScore
        fields = (
            'id', 'film', 'user_score'
        )


class SeriesScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeriesScore
        fields = (
            'id', 'series', 'user_score'
        )


class ProfileSerializer(serializers.ModelSerializer):
    films_watched = FilmDateSerializer(many=True)
    film_scores = FilmScoreSerializer(many=True)
    series_scores = SeriesScoreSerializer(many=True)

    class Meta:
        model = Profile
        read_only_fields = ('created_at', 'updated_at', 'role')
        exclude = ('user',)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'profile'
        )
