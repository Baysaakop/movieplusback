# Generated by Django 3.1.4 on 2021-04-11 10:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0011_review_score'),
        ('users', '0006_auto_20210331_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='critic_followed',
            field=models.ManyToManyField(blank=True, null=True, related_name='critic_followed', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='critic_likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='critic_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='review_likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='review_likes', to='movies.Review'),
        ),
    ]
