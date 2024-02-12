from catalog.models import Category
from django.core.cache import cache
from django.conf import settings


def get_categories():
    if settings.CACHE_ENABLED:
        key = "categories"
        categories = cache.get(key)

        if categories is None:
            categories = Category.objects.all()
            cache.set(key, categories)
            return categories

        return categories
    return Category.objects.all()
