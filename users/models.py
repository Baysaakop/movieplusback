from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from movies.models import Artist, Movie, Series, Review
from articles.models import Article

USER_ROLES = (
    ("1", "admin"),
    ("2", "moderator"),
    ("3", "user"),
)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/<id>/<filename>
    return 'users/{0}/{1}'.format(instance.user.id, filename)


class FilmScore(models.Model):
    film = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user_score = models.IntegerField(default=0)


class SeriesScore(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    user_score = models.IntegerField(default=0)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    birthday = models.DateField(null=True, blank=True)
    # User lists
    following = models.ManyToManyField(
        User, related_name="following", null=True, blank=True)
    followers = models.ManyToManyField(
        User, related_name="followers", null=True, blank=True)
    # Artist lists
    artists_liked = models.ManyToManyField(
        Artist, related_name="artists_liked", null=True, blank=True)
    artists_followed = models.ManyToManyField(
        Artist, related_name="artists_followed", null=True, blank=True)
    # Film lists
    films_liked = models.ManyToManyField(
        Movie, related_name="films_liked", null=True, blank=True)
    films_watched = models.ManyToManyField(
        Movie, related_name="films_watched", null=True, blank=True)
    films_watchlist = models.ManyToManyField(
        Movie, related_name="films_watchlist", null=True, blank=True)
    film_scores = models.ManyToManyField(FilmScore, null=True, blank=True)
    # Series lists
    series_liked = models.ManyToManyField(
        Series, related_name="series_liked", null=True, blank=True)
    series_watched = models.ManyToManyField(
        Series, related_name="series_watched", null=True, blank=True)
    series_watchlist = models.ManyToManyField(
        Series, related_name="series_watchlist", null=True, blank=True)
    series_scores = models.ManyToManyField(SeriesScore, null=True, blank=True)
    # Review lists
    reviews_liked = models.ManyToManyField(
        Review, related_name="reviews_liked", null=True, blank=True)
    reviews_disliked = models.ManyToManyField(
        Review, related_name="reviews_disliked", null=True, blank=True)
    facebook_channel = models.CharField(max_length=200, blank=True, null=True)
    instagram_channel = models.CharField(max_length=200, blank=True, null=True)
    twitter_channel = models.CharField(max_length=200, blank=True, null=True)
    youtube_channel = models.CharField(max_length=200, blank=True, null=True)
    avatar = models.ImageField(
        upload_to=user_directory_path, null=True, blank=True)
    role = models.CharField(max_length=20, choices=USER_ROLES, default="3")

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
