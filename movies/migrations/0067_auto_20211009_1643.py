# Generated by Django 3.1.4 on 2021-10-09 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0066_auto_20211009_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='landscape',
            field=models.ImageField(blank=True, null=True, upload_to='series/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='series',
            name='poster',
            field=models.ImageField(blank=True, null=True, upload_to='series/%Y/%m/%d'),
        ),
    ]
