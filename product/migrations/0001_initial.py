# Generated by Django 4.2 on 2024-12-12 15:13

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
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('total_price', models.PositiveIntegerField(default=0)),
                ('is_confirm', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_products', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'savatdagi mahsulot',
                'verbose_name_plural': 'savatdagi mahsulotlar',
            },
        ),
        migrations.CreateModel(
            name='CategoryProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('name_en', models.CharField(max_length=100, null=True)),
                ('name_uz', models.CharField(max_length=100, null=True)),
                ('name_ru', models.CharField(max_length=100, null=True)),
                ('image', models.ImageField(upload_to='product/category/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('name_en', models.CharField(max_length=100, null=True)),
                ('name_uz', models.CharField(max_length=100, null=True)),
                ('name_ru', models.CharField(max_length=100, null=True)),
                ('image', models.ImageField(upload_to='product/product/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.categoryproduct')),
            ],
            options={
                'verbose_name': 'mahsulot',
                'verbose_name_plural': 'mahsulotlar',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_confirm', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('tasdiqlangan', 'tasdiqlangan'), ('tasdiqlanmagan', 'tasdiqlanmagan')], max_length=50)),
                ('type', models.CharField(choices=[('kirim', 'kirim'), ('chiqim', 'chiqim')], default='chiqim', max_length=250)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='product.cartproduct')),
            ],
            options={
                'verbose_name': 'Buyurtmadagi mahsulot',
                'verbose_name_plural': 'Buyurtmadagi mahsulotlar',
            },
        ),
        migrations.CreateModel(
            name='CartItemProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('weight', models.PositiveIntegerField(default=0)),
                ('unit_status', models.CharField(choices=[('kg', 'kg'), ('dona', 'dona')], max_length=100)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('price', models.PositiveIntegerField(default=0)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items_products', to='product.cartproduct')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items_products', to='product.product')),
            ],
            options={
                'verbose_name': 'savatdagi mahsulot dona',
                'verbose_name_plural': 'savatdagi mahsulotlar dona',
            },
        ),
    ]
