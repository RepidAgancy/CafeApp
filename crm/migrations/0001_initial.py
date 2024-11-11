# Generated by Django 4.2 on 2024-11-11 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=250)),
                ('profession', models.CharField(blank=True, max_length=250, null=True)),
                ('price', models.PositiveIntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Tolov',
                'verbose_name_plural': 'Tolovlar',
            },
        ),
    ]
