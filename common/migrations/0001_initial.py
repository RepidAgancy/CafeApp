# Generated by Django 4.2 on 2024-11-08 06:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('total_price', models.DecimalField(decimal_places=3, default=0.0, max_digits=10)),
                ('is_confirm', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'savat',
                'verbose_name_plural': 'savatlar',
            },
        ),
        migrations.CreateModel(
            name='CategoryFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='common/category/image/%Y/%m/%d')),
                ('name', models.CharField(max_length=50)),
                ('name_en', models.CharField(max_length=50, null=True)),
                ('name_uz', models.CharField(max_length=50, null=True)),
                ('name_ru', models.CharField(max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'kategoriya',
                'verbose_name_plural': 'kategoriylar',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number', models.IntegerField(default=0, unique=True)),
                ('type', models.CharField(choices=[('band', 'band'), ('band emas', 'band emas')], default='band emas', max_length=20)),
            ],
            options={
                'verbose_name': 'stol',
                'verbose_name_plural': 'stollar',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('jarayonda', 'jarayonda'), ('bajarildi', 'bajarildi')], default='jarayonda', max_length=20)),
                ('is_confirm', models.BooleanField(default=False)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='common.cart')),
            ],
            options={
                'verbose_name': 'taom buyurtma',
                'verbose_name_plural': 'taom buyurtmalar',
            },
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('name_en', models.CharField(max_length=50, null=True)),
                ('name_uz', models.CharField(max_length=50, null=True)),
                ('name_ru', models.CharField(max_length=50, null=True)),
                ('image', models.ImageField(upload_to='common/food/image/%Y/%m/%d')),
                ('price', models.DecimalField(decimal_places=3, max_digits=10)),
                ('food_info', models.TextField()),
                ('food_info_en', models.TextField(null=True)),
                ('food_info_uz', models.TextField(null=True)),
                ('food_info_ru', models.TextField(null=True)),
                ('food_composition', models.TextField()),
                ('food_composition_en', models.TextField(null=True)),
                ('food_composition_uz', models.TextField(null=True)),
                ('food_composition_ru', models.TextField(null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food', to='common.categoryfood')),
            ],
            options={
                'verbose_name': 'toam',
                'verbose_name_plural': 'toamlar',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='common.cart')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='common.food')),
            ],
            options={
                'verbose_name': 'savatdagi taom',
                'verbose_name_plural': 'savatdagi taomlar',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.table'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
    ]
