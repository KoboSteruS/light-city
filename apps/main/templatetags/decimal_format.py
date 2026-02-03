"""
Template filter для форматирования Decimal значений с точкой вместо запятой.
"""

from django import template
from decimal import Decimal

register = template.Library()


@register.filter(name='decimal_dot')
def decimal_dot(value, decimal_places=2):
    """
    Форматирует Decimal значение с точкой в качестве разделителя.
    
    Примеры:
        {{ value|decimal_dot }} -> 1.00
        {{ value|decimal_dot:1 }} -> 1.0
    """
    if value is None:
        return ''
    
    # Преобразуем в Decimal если это не Decimal
    if not isinstance(value, Decimal):
        try:
            value = Decimal(str(value))
        except (ValueError, TypeError):
            return str(value)
    
    # Форматируем с точкой
    format_str = f'.{decimal_places}f'
    return format(value, format_str)
