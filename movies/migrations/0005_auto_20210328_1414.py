# Generated by Django 3.1.4 on 2021-03-28 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_artist_gender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='members',
            new_name='member',
        ),
        migrations.RemoveField(
            model_name='member',
            name='role_name',
        ),
        migrations.CreateModel(
            name='Cast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(blank=True, max_length=100, null=True)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.artist')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='cast',
            field=models.ManyToManyField(blank=True, null=True, to='movies.Cast'),
        ),
    ]
