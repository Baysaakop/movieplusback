# Generated by Django 3.1.4 on 2021-10-11 03:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djrichtextfield.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0067_auto_20211009_1643'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('comment', djrichtextfield.models.RichTextField()),
                ('score', models.IntegerField(default=0)),
                ('like_count', models.IntegerField(default=0)),
                ('dislike_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='comment_count',
            new_name='review_count',
        ),
        migrations.RenameField(
            model_name='series',
            old_name='comment_count',
            new_name='review_count',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='series',
            name='comments',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.AddField(
            model_name='movie',
            name='reviews',
            field=models.ManyToManyField(blank=True, null=True, related_name='film_reviews', to='movies.Review'),
        ),
        migrations.AddField(
            model_name='series',
            name='reviews',
            field=models.ManyToManyField(blank=True, null=True, related_name='series_reviews', to='movies.Review'),
        ),
    ]
