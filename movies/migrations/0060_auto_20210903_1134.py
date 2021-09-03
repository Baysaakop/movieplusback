# Generated by Django 3.1.4 on 2021-09-03 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0059_auto_20210902_1414'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='score',
            new_name='avg_score',
        ),
        migrations.AddField(
            model_name='movie',
            name='score_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='watched_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='watchlist_count',
            field=models.IntegerField(default=0),
        ),
    ]
