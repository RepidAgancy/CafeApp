# Generated by Django 5.1.3 on 2024-11-22 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='type',
            field=models.CharField(choices=[('kirim', 'kirim'), ('chiqim', 'chiqim')], default='chiqim', max_length=250),
        ),
    ]