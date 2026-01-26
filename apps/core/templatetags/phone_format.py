"""
Template filter для форматирования телефонных номеров.
"""

from django import template

register = template.Library()


@register.filter(name='phone_format')
def phone_format(value):
    """
    Форматирует телефонный номер в формат +7 (8142) 28-09-03
    
    Примеры:
        +78142280903 -> +7 (8142) 28-09-03
        78142280903 -> +7 (8142) 28-09-03
        8142280903 -> +7 (8142) 28-09-03
    """
    if not value:
        return value
    
    # Удаляем все нецифровые символы кроме плюса
    phone = ''.join(filter(str.isdigit, str(value).replace('+', '')))
    
    # Если номер начинается с 8, заменяем на 7
    if phone.startswith('8'):
        phone = '7' + phone[1:]
    
    # Если номер не начинается с 7, добавляем 7
    if not phone.startswith('7'):
        phone = '7' + phone
    
    # Форматируем: +7 (8142) 28-09-03
    if len(phone) >= 11:
        return f"+7 ({phone[1:5]}) {phone[5:7]}-{phone[7:9]}-{phone[9:11]}"
    elif len(phone) >= 7:
        # Если номер короче, форматируем что есть
        formatted = f"+7 ({phone[1:5]}) {phone[5:7]}"
        if len(phone) >= 9:
            formatted += f"-{phone[7:9]}"
        if len(phone) >= 11:
            formatted += f"-{phone[9:11]}"
        return formatted
    
    return value
