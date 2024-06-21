# Generated by Django 5.0 on 2024-06-18 17:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worm', '0003_worm_time_of_death'),
    ]

    operations = [
        migrations.AddField(
            model_name='worm',
            name='badge',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
        ),
    ]
