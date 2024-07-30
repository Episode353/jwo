# Generated by Django 5.0 on 2024-07-29 21:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worm', '0006_worm_times_revived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worm',
            name='times_revived',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(9), django.core.validators.MinValueValidator(0)]),
        ),
    ]
