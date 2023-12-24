from django.db import models
import os.path


class Post(models.Model):
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    title = models.CharField(max_length=40, verbose_name="Заголовок")
    slug = models.CharField(max_length=60, verbose_name="Слаг")
    body = models.TextField(verbose_name="Содержимое")
    preview_image = models.ImageField(upload_to=f'{os.path.join("blog_preview", "")}',
                                      default="blog_preview/default.png",
                                      verbose_name="Превью"
                                      )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    published = models.BooleanField(verbose_name="Опубликован ли пост", default=False)
    views = models.PositiveIntegerField(verbose_name="Количество просмотров", default=0)



