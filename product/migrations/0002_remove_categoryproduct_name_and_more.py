# Generated by Django 4.2 on 2024-12-16 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoryproduct',
            name='name',
        ),
        migrations.RemoveField(
            model_name='categoryproduct',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='categoryproduct',
            name='name_ru',
        ),
        migrations.RemoveField(
            model_name='product',
            name='name',
        ),
        migrations.RemoveField(
            model_name='product',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='product',
            name='name_ru',
        ),
        migrations.AlterField(
            model_name='categoryproduct',
            name='name_uz',
            field=models.CharField(default='1', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='name_uz',
            field=models.CharField(default='1', max_length=100),
            preserve_default=False,
        ),
    ]