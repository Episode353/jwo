# Generated by Django 5.0 on 2023-12-15 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_rename_body_foodreview_linkhtml'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodreview',
            name='linkhtml',
        ),
        migrations.AddField(
            model_name='foodreview',
            name='html',
            field=models.TextField(blank=True, null=True),
        ),
    ]
