from django.db import models
from django.contrib.auth.models import User
from djrichtextfield.models import RichTextField


class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Rating(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Production(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Occupation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_user")
    title = models.CharField(max_length=200)
    comment = RichTextField()
    is_spoiler = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ": " + self.title


class Artist(models.Model):
    name = models.CharField(max_length=100)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    biography = RichTextField(null=True, blank=True)
    birthdate = models.DateField(auto_now=False, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    occupations = models.ManyToManyField(Occupation)
    avatar = models.ImageField(
        upload_to='artists/%Y/%m/%d', null=True, blank=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    follow_count = models.IntegerField(default=0)
    facebook_channel = models.CharField(max_length=200, blank=True, null=True)
    instagram_channel = models.CharField(max_length=200, blank=True, null=True)
    twitter_channel = models.CharField(max_length=200, blank=True, null=True)
    youtube_channel = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='artist_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='artist_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Theater(models.Model):
    name = models.CharField(max_length=50)
    logo = models.CharField(max_length=200, default="")
    background = models.CharField(max_length=100, default="#000")

    def __str__(self):
        return self.name


class TheaterUrl(models.Model):
    url = models.CharField(max_length=200)
    theater = models.ForeignKey(
        Theater, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.url


class Platform(models.Model):
    name = models.CharField(max_length=50)
    logo = models.CharField(max_length=200, default="")
    background = models.CharField(max_length=100, default="#000")

    def __str__(self):
        return self.name


class PlatformUrl(models.Model):
    url = models.CharField(max_length=200)
    platform = models.ForeignKey(
        Platform, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.url


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField(null=True, blank=True)
    plot = models.TextField(null=True, blank=True)
    duration = models.IntegerField(default=90)
    releasedate = models.DateField(auto_now=False, null=True, blank=True)
    rating = models.ForeignKey(
        Rating, on_delete=models.SET_NULL, null=True, blank=True)
    genres = models.ManyToManyField(Genre, null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    productions = models.ManyToManyField(Production, null=True, blank=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    watched_count = models.IntegerField(default=0)
    watchlist_count = models.IntegerField(default=0)
    score_count = models.IntegerField(default=0)
    review_count = models.IntegerField(default=0)
    reviews = models.ManyToManyField(
        Review, null=True, blank=True, related_name="film_reviews")
    avg_score = models.IntegerField(default=0)
    poster = models.ImageField(
        upload_to='movies/%Y/%m/%d', null=True, blank=True)
    landscape = models.ImageField(
        upload_to='movies/%Y/%m/%d', null=True, blank=True)
    trailer = models.CharField(max_length=200, null=True, blank=True)
    is_released = models.BooleanField(default=True)
    in_theater = models.BooleanField(default=False)
    theaters = models.ManyToManyField(TheaterUrl, null=True, blank=True)
    platforms = models.ManyToManyField(PlatformUrl, null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='movie_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='movie_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title


class Series(models.Model):
    title = models.CharField(max_length=100)
    plot = models.TextField(null=True, blank=True)
    seasons = models.IntegerField(default=1)
    episodes = models.IntegerField(default=10)
    duration = models.IntegerField(default=30)
    releasedate = models.DateField(auto_now=False, null=True, blank=True)
    rating = models.ForeignKey(
        Rating, on_delete=models.SET_NULL, null=True, blank=True)
    genres = models.ManyToManyField(Genre, null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    productions = models.ManyToManyField(Production, null=True, blank=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    watched_count = models.IntegerField(default=0)
    watchlist_count = models.IntegerField(default=0)
    score_count = models.IntegerField(default=0)
    review_count = models.IntegerField(default=0)
    reviews = models.ManyToManyField(
        Review, null=True, blank=True, related_name="series_reviews")
    avg_score = models.IntegerField(default=0)
    poster = models.ImageField(
        upload_to='series/%Y/%m/%d', null=True, blank=True)
    landscape = models.ImageField(
        upload_to='series/%Y/%m/%d', null=True, blank=True)
    trailer = models.CharField(max_length=200, null=True, blank=True)
    is_released = models.BooleanField(default=True)
    on_tv = models.BooleanField(default=False)
    platforms = models.ManyToManyField(Platform, null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='series_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='series_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title


class CastMember(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    film = models.ForeignKey(
        Movie, on_delete=models.CASCADE, null=True, blank=True)
    series = models.ForeignKey(
        Series, on_delete=models.CASCADE, null=True, blank=True)
    is_lead = models.BooleanField(default=False)
    role_name = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cast_member_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cast_member_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        if self.series is not None:
            return self.series.title + " - " + self.artist.name
        return self.film.title + " - " + self.artist.name


class CrewMember(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    film = models.ForeignKey(
        Movie, on_delete=models.CASCADE, null=True, blank=True)
    series = models.ForeignKey(
        Series, on_delete=models.CASCADE, null=True, blank=True)
    roles = models.ManyToManyField(Occupation, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='crew_member_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='crew_member_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        if self.series is not None:
            return self.series.title + " - " + self.artist.name
        return self.film.title + " - " + self.artist.name
