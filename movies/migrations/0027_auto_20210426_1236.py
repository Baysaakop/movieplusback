# Generated by Django 3.1.4 on 2021-04-26 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0026_comment_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='actors',
            field=models.ManyToManyField(blank=True, null=True, related_name='movie_actors', to='movies.Actor'),
        ),
    ]
