# Generated by Django 5.0 on 2024-05-06 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_todo_progress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='progress',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]