from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Genre, Rating, Production, Occupation, Artist, Movie, CastMember, CrewMember
# from users.models import User, Profile
# from users.serializers import UserSerializer


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'description', 'count')


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
    occupation = OccupationSerializer(read_only=True, many=True)

    class Meta:
        model = Artist
        fields = ('id', 'name', 'firstname', 'lastname', 'biography', 'birthdate', 'gender', 'avatar', 'occupation',
                  'view_count', 'like_count', 'follow_count', 'facebook_channel', 'instagram_channel', 'twitter_channel', 'youtube_channel',
                  'created_by', 'created_at', 'updated_by', 'updated_at')


class MovieSerializer(serializers.ModelSerializer):
    rating = RatingSerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    production = ProductionSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'plot', 'duration',
                  'releasedate', 'rating', 'genre', 'production',
                  'view_count', 'like_count', 'watched_count', 'watchlist_count', 'score_count', 'comment_count', 'avg_score',
                  'poster', 'landscape', 'trailer', 'is_released', 'is_playing',
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
    role = OccupationSerializer(read_only=True, many=True)

    class Meta:
        model = CrewMember
        fields = ('id', 'artist', 'film', 'role', 'created_by',
                  'created_at', 'updated_by', 'updated_at')
