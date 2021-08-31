from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Category, Author, Article
from users.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'user', 'article_count',
                  'like_count', 'view_count', 'follow_count')


class ArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'author', 'title', 'content',
                  'thumbnail', 'created_at')
