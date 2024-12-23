# Generated by Django 5.0.8 on 2024-12-23 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bounty', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bounty',
            name='tier',
            field=models.CharField(choices=[('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV'), ('V', 'V')], default='I', max_length=3),
        ),
    ]
