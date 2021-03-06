# Generated by Django 3.1.4 on 2021-05-12 03:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0039_auto_20210510_1841'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempArtist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('firstname', models.CharField(blank=True, max_length=50, null=True)),
                ('lastname', models.CharField(blank=True, max_length=50, null=True)),
                ('biography', models.TextField(blank=True, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='artists/%Y/%m/%d')),
                ('views', models.IntegerField(default=0)),
                ('is_accepted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tempartist_created_by', to=settings.AUTH_USER_MODEL)),
                ('follows', models.ManyToManyField(blank=True, null=True, related_name='tempartist_follows', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, null=True, related_name='tempartist_likes', to=settings.AUTH_USER_MODEL)),
                ('occupation', models.ManyToManyField(to='movies.Occupation')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tempartist_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
