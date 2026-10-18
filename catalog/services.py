from django.core.cache import cache
from django.db.models import QuerySet
from django.conf import settings

from catalog.models import Product

CACHE_TTL = 60 * 5  # 5 минут
CACHE_KEY_TEMPLATE = "products_by_category:{slug}"
CACHE_KEY_ALL = "products_list"


def get_products() -> list[Product]:
    """Возвращает список всех продуктов (с кешированием)."""
    # Проверяем настройку через settings
    if not getattr(settings, "CACHE_ENABLED", True):
        return list(Product.objects.all().order_by("-created_at"))

    products = cache.get(CACHE_KEY_ALL)
    if products is not None:
        return products

    # ВАЖНО: оборачиваем QuerySet в list(), иначе кеш не сработает
    products = list(Product.objects.all().order_by("-created_at"))
    cache.set(CACHE_KEY_ALL, products, CACHE_TTL)
    return products

def get_products_by_category(category_slug: str) -> list[Product]:
    """
    Возвращает список всех продуктов в указанной категории.
    Результат кешируется на CACHE_TTL секунд.
    """
    cache_key = CACHE_KEY_TEMPLATE.format(slug=category_slug)

    products = cache.get(cache_key)
    if products is not None:
        return products

    products = list(
        Product.objects
        .filter(category__slug=category_slug)
        .select_related("category")
        .order_by("-created_at")
    )
    cache.set(cache_key, products, CACHE_TTL)
    return products


def invalidate_products_by_category_cache(category_slug: str | None = None) -> None:
    """
    Сбрасывает кеш продуктов.
    Если slug передан — только для этой категории
    """
    if category_slug is not None:
        cache.delete(CACHE_KEY_TEMPLATE.format(slug=category_slug))
        return

    # Удаляем по шаблону через django-redis
    try:
        cache.delete_pattern(CACHE_KEY_TEMPLATE.format(slug="*"))
    except AttributeError:
        cache.clear()