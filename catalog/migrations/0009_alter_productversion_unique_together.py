# Generated by Django 5.0 on 2024-01-15 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_alter_productversion_product'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='productversion',
            unique_together=set(),
        ),
    ]
