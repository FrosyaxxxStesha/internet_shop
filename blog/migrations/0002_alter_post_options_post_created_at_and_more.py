# Generated by Django 5.0 on 2023-12-23 15:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at'], 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
        migrations.AddField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='preview_image',
            field=models.ImageField(default='blog_preview/default.svg', upload_to='blog_preview/', verbose_name='Превью'),
        ),
        migrations.AddField(
            model_name='post',
            name='published',
            field=models.BooleanField(default=False, verbose_name='Опубликован ли пост'),
        ),
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество просмотров'),
            preserve_default=False,
        ),
    ]
