# Generated by Django 3.1.4 on 2021-05-08 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0031_auto_20210508_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='movie',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
    ]
