"""
Форматирование уведомлений о заявках (VK, и др.).
"""


def format_contact_message(
    name: str,
    phone: str,
    email: str = '',
    message: str = '',
    is_callback: bool = False,
    contact_preference: str = '',
) -> str:
    """
    Текст уведомления о новой заявке (без HTML — подходит для VK).

    Args:
        name: Имя клиента
        phone: Телефон
        email: Email (опционально)
        message: Текст сообщения (опционально)
        is_callback: Заказ звонка
        contact_preference: call / message / any

    Returns:
        Отформатированное сообщение
    """
    message_type = '📞 Заказ звонка' if is_callback else '✉️ Новое сообщение'

    pref_labels = {'call': 'Звонок', 'message': 'Сообщение', 'any': 'Без разницы'}
    pref_display = pref_labels.get(contact_preference, contact_preference or '—')

    lines = [
        message_type,
        '',
        f'👤 Имя: {name}',
        f'📱 Телефон: {phone}',
    ]

    if contact_preference:
        lines.append(f'📲 Способ связи: {pref_display}')

    if email:
        lines.append(f'📧 Email: {email}')

    if message:
        lines.extend(['', '💬 Сообщение:', message])

    return '\n'.join(lines)
