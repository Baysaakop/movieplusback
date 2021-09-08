from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Category, Author, Article, Comment, Review
from users.serializers import UserSerializer
from movies.serializers import MovieSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CommentSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'comment', 'likers',
                  'dislikers', 'created_at', 'updated_at')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'user', 'article_count',
                  'like_count', 'view_count', 'follow_count')


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'author', 'title', 'outline', 'content',
                  'thumbnail', 'categories', 'view_count', 'like_count',
                  'comments', 'featured', 'approved', 'created_at'
                  )


class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'author', 'film', 'title', 'outline', 'content',
                  'score', 'view_count', 'like_count', 'thumbnail',
                  'comments', 'approved', 'created_at'
                  )
