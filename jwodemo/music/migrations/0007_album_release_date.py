# Generated by Django 5.0 on 2024-03-27 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0006_album_review_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='release_date',
            field=models.CharField(default='2001', max_length=4),
            preserve_default=False,
        ),
    ]
