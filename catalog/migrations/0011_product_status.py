# Generated by Django 5.0 on 2024-02-05 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_product_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('FM', 'Moderation failed'), ('WM', 'Waiting for moderation'), ('PD', 'Published')], default='WM', max_length=2),
        ),
    ]
