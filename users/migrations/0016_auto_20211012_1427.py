# Generated by Django 3.1.4 on 2021-10-12 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0069_review_is_spoiler'),
        ('users', '0015_profile_series_scores'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='series_liked',
            field=models.ManyToManyField(related_name='series_liked', to='movies.Series'),
        ),
        migrations.AddField(
            model_name='profile',
            name='series_watched',
            field=models.ManyToManyField(related_name='series_watched', to='movies.Series'),
        ),
        migrations.AddField(
            model_name='profile',
            name='series_watchlist',
            field=models.ManyToManyField(related_name='series_watchlist', to='movies.Series'),
        ),
    ]
