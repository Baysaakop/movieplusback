# Generated by Django 3.1.4 on 2021-10-09 08:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0065_auto_20210907_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('plot', models.TextField(blank=True, null=True)),
                ('seasons', models.IntegerField(default=1)),
                ('episodes', models.IntegerField(default=10)),
                ('duration', models.IntegerField(default=30)),
                ('releasedate', models.DateField(blank=True, null=True)),
                ('view_count', models.IntegerField(default=0)),
                ('like_count', models.IntegerField(default=0)),
                ('watched_count', models.IntegerField(default=0)),
                ('watchlist_count', models.IntegerField(default=0)),
                ('score_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('avg_score', models.IntegerField(default=0)),
                ('poster', models.ImageField(blank=True, null=True, upload_to='movies/%Y/%m/%d')),
                ('landscape', models.ImageField(blank=True, null=True, upload_to='movies/%Y/%m/%d')),
                ('trailer', models.CharField(blank=True, max_length=200, null=True)),
                ('is_released', models.BooleanField(default=True)),
                ('on_tv', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('comments', models.ManyToManyField(blank=True, null=True, related_name='series_comments', to='movies.Comment')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='series_created_by', to=settings.AUTH_USER_MODEL)),
                ('genres', models.ManyToManyField(blank=True, null=True, to='movies.Genre')),
                ('platforms', models.ManyToManyField(blank=True, null=True, to='movies.Platform')),
                ('productions', models.ManyToManyField(blank=True, null=True, to='movies.Production')),
                ('rating', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='movies.rating')),
                ('tags', models.ManyToManyField(blank=True, null=True, to='movies.Tag')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='series_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='castmember',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.series'),
        ),
        migrations.AddField(
            model_name='crewmember',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.series'),
        ),
    ]
