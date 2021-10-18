from rest_framework.generics import get_object_or_404
from movies.models import Movie
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Author, Article, Category, Comment, Review
from .serializers import (
    AuthorSerializer, CategorySerializer, CommentSerializer,
    ArticleSerializer, ReviewSerializer
)
from rest_framework import viewsets, filters
# from users.models import Score
# from users.views import calculateScore


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('name')


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all().order_by('-follow_count')


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all().order_by('-created_at')

    def get_queryset(self):
        queryset = Comment.objects.all().order_by('-created_at')
        article = self.request.query_params.get('article', None)
        review = self.request.query_params.get('review', None)
        if article is not None:
            article = Article.objects.get(id=int(article))
            queryset = article.comments.all().order_by('-created_at')
        if review is not None:
            review = Review.objects.get(id=int(review))
            queryset = review.comments.all().order_by('-created_at')
        return queryset

    def create(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.data['token']).user
        comment = Comment.objects.create(
            user=user,
            comment=request.data['comment'],
        )
        if 'article' in request.data:
            article = Article.objects.get(id=int(request.data['article']))
            article.comments.add(comment)
        if 'review' in request.data:
            review = Review.objects.get(id=int(request.data['review']))
            review.comments.add(comment)
        comment.save()
        serializer = CommentSerializer(comment)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        user = Token.objects.get(key=request.data['token']).user
        if 'like' in request.data:
            if user in comment.likers.all():
                comment.likers.remove(user)
            else:
                comment.likers.add(user)
        if 'dislike' in request.data:
            if user in comment.dislikers.all():
                comment.dislikers.remove(user)
            else:
                comment.dislikers.add(user)
        if 'edit' in request.data:
            if user == comment.user:
                comment.comment = request.data['comment']
            else:
                return Response(None, status=status.HTTP_403_FORBIDDEN)
        comment.save()
        serializer = CommentSerializer(comment)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.order_by('-created_at')

    def get_queryset(self):
        # queryset = Article.objects.filter(
        #     approved=True).order_by('-created_at')
        queryset = Article.objects.order_by('-created_at')
        author = self.request.query_params.get('author', None)
        title = self.request.query_params.get('title', None)
        # waiting = self.request.query_params.get('waiting', None)
        if author is not None:
            user = User.objects.get(id=int(author))
            queryset = queryset.filter(author=user)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        # if waiting is not None:
        #     queryset = Article.objects.filter(
        #         approved=False).order_by('-created_at')
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count = instance.view_count + 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.data['token']).user
        article = Article.objects.create(
            author=user,
            title=request.data['title']
        )
        updateArticle(article, request)
        # user.profile.articles_count += 1
        # user.profile.save()
        serializer = ArticleSerializer(article)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        article = self.get_object()
        # user = Token.objects.get(key=request.data['token']).user
        if 'approved' in request.data:
            article.approved = True
            article.author.profile.article_count += 1
            article.author.profile.save()
        updateArticle(article, request)
        serializer = ArticleSerializer(article)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


# class ReviewViewSet(viewsets.ModelViewSet):
#     serializer_class = ReviewSerializer
#     queryset = Review.objects.filter(
#         approved=True).order_by('-like_count', '-created_at')

#     def get_queryset(self):
#         queryset = Review.objects.filter(
#             approved=True).order_by('-like_count', '-created_at')
#         author = self.request.query_params.get('author', None)
#         film = self.request.query_params.get('film', None)
#         title = self.request.query_params.get('title', None)
#         waiting = self.request.query_params.get('waiting', None)
#         if author is not None:
#             user = User.objects.get(id=int(author))
#             queryset = queryset.filter(author=user)
#         if film is not None:
#             film = Movie.objects.get(id=int(film))
#             queryset = queryset.filter(film=film)
#         if title is not None:
#             queryset = queryset.filter(title__icontains=title)
#         if waiting is not None:
#             queryset = Review.objects.filter(
#                 approved=False).order_by('-created_at')
#         return queryset

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.view_count = instance.view_count + 1
#         instance.save()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         user = Token.objects.get(key=request.data['token']).user
#         film = Movie.objects.get(id=int(request.data['film']))
#         review = Review.objects.create(
#             author=user,
#             film=film
#         )
#         updateArticle(review, request)
#         serializer = ReviewSerializer(review)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def update(self, request, *args, **kwargs):
#         review = self.get_object()
#         # user = Token.objects.get(key=request.data['token']).user
#         if 'approved' in request.data:
#             review.approved = True
#             review.author.profile.reviews_count += 1
#             review.author.profile.save()
#         updateArticle(review, request)
#         serializer = ReviewSerializer(review)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


def updateArticle(article, request):
    if 'title' in request.data:
        article.title = request.data['title']
    if 'outline' in request.data:
        article.outline = request.data['outline']
    if 'content' in request.data:
        article.content = request.data['content']
    if 'thumbnail' in request.data:
        article.thumbnail = request.data['thumbnail']
    article.save()
    return article
