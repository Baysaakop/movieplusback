# Generated by Django 3.1.4 on 2021-04-21 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0016_auto_20210421_1049'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='likes',
            new_name='check_count',
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='views',
            new_name='comment_count',
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='watched',
            new_name='like_count',
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='watchlist',
            new_name='view_count',
        ),
        migrations.AddField(
            model_name='movie',
            name='watchlist_count',
            field=models.IntegerField(default=0),
        ),
    ]
