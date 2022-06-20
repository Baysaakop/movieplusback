from re import T
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from movies.models import Movie
from movies.serializers import RatingSerializer, GenreSerializer, ProductionSerializer
# from users.models import User, Profile
from users.serializers import UserSerializer


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'releasedate', 'score_count', 'avg_score', 'poster'
        )


class MovieDetailSerializer(serializers.ModelSerializer):
    rating = RatingSerializer(read_only=True)
    genres = GenreSerializer(read_only=True, many=True)
    productions = ProductionSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'description', 'plot', 'duration', 'releasedate',
            'rating', 'genres', 'tags', 'productions', 'poster', 'landscape',
            'view_count', 'like_count', 'watched_count', 'watchlist_count',
            'score_count', 'avg_score', 'trailer', 'is_released', 'in_theater',
            'created_by', 'created_at', 'updated_by', 'updated_at'
        )
