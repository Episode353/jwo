# Generated by Django 5.0 on 2024-05-06 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_todo_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='progress',
            field=models.CharField(blank=True, max_length=2),
        ),
    ]
