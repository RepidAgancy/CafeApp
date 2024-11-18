# Generated by Django 4.2 on 2024-11-18 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_alter_categoryfood_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryfood',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='categoryfood',
            name='name_en',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='categoryfood',
            name='name_ru',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='categoryfood',
            name='name_uz',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
