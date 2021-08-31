from django.http import Http404
from django.db.models import Q, Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Artist, Genre, Movie, Rating, Production, Occupation, CastMember, CrewMember
from .serializers import (
    GenreSerializer, RatingSerializer, ProductionSerializer, OccupationSerializer, CastMemberSerializer, CrewMemberSerializer
)
from rest_framework import viewsets


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all().order_by('name')


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all().order_by('name')


class ProductionViewSet(viewsets.ModelViewSet):
    serializer_class = ProductionSerializer
    queryset = Production.objects.all().order_by('name')


class OccupationViewSet(viewsets.ModelViewSet):
    serializer_class = OccupationSerializer
    queryset = Occupation.objects.all().order_by('name')


class CastMemberViewSet(viewsets.ModelViewSet):
    serializer_class = CastMemberSerializer
    queryset = CastMember.objects.all().order_by('film__id')

    def get_queryset(self):
        queryset = CastMember.objects.all().order_by('film__id')
        film = self.request.query_params.get('film', None)
        artist = self.request.query_params.get('artist', None)
        if film is not None:
            queryset = queryset.filter(
                film__id=int(film))
        if artist is not None:
            queryset = queryset.filter(
                artist__id=int(artist))
        return queryset


class CrewMemberViewSet(viewsets.ModelViewSet):
    serializer_class = CrewMemberSerializer
    queryset = CrewMember.objects.all().order_by('film__id')

    def get_queryset(self):
        queryset = CrewMember.objects.all().order_by('film__id')
        film = self.request.query_params.get('film', None)
        artist = self.request.query_params.get('artist', None)
        if film is not None:
            queryset = queryset.filter(
                film__id=int(film))
        if artist is not None:
            queryset = queryset.filter(
                artist__id=int(artist))
        return queryset

# class ScoreViewSet(viewsets.ModelViewSet):
#     serializer_class = ScoreSerializer
#     queryset = Score.objects.all()

# class ReviewViewSet(viewsets.ModelViewSet):
#     serializer_class = ReviewSerializer
#     queryset = Review.objects.all().order_by('-created_at')

#     def get_queryset(self):
#         queryset = Review.objects.all().order_by('-created_at')
#         title = self.request.query_params.get('title', None)
#         order = self.request.query_params.get('order', None)
#         if title is not None:
#             queryset = queryset.filter(title__icontains=title)
#         if order is not None:
#             if (order == 'created_at'):
#                 queryset = queryset.order_by('-created_at')
#             elif (order == 'title'):
#                 queryset = queryset.order_by('title')
#             elif (order == 'views'):
#                 queryset = queryset.order_by('-views')
#             elif (order == 'likes'):
#                 queryset = queryset.annotate(likes_count=Count('likes')).order_by('-likes_count')
#             elif (order == 'dislikes'):
#                 queryset = queryset.annotate(dislikes_count=Count('dislikes')).order_by('-dislikes_count')
#             elif (order == 'comments'):
#                 queryset = queryset.annotate(comments_count=Count('comments')).order_by('-comments_count')
#         return queryset

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.views = instance.views + 1
#         instance.save()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         user = Token.objects.get(key=request.data['token']).user
#         title = request.data['title']
#         content = request.data['content']
#         thumbnail = request.data['thumbnail']
#         review = Review.objects.create(
#             user=user,
#             title=title,
#             thumbnail=thumbnail,
#             content=content
#         )
#         if 'movie' in request.data:
#             movie = Movie.objects.get(id=int(request.data['movie']))
#             review.movie = movie
#         if 'score' in request.data:
#             review.score = int(request.data['score'])
#         review.save()
#         serializer = ReviewSerializer(review)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def update(self, request, *args, **kwargs):
#         review = self.get_object()
#         user = Token.objects.get(key=request.data['token']).user
#         if 'title' in request.data:
#             review.title = request.data['title']
#         if 'thumbnail' in request.data:
#             review.thumbnail = request.data['thumbnail']
#         if 'content' in request.data:
#             review.content = request.data['content']
#         if 'score' in request.data:
#             review.score = request.data['score']
#         if 'movie' in request.data:
#             movie = Movie.objects.get(id=int(request.data['movie']))
#             review.movie = movie
#         if 'like' in request.data:
#             if user in review.likes.all():
#                 review.likes.remove(user)
#             else:
#                 review.likes.add(user)
#         if 'dislike' in request.data:
#             if user in review.dislikes.all():
#                 review.dislikes.remove(user)
#             else:
#                 review.dislikes.add(user)
#         review.save()
#         serializer = ReviewSerializer(review)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

# class MemberViewSet(viewsets.ModelViewSet):
#     serializer_class = MemberSerializer
#     queryset = Member.objects.all().order_by('artist__id')

# class SeriesViewSet(viewsets.ModelViewSet):
#     serializer_class = SeriesSerializer
#     queryset = Series.objects.all()

# def calculateScore(item):
#     total = 0
#     if (item.scores.count() == 0):
#         return 0
#     for obj in item.scores.all():
#         total = total + obj.score
#     average = int((total * 10) / item.scores.count())
#     return average
