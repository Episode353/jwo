# Generated by Django 5.0 on 2024-06-11 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worm', '0002_worm_last_fed_worm_last_played_worm_last_slept'),
    ]

    operations = [
        migrations.AddField(
            model_name='worm',
            name='time_of_death',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
