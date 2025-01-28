# Generated by Django 5.0.1 on 2025-01-28 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_todoitem_updated_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todoitem',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='todoitem',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
