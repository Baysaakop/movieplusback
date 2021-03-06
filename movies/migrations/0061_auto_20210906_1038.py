# Generated by Django 3.1.4 on 2021-09-06 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0060_auto_20210903_1134'),
    ]

    operations = [
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='platforms/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='Theater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='theaters/%Y/%m/%d')),
            ],
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='is_playing',
            new_name='in_theater',
        ),
        migrations.AddField(
            model_name='movie',
            name='platforms',
            field=models.ManyToManyField(blank=True, null=True, to='movies.Platform'),
        ),
        migrations.AddField(
            model_name='movie',
            name='theaters',
            field=models.ManyToManyField(blank=True, null=True, to='movies.Theater'),
        ),
    ]
