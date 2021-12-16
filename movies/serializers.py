from re import T
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Genre, PlatformUrl, Tag, Theater, Platform, Rating, Production, Occupation, Artist, Review, Movie, Series, CastMember, CrewMember, TheaterUrl
# from users.models import User, Profile
from users.serializers import UserSerializer


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'description', 'count')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class TheaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = ('id', 'name', 'logo', 'background')


class TheaterUrlSerializer(serializers.ModelSerializer):
    theater = TheaterSerializer(read_only=True)

    class Meta:
        model = TheaterUrl
        fields = ('id', 'url', 'theater')


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ('id', 'name', 'logo', 'background')


class PlatformUrlSerializer(serializers.ModelSerializer):
    platform = PlatformSerializer(read_only=True)

    class Meta:
        model = PlatformUrl
        fields = ('id', 'url', 'platform')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'name', 'description', 'count')


class ProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Production
        fields = ('id', 'name', 'description', 'count')


class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        fields = ('id', 'name', 'description', 'count')


class ArtistSerializer(serializers.ModelSerializer):
    occupations = OccupationSerializer(read_only=True, many=True)

    class Meta:
        model = Artist
        fields = (
            'id', 'name', 'firstname', 'lastname', 'biography', 'birthdate',
            'gender', 'avatar', 'occupations', 'view_count', 'like_count',
            'follow_count', 'facebook_channel', 'instagram_channel',
            'twitter_channel', 'youtube_channel',
            'created_by', 'created_at', 'updated_by', 'updated_at'
        )


class ReviewSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'user', 'title', 'comment', 'is_spoiler', 'score',
                  'like_count', 'dislike_count', 'created_at', 'updated_at')


class MovieSerializer(serializers.ModelSerializer):
    rating = RatingSerializer(read_only=True)
    genres = GenreSerializer(read_only=True, many=True)
    theaters = TheaterUrlSerializer(read_only=True, many=True)
    platforms = PlatformUrlSerializer(read_only=True, many=True)
    productions = ProductionSerializer(read_only=True, many=True)
    # reviews = ReviewSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'description', 'plot', 'duration', 'releasedate',
            'rating', 'genres', 'tags', 'productions', 'theaters', 'platforms',
            'view_count', 'like_count', 'watched_count', 'watchlist_count',
            'score_count', 'review_count', 'avg_score', 'poster', 'landscape',
            'trailer', 'is_released', 'in_theater', 'reviews',
            'created_by', 'created_at', 'updated_by', 'updated_at'
        )


class SeriesSerializer(serializers.ModelSerializer):
    rating = RatingSerializer(read_only=True)
    genres = GenreSerializer(read_only=True, many=True)
    platforms = PlatformSerializer(read_only=True, many=True)
    productions = ProductionSerializer(read_only=True, many=True)
    reviews = ReviewSerializer(read_only=True, many=True)

    class Meta:
        model = Series
        fields = (
            'id', 'title', 'plot', 'seasons', 'episodes', 'duration', 'releasedate',
            'rating', 'genres', 'tags', 'productions', 'platforms',
            'view_count', 'like_count', 'watched_count', 'watchlist_count',
            'score_count', 'review_count', 'avg_score', 'poster', 'landscape',
            'trailer', 'is_released', 'on_tv', 'reviews',
            'created_by', 'created_at', 'updated_by', 'updated_at'
        )


class CastMemberSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    film = MovieSerializer(read_only=True)
    series = SeriesSerializer(read_only=True)

    class Meta:
        model = CastMember
        fields = ('id', 'artist', 'film', 'series', 'is_lead', 'role_name',
                  'created_by', 'created_at', 'updated_by', 'updated_at')


class CrewMemberSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    film = MovieSerializer(read_only=True)
    series = SeriesSerializer(read_only=True)
    roles = OccupationSerializer(read_only=True, many=True)

    class Meta:
        model = CrewMember
        fields = ('id', 'artist', 'film', 'series', 'roles', 'created_by',
                  'created_at', 'updated_by', 'updated_at')
