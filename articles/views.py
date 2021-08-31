from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Author, Article, Category
from .serializers import AuthorSerializer, ArticleSerializer, CategorySerializer
from rest_framework import viewsets, filters


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('name')


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all().order_by('-follow_count')


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all().order_by('-created_at')

    # def create(self, request, *args, **kwargs):
    #     user = Token.objects.get(key=request.data['token']).user
    #     post = Post.objects.create(
    #         title=request.data['title'],
    #         created_by=user
    #     )
    #     if 'content' in request.data:
    #         post.content = request.data['content']
    #     if 'thumbnail' in request.data:
    #         post.thumbnail = request.data['thumbnail']
    #     post.save()
    #     serializer = PostSerializer(post)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def update(self, request, *args, **kwargs):
    #     post = self.get_object()
    #     user = Token.objects.get(key=request.data['token']).user
    #     post.updated_by = user
    #     if 'title' in request.data:
    #         post.title = request.data['title']
    #     if 'content' in request.data:
    #         post.content = request.data['content']
    #     if 'thumbnail' in request.data:
    #         post.thumbnail = request.data['thumbnail']
    #     post.save()
    #     serializer = PostSerializer(post)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
