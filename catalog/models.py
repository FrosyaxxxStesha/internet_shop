from django.db import models
import os.path
from django.contrib.auth import get_user_model


User = get_user_model()


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
                                      default='product_preview/default.svg')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='Цена')
    created_at = models.DateTimeField(verbose_name='Дата добавления товара', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления товара', auto_now=True)
    user = models.ForeignKey(User,
                             verbose_name="Пользователь",
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True,
                             related_name="products"
                             )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class ContactResponse(models.Model):
    name = models.CharField(max_length=35, verbose_name="Имя")
    email = models.EmailField(verbose_name='Электронная почта')

    class Meta:
        verbose_name = 'Запрос на связь'
        verbose_name_plural = 'Запросы на связь'

    def __str__(self):
        return self.name


class ProductVersion(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="versions",
                                verbose_name="Продукт"
                                )
    number = models.PositiveSmallIntegerField(verbose_name="Номер")
    name = models.CharField(max_length=30, verbose_name="Название")
    current = models.BooleanField(default=False, verbose_name="Текущая версия")

    class Meta:
        verbose_name = "Версия продукта"
        verbose_name_plural = "Версии продуктов"
        ordering = ["-number"]
