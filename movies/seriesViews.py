import string
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Series, Rating, Genre
from .serializers import SeriesSerializer
from rest_framework import viewsets


class SeriesViewSet(viewsets.ModelViewSet):
    serializer_class = SeriesSerializer
    queryset = Series.objects.all().order_by('-created_at')

    def get_queryset(self):
        queryset = Series.objects.all().order_by('-created_at')
        title = self.request.query_params.get('title', None)
        search = self.request.query_params.get('search', None)
        genre = self.request.query_params.get('genre', None)
        yearfrom = self.request.query_params.get('yearfrom', None)
        yearto = self.request.query_params.get('yearto', None)
        scorefrom = self.request.query_params.get('scorefrom', None)
        scoreto = self.request.query_params.get('scoreto', None)
        order = self.request.query_params.get('order', None)
        if title is not None:
            queryset = queryset.filter(Q(title__icontains=title) | Q(
                title__icontains=string.capwords(title))).distinct()
        if search is not None:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(title__icontains=string.capwords(search)) |
                Q(tags__name__icontains=search) |
                Q(tags__name__icontains=string.capwords(search))).distinct()
        if genre is not None:
            queryset = queryset.filter(genres__id=genre).distinct()
        if yearfrom is not None:
            queryset = queryset.filter(
                releasedate__year__gte=yearfrom).distinct()
        if yearto is not None:
            queryset = queryset.filter(
                releasedate__year__lte=yearto).distinct()
        if scorefrom is not None:
            queryset = queryset.filter(avg_score__gte=scorefrom).distinct()
        if scoreto is not None:
            queryset = queryset.filter(avg_score__lte=scoreto).distinct()
        if order is not None:
            queryset = queryset.order_by(order).distinct()
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count = instance.view_count + 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.data['token']).user
        series = Series.objects.create(
            title=request.data['title'],
            created_by=user
        )
        updateSeries(series, request)
        serializer = SeriesSerializer(series)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        series = self.get_object()
        user = Token.objects.get(key=request.data['token']).user
        # if 'comment' in request.data:
        #     comment = request.data['comment']
        #     comment_obj = Comment.objects.create(
        #         user=user,
        #         comment=comment
        #     )
        #     movie.comments.add(comment_obj)
        # else:
        series.updated_by = user
        updateSeries(series, request)
        serializer = SeriesSerializer(series)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


def updateSeries(series, request):
    if 'title' in request.data:
        series.title = request.data['title']
    if 'plot' in request.data:
        series.plot = request.data['plot']
    if 'seasons' in request.data:
        series.seasons = request.data['seasons']
    if 'episodes' in request.data:
        series.episodes = request.data['episodes']
    if 'duration' in request.data:
        series.duration = request.data['duration']
    if 'releasedate' in request.data:
        series.releasedate = request.data['releasedate']
    if 'trailer' in request.data:
        series.trailer = request.data['trailer']
    if 'poster' in request.data:
        series.poster = request.data['poster']
    if 'landscape' in request.data:
        series.landscape = request.data['landscape']
    if 'is_released' in request.data:
        if request.data['is_released'] == "true":
            series.is_released = True
        else:
            series.is_released = False
    if 'on_tv' in request.data:
        if request.data['on_tv'] == "true":
            series.on_tv = True
        else:
            series.on_tv = False
    if 'rating' in request.data:
        rating = Rating.objects.get(id=int(request.data['rating']))
        series.rating = rating
    if 'productions' in request.data:
        series.productions.clear()
        productions = request.data['productions'].split(",")
        for item in productions:
            series.productions.add(int(item))
    if 'genres' in request.data:
        series.genres.clear()
        genres = request.data['genres'].split(",")
        for item in genres:
            series.genres.add(int(item))
    if 'tags' in request.data:
        series.tags.clear()
        tags = request.data['tags'].split(",")
        for item in tags:
            series.tags.add(int(item))
    if 'theaters' in request.data:
        series.theaters.clear()
        theaters = request.data['theaters'].split(",")
        for item in theaters:
            series.theaters.add(int(item))
    if 'platforms' in request.data:
        series.platforms.clear()
        platforms = request.data['platforms'].split(",")
        for item in platforms:
            series.platforms.add(int(item))
    if 'comments' in request.data:
        series.platforms.clear()
        platforms = request.data['platforms'].split(",")
        for item in platforms:
            series.platforms.add(int(item))
    series.save()
    return series
