# Generated by Django 3.1.4 on 2021-09-08 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20210908_0933'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='like_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
