# Generated by Django 5.0 on 2024-03-27 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_remove_song_rank_song_tier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='release_date',
            field=models.CharField(max_length=6),
        ),
    ]
