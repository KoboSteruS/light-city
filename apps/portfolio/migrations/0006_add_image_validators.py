# Generated manually for portfolio image validators
# No database changes required - validators are Python-level only
#
# To apply (if needed):
# python manage.py makemigrations portfolio
# python manage.py migrate portfolio

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_add_portfolio_order'),  # Последняя миграция
    ]

    operations = [
        # Валидаторы добавлены в модель, но не требуют изменения схемы БД
    ]
