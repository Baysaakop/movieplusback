# Generated by Django 3.1.4 on 2021-05-10 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0036_auto_20210510_1327'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempFilm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(default=1)),
                ('movie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
            ],
        ),
    ]
