# Generated by Django 4.2 on 2024-11-24 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('admin', 'admin'), ('ofitsant', 'ofitsant'), ('kassir', 'kassir'), ('omborchi', 'omborchi'), ('oshpaz', 'oshpaz')], max_length=50),
        ),
    ]
