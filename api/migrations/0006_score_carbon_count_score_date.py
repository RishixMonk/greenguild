# Generated by Django 4.2 on 2023-04-15 19:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_score_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='carbon_count',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='score',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
