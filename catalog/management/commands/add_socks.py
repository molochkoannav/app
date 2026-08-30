from django.core.management.base import BaseCommand
from catalog.models import Product, Category
from decimal import Decimal

class Command(BaseCommand):
    help = 'Add all socks products to categories'

    def handle(self, *args, **options):
        men_category, created = Category.objects.get_or_create(
            name_category='Мужские носки',
            defaults={'description': 'Мужские носки'}
        )
        
        women_category, created = Category.objects.get_or_create(
            name_category='Женские носки',
            defaults={'description': 'Женские носки'}
        )
        
        kids_category, created = Category.objects.get_or_create(
            name_category='Детские носки',
            defaults={'description': 'Детские носки'}
        )
        
        wool_category, created = Category.objects.get_or_create(
            name_category='Шерстяные носки',
            defaults={'description': 'Шерстяные носки'}
        )

        men_products = [
            ('Классические', 'Парадновыходные носки, для официальных мероприятий. Хлопок 95%, эластан 5%. Размеры: 39-42, 43-46', 15.00),
            ('Спортивные', 'Обеспечивают эффективный отвод пота и влаги. Усиленная пятка и мысок. Дышащая сетка', 18.00),
            ('Длинные', 'Высокая посадка до колена. Тёплый хлопок', 20.00),
            ('Премиум', 'Мерсеризованный хлопок. Без швов на пальцах', 25.00),
            ('Тёплые', 'Шерсть 70%, акрил 30%. Для холодной погоды', 22.00),
            ('Лёгкие', 'Тонкий хлопок. Для жаркой погоды', 12.00),
        ]

        women_products = [
            ('Классические', 'Хлопок 95%, эластан 5%. Размеры: 39-42, 43-46', 15.00),
            ('Капроновые', 'Сеточкой. Дышащая структура', 18.00),
            ('Гетры', 'Высокая посадка до колена. Тёплый хлопок', 20.00),
            ('Премиум', 'Кашемировые. Без швов на пальцах', 25.00),
            ('Ажурные', 'Кружевной узор. Хлопок 100%', 22.00),
            ('Тёплые', 'Шерсть 80%, акрил 20%. Для холодной погоды', 24.00),
        ]
        kids_products = [
            ('Яркие', 'Мультяшный принт. Хлопок 100%', 8.00),
            ('Спортивные', 'Усиленная пятка. Подойдут для бега', 10.00),
            ('Тёплые', 'Флисовая подкладка. Для зимы', 12.00),
            ('Премиум', 'Органический хлопок. Без швов', 15.00),
            ('Полосатые', 'Яркие полоски. Хлопок 95%', 9.00),
            ('С рисунком', 'Животные. Хлопок 100%', 11.00),
        ]

        wool_products = [
            ('Меринос', 'Шерсть мериноса 100%. Очень тёплые', 25.00),
            ('Смесовые', 'Шерсть + акрил. Меньше скатываются', 20.00),
            ('Термо', 'Термошерсть. Для экстремального холода', 28.00),
            ('Кашемир', 'Кашемир + шерсть. Максимальная мягкость', 35.00),
            ('Альпака', 'Шерсть альпака 100%. Гипоаллергенные', 30.00),
            ('Овечья', 'Натуральная овечья шерсть. Классические', 18.00),
        ]
        
        self.stdout.write(self.style.SUCCESS('Мужские носки:'))
        for name, desc, price in men_products:
            self.add_product(name, desc, price, men_category)
        
        self.stdout.write(self.style.SUCCESS('Женские носки:'))
        for name, desc, price in women_products:
            self.add_product(name, desc, price, women_category)
        
        self.stdout.write(self.style.SUCCESS('Детские носки:'))
        for name, desc, price in kids_products:
            self.add_product(name, desc, price, kids_category)
        
        self.stdout.write(self.style.SUCCESS('Шерстяные носки:'))
        for name, desc, price in wool_products:
            self.add_product(name, desc, price, wool_category)
        
        # Итог
        total_men = Product.objects.filter(category=men_category).count()
        total_women = Product.objects.filter(category=women_category).count()
        total_kids = Product.objects.filter(category=kids_category).count()
        total_wool = Product.objects.filter(category=wool_category).count()
        total_all = Product.objects.all().count()
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS(f'   Мужские носки: {total_men} товаров'))
        self.stdout.write(self.style.SUCCESS(f'   Женские носки: {total_women} товаров'))
        self.stdout.write(self.style.SUCCESS(f'   Детские носки: {total_kids} товаров'))
        self.stdout.write(self.style.SUCCESS(f'   Шерстяные носки: {total_wool} товаров'))
        self.stdout.write(self.style.SUCCESS(f'   Всего товаров: {total_all}'))
        self.stdout.write(self.style.SUCCESS('='*50))
    
    def add_product(self, name, desc, price, category):
        obj, created = Product.objects.update_or_create(
            name_product=name,
            category=category,
            defaults={
                'description': desc,
                'price': Decimal(str(price))
            }
        )
        status = 'Готово' if created else 'Не готово'
        self.stdout.write(f'  {status} {obj.name_product} - ${obj.price}')