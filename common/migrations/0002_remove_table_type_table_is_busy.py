# Generated by Django 4.2 on 2024-11-14 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='type',
        ),
        migrations.AddField(
            model_name='table',
            name='is_busy',
            field=models.BooleanField(default=False),
        ),
    ]
