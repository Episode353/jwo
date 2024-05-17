# Generated by Django 5.0 on 2024-05-06 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_profile_coin_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('position', models.PositiveIntegerField()),
            ],
        ),
    ]