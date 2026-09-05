from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category
import os

class Command(BaseCommand):
    help = 'Load socks products from fixtures'

    def handle(self, *args, **options):
    
        fixtures_dir = os.path.join('fixtures')  
        
    
        if not os.path.exists(fixtures_dir):
            self.stdout.write(self.style.ERROR(f'Директория фикстур не найдена: {fixtures_dir}'))
            return
        
        
        available_fixtures = []
        if os.path.exists(os.path.join(fixtures_dir, 'categories.json')):
            available_fixtures.append('categories.json')
        if os.path.exists(os.path.join(fixtures_dir, 'products.json')):
            available_fixtures.append('products.json')
        
        if not available_fixtures:
            self.stdout.write(self.style.ERROR('Фикстуры не найдены!'))
            self.stdout.write(self.style.WARNING('Создайте фикстуры командой:'))
            self.stdout.write(self.style.WARNING('  mkdir fixtures'))
            self.stdout.write(self.style.WARNING('  python manage.py dumpdata catalog.Category --indent 2 > fixtures/categories.json'))
            self.stdout.write(self.style.WARNING('  python manage.py dumpdata catalog.Product --indent 2 > fixtures/products.json'))
            return
        
        
        self.stdout.write(self.style.WARNING('Удаление существующих данных...'))
        
        products_deleted = Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено продуктов: {products_deleted[0]}'))
        
        categories_deleted = Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено категорий: {categories_deleted[0]}'))
        
        self.stdout.write(self.style.SUCCESS('Данные очищены. Начинаем загрузку фикстур...\n'))
        
     
        try:
        
            if 'categories.json' in available_fixtures:
                self.stdout.write(self.style.SUCCESS('Загрузка категорий...'))
                call_command('loaddata', 'fixtures/categories.json', verbosity=0)  # ← исправлено

            if 'products.json' in available_fixtures:
                self.stdout.write(self.style.SUCCESS('Загрузка продуктов...'))
                call_command('loaddata', 'fixtures/products.json', verbosity=0)  # ← исправлено
            
            self.stdout.write(self.style.SUCCESS('\n' + '='*50))
            self.stdout.write(self.style.SUCCESS('Фикстуры успешно загружены!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке фикстур: {e}'))
            return
        
        # Статистика
        total_men = Product.objects.filter(category__name_category='Мужские носки').count()
        total_women = Product.objects.filter(category__name_category='Женские носки').count()
        total_kids = Product.objects.filter(category__name_category='Детские носки').count()
        total_wool = Product.objects.filter(category__name_category='Шерстяные носки').count()
        total_all = Product.objects.all().count()
        total_categories = Category.objects.all().count()
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS(f'   Всего категорий: {total_categories}'))
        self.stdout.write(self.style.SUCCESS(f'   Мужские носки: {total_men} товаров'))
        self.stdout.write(self.style.SUCCESS(f'   Женские носки: {total_women} товаров'))
        self.stdout.write(self.style.SUCCESS(f'   Детские носки: {total_kids} товаров'))
        self.stdout.write(self.style.SUCCESS(f'   Шерстяные носки: {total_wool} товаров'))
        self.stdout.write(self.style.SUCCESS(f'   Всего товаров: {total_all}'))
        self.stdout.write(self.style.SUCCESS('='*50))