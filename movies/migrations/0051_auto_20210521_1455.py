# Generated by Django 3.1.4 on 2021-05-21 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0050_auto_20210521_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempactor',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tempmember',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
    ]
