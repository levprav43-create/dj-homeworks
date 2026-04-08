import csv
from django.core.management.base import BaseCommand
from phones.models import Phone
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Импортирует телефоны из CSV файла'

    def handle(self, *args, **options):
        # Открываем CSV файл
        with open('phones.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            
            # Очищаем базу перед импортом
            Phone.objects.all().delete()
            
            # Проходим по каждой строке
            for row in reader:
                Phone.objects.create(
                    id=int(row['id']),
                    name=row['name'],
                    price=float(row['price'].replace(' ', '')),
                    image=row['image'],
                    release_date=row['release_date'],
                    lte_exists=row['lte_exists'].lower() == 'true',
                    slug=slugify(row['name'])
                )
        
        self.stdout.write(self.style.SUCCESS('Успешно импортированы телефоны!'))