# Generated by Django 5.0 on 2024-03-27 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_remove_album_release_date_album_hours_album_minutes'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='review_body',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
