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

# class Score(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     score = models.IntegerField(default=0)

# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment = models.TextField()
#     score = models.IntegerField(default=0)
#     likes = models.ManyToManyField(User, null=True, blank=True, related_name="comment_likes")
#     dislikes = models.ManyToManyField(User, null=True, blank=True, related_name="comment_dislikes")
#     created_at = models.DateTimeField(auto_now_add=True)

# class Review(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     title = models.CharField(max_length=100)
#     content = RichTextField()
#     thumbnail = models.ImageField(upload_to='review/%Y/%m/%d', null=True, blank=True)
#     score = models.IntegerField(default=0)
#     views = models.IntegerField(default=0)
#     likes = models.ManyToManyField(User, related_name="review_likes", null=True, blank=True)
#     dislikes = models.ManyToManyField(User, related_name="review_dislikes", null=True, blank=True)
#     comments = models.ManyToManyField(Comment, null=True, blank=True, related_name="review_comments")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title


class Artist(models.Model):
    name = models.CharField(max_length=100)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    biography = RichTextField(null=True, blank=True)
    birthdate = models.DateField(auto_now=False, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    occupation = models.ManyToManyField(Occupation)
    avatar = models.ImageField(
        upload_to='artists/%Y/%m/%d', null=True, blank=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    follow_count = models.IntegerField(default=0)
    facebook_channel = models.CharField(max_length=200, blank=True, null=True)
    instagram_channel = models.CharField(max_length=200, blank=True, null=True)
    twitter_channel = models.CharField(max_length=200, blank=True, null=True)
    youtube_channel = models.CharField(max_length=200, blank=True, null=True)
    # likes = models.ManyToManyField(
    #     User, null=True, blank=True, related_name="artist_likes")
    # follows = models.ManyToManyField(
    #     User, null=True, blank=True, related_name="artist_follows")
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='artist_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='artist_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField(null=True, blank=True)
    plot = models.TextField(null=True, blank=True)
    duration = models.IntegerField(default=90)
    releasedate = models.DateField(auto_now=False, null=True, blank=True)
    rating = models.ForeignKey(
        Rating, on_delete=models.SET_NULL, null=True, blank=True)
    genre = models.ManyToManyField(Genre, null=True, blank=True)
    production = models.ManyToManyField(Production, null=True, blank=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    # likes = models.ManyToManyField(
    #     User, null=True, blank=True, related_name="movie_likes")
    # checks = models.ManyToManyField(
    #     User, null=True, blank=True, related_name="movie_checks")
    # watchlists = models.ManyToManyField(
    #     User, null=True, blank=True, related_name="movie_watchlists")
    # scores = models.ManyToManyField(
    #     Score, null=True, blank=True, related_name="movie_scores")
    # comments = models.ManyToManyField(
    #     Comment, null=True, blank=True, related_name="movie_comments")
    # members = models.ManyToManyField(Member, null=True, blank=True, related_name="movie_members")
    # actors = models.ManyToManyField(Actor, null=True, blank=True, related_name="movie_actors")
    score = models.IntegerField(default=0)
    poster = models.ImageField(
        upload_to='movies/%Y/%m/%d', null=True, blank=True)
    landscape = models.ImageField(
        upload_to='movies/%Y/%m/%d', null=True, blank=True)
    trailer = models.CharField(max_length=200, null=True, blank=True)
    is_released = models.BooleanField(default=True)
    is_playing = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='movie_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='movie_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title


class CastMember(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    film = models.ForeignKey(
        Movie, on_delete=models.CASCADE, null=True, blank=True)
    is_lead = models.BooleanField(default=False)
    role_name = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cast_member_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cast_member_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.artist.name + " - " + self.film.title


class CrewMember(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    film = models.ForeignKey(
        Movie, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ManyToManyField(Occupation, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='crew_member_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='crew_member_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.artist.name + " - " + self.film.title
