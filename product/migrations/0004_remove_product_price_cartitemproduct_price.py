# Generated by Django 4.2 on 2024-12-10 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_categoryproduct_image_alter_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.AddField(
            model_name='cartitemproduct',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
