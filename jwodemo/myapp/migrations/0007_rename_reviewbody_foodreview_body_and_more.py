# Generated by Django 5.0 on 2023-12-15 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_foodreview_reviewbody'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foodreview',
            old_name='reviewBody',
            new_name='Body',
        ),
        migrations.RenameField(
            model_name='foodreview',
            old_name='reviewDate',
            new_name='Date',
        ),
        migrations.RenameField(
            model_name='foodreview',
            old_name='reviewPhotoLink',
            new_name='PhotoLink',
        ),
        migrations.RenameField(
            model_name='foodreview',
            old_name='reviewlink',
            new_name='slug',
        ),
    ]
