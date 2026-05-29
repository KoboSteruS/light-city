"""
Утилиты для главного приложения.
"""

from .notifications import format_contact_message
from .vk import send_vk_message

__all__ = ['format_contact_message', 'send_vk_message']
