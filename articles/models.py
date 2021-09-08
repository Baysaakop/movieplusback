from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie
from djrichtextfield.models import RichTextField


def article_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/items/<id>/<filename>
    return 'articles/{0}/{1}'.format(instance.id, filename)


class Author(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    article_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    follow_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="article_comment_user")
    comment = models.TextField(null=True, blank=True)
    likers = models.ManyToManyField(
        User, null=True, blank=True, related_name="article_comment_likers")
    dislikers = models.ManyToManyField(
        User, null=True, blank=True, related_name="article_comment_dislikers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    outline = models.TextField(blank=True)
    content = RichTextField()
    thumbnail = models.ImageField(
        upload_to=article_directory_path, null=True, blank=True)
    categories = models.ManyToManyField(Category, null=True, blank=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    comments = models.ManyToManyField(Comment, null=True, blank=True)
    featured = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Movie, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    outline = models.TextField(blank=True)
    content = RichTextField()
    thumbnail = models.ImageField(
        upload_to=article_directory_path, null=True, blank=True)
    score = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    comments = models.ManyToManyField(Comment, null=True, blank=True)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
