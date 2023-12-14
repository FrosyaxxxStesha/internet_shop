from django.db import models
import os.path


class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    description = models.TextField(verbose_name='описание', null=True, blank=True)
    preview_image = models.ImageField(verbose_name='Фото товара(превью)',
                                      upload_to=f'{os.path.join("product_preview", "")}',
                                      default='default.svg')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='Цена')
    created_at = models.DateField(verbose_name='Дата добавления товара', auto_now_add=True)
    updated_at = models.DateField(verbose_name='Дата обновления товара', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
