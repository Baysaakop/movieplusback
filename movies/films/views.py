import string
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from movies.models import Movie, Platform, PlatformUrl, Rating
from .serializers import MovieListSerializer, MovieDetailSerializer
from rest_framework import viewsets


class MovieListViewSet(viewsets.ModelViewSet):
    serializer_class = MovieListSerializer
    queryset = Movie.objects.all().order_by('-created_at')

    def get_queryset(self):
        queryset = Movie.objects.all().order_by('-created_at')
        search = self.request.query_params.get('search', None)
        genre = self.request.query_params.get('genre', None)
        decade = self.request.query_params.get('decade', None)
        year = self.request.query_params.get('year', None)
        scoreto = self.request.query_params.get('scoreto', None)
        order = self.request.query_params.get('order', None)
        if search is not None:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(title__icontains=string.capwords(search)) |
                Q(tags__name__icontains=search) |
                Q(tags__name__icontains=string.capwords(search))).distinct()
        if genre is not None:
            queryset = queryset.filter(genres__id=genre).distinct()
        if decade is not None:
            queryset = queryset.filter(
                Q(releasedate__year__gte=int(decade)) &
                Q(releasedate__year__lt=int(decade)+10)).distinct()
        if year is not None:
            queryset = queryset.filter(releasedate__year=year).distinct()
        if scoreto is not None:
            queryset = queryset.filter(
                Q(avg_score__gte=int(scoreto)-20) &
                Q(avg_score__lt=int(scoreto))).distinct()
        if order is not None:
            queryset = queryset.order_by(order).distinct()
        return queryset


class MovieDetailViewSet(viewsets.ModelViewSet):
    serializer_class = MovieDetailSerializer
    queryset = Movie.objects.all().order_by('-created_at')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count = instance.view_count + 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
