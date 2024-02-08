# Generated by Django 5.0 on 2024-02-07 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_product_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_at'], 'permissions': [('can_moderate', 'can view moderation and apply decision to public or no')], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
    ]
