from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from catalog.models import Product, Category
import os


class Command(BaseCommand):
    help = 'Load socks products from fixtures'

    def handle(self, *args, **options):
        fixtures_dir = os.path.join(settings.BASE_DIR, 'fixtures')

        if not os.path.exists(fixtures_dir):
            self.stdout.write(self.style.ERROR(f'Директория фикстур не найдена: {fixtures_dir}'))
            return

        categories_fixture = os.path.join(fixtures_dir, 'categories.json')
        products_fixture = os.path.join(fixtures_dir, 'products.json')

        if not os.path.exists(categories_fixture) and not os.path.exists(products_fixture):
            self.stdout.write(self.style.ERROR('Фикстуры не найдены!'))
            self.stdout.write(self.style.WARNING('Создайте их командой:'))
            self.stdout.write(self.style.WARNING('  python manage.py dumpdata catalog.Category --indent 2 > fixtures/categories.json'))
            self.stdout.write(self.style.WARNING('  python manage.py dumpdata catalog.Product --indent 2 > fixtures/products.json'))
            return

        self.stdout.write(self.style.WARNING('Удаление существующих данных...'))
        deleted_products, _ = Product.objects.all().delete()
        deleted_categories, _ = Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено продуктов: {deleted_products}'))
        self.stdout.write(self.style.SUCCESS(f'Удалено категорий: {deleted_categories}'))
        self.stdout.write(self.style.SUCCESS('Данные очищены. Начинаем загрузку фикстур...\n'))

        try:
            if os.path.exists(categories_fixture):
                self.stdout.write(self.style.SUCCESS('Загрузка категорий...'))
                call_command('loaddata', categories_fixture, verbosity=0)

            if os.path.exists(products_fixture):
                self.stdout.write(self.style.SUCCESS('Загрузка продуктов...'))
                call_command('loaddata', products_fixture, verbosity=0)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке фикстур: {e}'))
            import traceback
            traceback.print_exc()
            return

        # Статистика
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 50))
        self.stdout.write(self.style.SUCCESS(f'   Всего категорий: {Category.objects.count()}'))
        for cat in Category.objects.all():
            cnt = Product.objects.filter(category=cat).count()
            self.stdout.write(self.style.SUCCESS(f'   {cat.name_category}: {cnt} товаров'))
        self.stdout.write(self.style.SUCCESS(f'   Всего товаров: {Product.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('Фикстуры успешно загружены!'))