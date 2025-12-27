"""
Команда для исправления slug с транслитерацией.
"""

from django.core.management.base import BaseCommand
from apps.services.models import Service


# Простая транслитерация
TRANSLIT_TABLE = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
    'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
    'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
    'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch',
    'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
}


def transliterate(text):
    """Транслитерация русского текста."""
    result = []
    for char in text:
        result.append(TRANSLIT_TABLE.get(char, char))
    return ''.join(result)


def make_slug(text):
    """Создание slug с транслитерацией."""
    from django.utils.text import slugify
    transliterated = transliterate(text)
    return slugify(transliterated)


class Command(BaseCommand):
    """Команда для исправления slug."""
    
    help = 'Исправляет slug для услуг с транслитерацией'
    
    def handle(self, *args, **options):
        """Основная логика команды."""
        
        self.stdout.write(self.style.WARNING('Исправление slug для услуг...'))
        
        try:
            services = Service.objects.all()
            
            for service in services:
                # Генерируем уникальный slug
                base_slug = make_slug(service.name)
                slug = base_slug
                counter = 1
                
                # Проверяем уникальность
                while Service.objects.filter(slug=slug).exclude(pk=service.pk).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                # Сохраняем
                Service.objects.filter(pk=service.pk).update(slug=slug)
                
                self.stdout.write(f'  [OK] Slug создан для: {service.name} -> {slug}')
            
            self.stdout.write(self.style.SUCCESS('Slug успешно исправлены!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))


