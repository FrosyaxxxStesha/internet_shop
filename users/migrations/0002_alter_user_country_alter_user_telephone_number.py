# Generated by Django 5.0 on 2024-01-16 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Страна'),
        ),
        migrations.AlterField(
            model_name='user',
            name='telephone_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name=True),
        ),
    ]
