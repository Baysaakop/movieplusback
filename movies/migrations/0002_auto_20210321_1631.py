# Generated by Django 3.1.4 on 2021-03-21 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='updated_by',
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(blank=True, null=True, to='movies.Genre'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='members',
            field=models.ManyToManyField(blank=True, null=True, to='movies.Member'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='production',
            field=models.ManyToManyField(blank=True, null=True, to='movies.Production'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='rating',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.rating'),
        ),
    ]
