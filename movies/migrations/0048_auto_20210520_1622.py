# Generated by Django 3.1.4 on 2021-05-20 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0047_auto_20210520_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='film',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.film'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.series'),
        ),
        migrations.AlterField(
            model_name='member',
            name='film',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.film'),
        ),
        migrations.AlterField(
            model_name='member',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.series'),
        ),
        migrations.AlterField(
            model_name='tempactor',
            name='film',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.film'),
        ),
        migrations.AlterField(
            model_name='tempactor',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.series'),
        ),
        migrations.AlterField(
            model_name='tempmember',
            name='film',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.film'),
        ),
        migrations.AlterField(
            model_name='tempmember',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.series'),
        ),
    ]
