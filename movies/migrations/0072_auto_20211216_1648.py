# Generated by Django 3.1.4 on 2021-12-16 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0071_theater_background'),
    ]

    operations = [
        migrations.AddField(
            model_name='platform',
            name='background',
            field=models.CharField(default='#000', max_length=100),
        ),
        migrations.AlterField(
            model_name='platform',
            name='logo',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='theater',
            name='logo',
            field=models.CharField(default='', max_length=100),
        ),
    ]
