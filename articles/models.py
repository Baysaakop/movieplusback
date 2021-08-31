from django.db import models
from django.contrib.auth.models import User
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


class Article(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = RichTextField()
    thumbnail = models.ImageField(
        upload_to=article_directory_path, null=True, blank=True)
    category = models.ManyToManyField(Category)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()
    article = models.ForeignKey(
        Article, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " - " + self.article.title
