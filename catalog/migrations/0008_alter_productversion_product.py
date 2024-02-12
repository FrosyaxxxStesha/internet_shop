# Generated by Django 5.0 on 2024-01-12 03:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_productversion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productversion',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='catalog.product', verbose_name='Продукт'),
        ),
    ]