# Generated by Django 5.0 on 2024-07-26 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0023_alter_redeemcode_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redeemcode',
            name='code',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
