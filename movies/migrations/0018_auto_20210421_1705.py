# Generated by Django 3.1.4 on 2021-04-21 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0017_auto_20210421_1118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artist',
            old_name='followers',
            new_name='follow_count',
        ),
        migrations.RenameField(
            model_name='artist',
            old_name='likes',
            new_name='like_count',
        ),
        migrations.RenameField(
            model_name='artist',
            old_name='views',
            new_name='view_count',
        ),
    ]
