# # import csv
# # from datetime import datetime
# #
# # from django.core.management.base import BaseCommand
# # from phones.models import Phone
# #
# #
# # class Command(BaseCommand):
# #     def add_arguments(self, parser):
# #         pass
# #
# #     def handle(self, *args, **options):
# #         with open('phones.csv', 'r') as file:
# #             phones = list(csv.DictReader(file, delimiter=';'))
# #
# #         for phone in phones:
# #             pass
#
# import csv
# from datetime import datetime
#
# from django.core.management.base import BaseCommand
# from phones.models import Phone
# from django.utils import timezone
#
#
# class Command(BaseCommand):
#     def add_arguments(self, parser):
#         pass
#
#     def handle(self, *args, **options):
#         with open('phones.csv', 'r', encoding='utf-8') as file:
#             phones = list(csv.DictReader(file, delimiter=';'))
#
#         for phone_data in phones:
#             try:
#                 # Преобразуем строку даты в объект datetime
#                 release_date_str = phone_data.get('release_date')
#                 release_date = None
#
#                 if release_date_str:
#                     release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
#
#                 Phone.objects.get_or_create(
#                     id=int(phone_data['id']),
#                     name=phone_data['name'],
#                     image=phone_data['image'],
#                     price=int(phone_data['price']),
#                     release_date=release_date,
#                     lte_exists=bool(phone_data['lte_exists'] == 'True'),
#                 )
#             except ValueError as e:
#                 self.stdout.write(self.style.ERROR(f"Ошибка обработки строки: {phone_data}. Ошибка: {e}"))
#             except Exception as e:
#                 self.stdout.write(self.style.ERROR(f"Непредвиденная ошибка при обработке строки {phone_data}. Ошибка: {e}"))
#
#         self.stdout.write(self.style.SUCCESS('Данные успешно импортированы!'))
import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from phones.models import Phone
from django.utils import timezone
from django.utils.text import slugify


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r', encoding='utf-8') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone_data in phones:
            try:
                release_date_str = phone_data.get('release_date')
                release_date = None
                if release_date_str:
                    release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()


                slug = slugify(phone_data['name'])
                phone, created = Phone.objects.get_or_create(
                    id=int(phone_data['id']),
                    defaults={
                        'name': phone_data['name'],
                        'image': phone_data['image'],
                        'price': int(phone_data['price']),
                        'release_date': release_date,
                        'lte_exists': bool(phone_data['lte_exists'] == 'True'),
                        'slug': slug,
                    }
                )
                if not created:
                  phone.name = phone_data['name']
                  phone.image = phone_data['image']
                  phone.price = int(phone_data['price'])
                  phone.release_date = release_date
                  phone.lte_exists = bool(phone_data['lte_exists'] == 'True')
                  phone.slug = slug
                  phone.save()


            except ValueError as e:
                self.stdout.write(self.style.ERROR(f"Ошибка обработки строки: {phone_data}. Ошибка: {e}"))
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Непредвиденная ошибка при обработке строки {phone_data}. Ошибка: {e}"))

        self.stdout.write(self.style.SUCCESS('Данные успешно импортированы!'))