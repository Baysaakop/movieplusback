from re import T
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Genre, Tag, Theater, Platform, Rating, Production, Occupation, Artist, Comment, Movie, CastMember, CrewMember
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
        fields = ('id', 'name', 'logo')


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ('id', 'name', 'logo')


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


class CommentSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'comment', 'likers',
                  'dislikers', 'created_at', 'updated_at')


class MovieSerializer(serializers.ModelSerializer):
    rating = RatingSerializer(read_only=True)
    genres = GenreSerializer(read_only=True, many=True)
    theaters = TheaterSerializer(read_only=True, many=True)
    platforms = PlatformSerializer(read_only=True, many=True)
    productions = ProductionSerializer(read_only=True, many=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'description', 'plot', 'duration', 'releasedate',
            'rating', 'genres', 'tags', 'productions', 'theaters', 'platforms',
            'view_count', 'like_count', 'watched_count', 'watchlist_count',
            'score_count', 'comment_count', 'avg_score', 'poster', 'landscape',
            'trailer', 'is_released', 'in_theater', 'comments',
            'created_by', 'created_at', 'updated_by', 'updated_at'
        )


class CastMemberSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    film = MovieSerializer(read_only=True)

    class Meta:
        model = CastMember
        fields = ('id', 'artist', 'film', 'is_lead', 'role_name',
                  'created_by', 'created_at', 'updated_by', 'updated_at')


class CrewMemberSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    film = MovieSerializer(read_only=True)
    roles = OccupationSerializer(read_only=True, many=True)

    class Meta:
        model = CrewMember
        fields = ('id', 'artist', 'film', 'roles', 'created_by',
                  'created_at', 'updated_by', 'updated_at')
