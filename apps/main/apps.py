"""
Конфигурация главного приложения.
"""

import threading
import os
from django.apps import AppConfig
from loguru import logger

# Глобальная переменная для отслеживания запуска бота
_bot_thread_started = False
_bot_thread_lock = threading.Lock()
_bot_thread = None


class MainConfig(AppConfig):
    """Конфигурация главного приложения."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.main'
    verbose_name = 'Главная страница'
    
    def ready(self):
        """Запуск при инициализации приложения."""
        global _bot_thread_started, _bot_thread
        
        # На production бот запускается через systemd service
        # Автозапуск только в режиме разработки (runserver)
        if os.environ.get('RUN_MAIN') != 'true':
            return
        
        # Проверяем, не запущен ли уже поток бота
        if _bot_thread is not None and _bot_thread.is_alive():
            return
        
        # Запускаем бота только один раз (только в режиме разработки)
        with _bot_thread_lock:
            if not _bot_thread_started:
                _bot_thread_started = True
                self._start_telegram_bot()
    
    def _start_telegram_bot(self):
        """Запуск Telegram бота в отдельном потоке."""
        global _bot_thread
        
        def run_bot():
            try:
                from django.core.management import call_command
                # Небольшая задержка, чтобы Django полностью инициализировался
                import time
                time.sleep(3)
                logger.info('Запуск Telegram бота...')
                call_command('telegram_bot')
            except Exception as e:
                logger.error(f'Ошибка при запуске Telegram бота: {e}')
        
        # Запускаем бота в отдельном потоке (daemon=True, чтобы не блокировать завершение)
        _bot_thread = threading.Thread(target=run_bot, daemon=True, name='TelegramBot')
        _bot_thread.start()
        logger.info('Поток для Telegram бота создан')

