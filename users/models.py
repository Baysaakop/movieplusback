from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from movies.models import Artist, Movie

USER_ROLES = (
    ("1", "admin"),
    ("2", "moderator"),
    ("3", "user"),
)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/<id>/<filename>
    return 'users/{0}/{1}'.format(instance.user.id, filename)


class Score(models.Model):
    film = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user_score = models.IntegerField(default=0)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    birthday = models.DateField(null=True, blank=True)
    artists_liked = models.ManyToManyField(
        Artist, related_name="artists_liked")
    artists_followed = models.ManyToManyField(
        Artist, related_name="artists_followed")
    films_liked = models.ManyToManyField(Movie, related_name="films_liked")
    films_watched = models.ManyToManyField(Movie, related_name="films_watched")
    films_watchlist = models.ManyToManyField(
        Movie, related_name="films_watchlist")
    scores = models.ManyToManyField(Score)
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
