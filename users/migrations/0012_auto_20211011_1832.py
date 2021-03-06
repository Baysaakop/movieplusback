# Generated by Django 3.1.4 on 2021-10-11 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0069_review_is_spoiler'),
        ('users', '0011_auto_20210908_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='reviews_disliked',
            field=models.ManyToManyField(related_name='reviews_disliked', to='movies.Review'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='reviews_liked',
            field=models.ManyToManyField(related_name='reviews_liked', to='movies.Review'),
        ),
    ]
