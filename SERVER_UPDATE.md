# Инструкция по обновлению на сервере

## Обновление услуг (Холсты и Интерьерные решения)

Для обновления услуг на сервере выполните следующие команды:

```bash
# 1. Активируйте виртуальное окружение (если используется)
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows

# 2. Перейдите в директорию проекта
cd /path/to/your/project

# 3. Обновите услуги (простая команда)
python manage.py update_services_server

# ИЛИ используйте полную команду:
python manage.py update_home_services
```

## Что делает команда `update_home_services`:

- Создает/обновляет все услуги, включая:
  - **Холсты** (slug: `kholsty`, order: 7)
  - **Интерьерные решения** (slug: `interiernye-resheniia`, order: 8)
- Активирует все нужные услуги
- Загружает изображения для услуг (если они есть в `static/img/`)

## Проверка после обновления:

1. Проверьте, что обе услуги отображаются в админ-панели:
   - Зайдите в `/admin/services/service/`
   - Убедитесь, что есть услуги "Холсты" и "Интерьерные решения"

2. Проверьте на сайте:
   - Главная страница: `/` - должны отображаться обе услуги
   - Каталог услуг: `/services/` - обе услуги в списке
   - Портфолио: `/portfolio/` - обе услуги в фильтрах

## Если что-то пошло не так:

Если услуги не обновились, можно вручную проверить в Django shell:

```bash
python manage.py shell
```

```python
from apps.services.models import Service

# Проверяем услуги
services = Service.objects.filter(is_active=True)
for s in services:
    print(f"{s.name} (slug: {s.slug}, order: {s.order})")

# Если нужно создать вручную
from apps.services.models import Service, ServiceCategory

# Получаем категорию
cat = ServiceCategory.objects.first()

# Создаем/обновляем услугу "Холсты"
kholsty, _ = Service.objects.get_or_create(
    slug='kholsty',
    defaults={
        'name': 'Холсты',
        'description': '<p>Печать на холстах. Интерьерные решения, фотографии, картины. Высокое качество печати.</p>',
        'price_from': 800,
        'price_unit': '₽',
        'order': 7,
        'is_active': True,
        'category': cat
    }
)

# Создаем/обновляем услугу "Интерьерные решения"
interior, _ = Service.objects.get_or_create(
    slug='interiernye-resheniia',
    defaults={
        'name': 'Интерьерные решения',
        'description': '<p>Интерьерные решения для вашего бизнеса. Декоративные элементы, оформление помещений, дизайн интерьеров.</p>',
        'price_from': 5000,
        'price_unit': '₽',
        'order': 8,
        'is_active': True,
        'category': cat
    }
)
```
