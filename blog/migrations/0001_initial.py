# Generated by Django 5.0 on 2023-12-23 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='Заголовок')),
                ('slug', models.CharField(max_length=60, verbose_name='Слаг')),
                ('body', models.TextField(verbose_name='Содержимое')),
            ],
        ),
    ]
