# Generated by Django 3.1.4 on 2021-12-16 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0072_auto_20211216_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform',
            name='logo',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='theater',
            name='logo',
            field=models.CharField(default='', max_length=200),
        ),
    ]
