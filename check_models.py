"""
Скрипт для проверки импортов моделей.
"""

import os
import sys
import django

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("=" * 60)
print("ПРОВЕРКА ИМПОРТОВ МОДЕЛЕЙ")
print("=" * 60)

# Проверяем core
try:
    from apps.core.models import BaseModel
    print("✓ apps.core.models.BaseModel - OK")
except Exception as e:
    print(f"✗ apps.core.models.BaseModel - ОШИБКА: {e}")

# Проверяем main
try:
    from apps.main.models import Slider, AboutUs, SiteSettings
    print("✓ apps.main.models - OK (Slider, AboutUs, SiteSettings)")
except Exception as e:
    print(f"✗ apps.main.models - ОШИБКА: {e}")

# Проверяем services
try:
    from apps.services.models import Service
    print("✓ apps.services.models.Service - OK")
except Exception as e:
    print(f"✗ apps.services.models.Service - ОШИБКА: {e}")

# Проверяем portfolio
try:
    from apps.portfolio.models import Category, PortfolioItem
    print("✓ apps.portfolio.models - OK (Category, PortfolioItem)")
except Exception as e:
    print(f"✗ apps.portfolio.models - ОШИБКА: {e}")

# Проверяем contacts
try:
    from apps.contacts.models import ContactMessage
    print("✓ apps.contacts.models.ContactMessage - OK")
except Exception as e:
    print(f"✗ apps.contacts.models.ContactMessage - ОШИБКА: {e}")

print("=" * 60)
print("\nПроверка завершена!")
print("\nЕсли все OK - запусти:")
print("python manage.py makemigrations")
print("python manage.py migrate")



