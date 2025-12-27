"""
Middleware для дополнительной безопасности.

Обеспечивает защиту от различных атак и логирование подозрительной активности.
"""

import time
from typing import Callable
from django.http import HttpRequest, HttpResponse
from django.core.cache import cache
from loguru import logger


class SecurityHeadersMiddleware:
    """
    Middleware для добавления заголовков безопасности.
    
    Добавляет важные HTTP заголовки для защиты от XSS, clickjacking и т.д.
    """
    
    def __init__(self, get_response: Callable):
        self.get_response = get_response
    
    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        
        # Защита от XSS
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Защита от clickjacking
        response['X-Frame-Options'] = 'DENY'
        
        # Referrer Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Content Security Policy (базовая)
        # В продакшене настройте под свои нужды
        if not request.path.startswith('/admin'):
            response['Content-Security-Policy'] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
                "img-src 'self' data: https:; "
                "font-src 'self' https://fonts.gstatic.com;"
            )
        
        return response


class RequestLoggingMiddleware:
    """
    Middleware для логирования запросов.
    
    Логирует все запросы с информацией о времени выполнения.
    """
    
    def __init__(self, get_response: Callable):
        self.get_response = get_response
    
    def __call__(self, request: HttpRequest) -> HttpResponse:
        start_time = time.time()
        
        # Получаем IP адрес
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Обрабатываем запрос
        response = self.get_response(request)
        
        # Считаем время выполнения
        duration = time.time() - start_time
        
        # Логируем
        logger.info(
            f"{request.method} {request.path} | "
            f"Status: {response.status_code} | "
            f"IP: {ip} | "
            f"Duration: {duration:.3f}s"
        )
        
        # Добавляем заголовок с временем выполнения
        response['X-Response-Time'] = f"{duration:.3f}s"
        
        return response


class RateLimitMiddleware:
    """
    Middleware для ограничения частоты запросов.
    
    Защита от DDoS и автоматизированных атак.
    """
    
    # Лимиты: (количество запросов, период в секундах)
    RATE_LIMITS = {
        'default': (100, 60),  # 100 запросов в минуту
        'contact': (10, 60),   # 10 запросов к форме контактов в минуту
    }
    
    def __init__(self, get_response: Callable):
        self.get_response = get_response
    
    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Получаем IP
        ip = self.get_client_ip(request)
        
        # Определяем тип лимита
        limit_type = self.get_limit_type(request)
        max_requests, period = self.RATE_LIMITS.get(limit_type, self.RATE_LIMITS['default'])
        
        # Ключ для кеша
        cache_key = f'ratelimit:{limit_type}:{ip}'
        
        # Получаем текущее количество запросов
        requests = cache.get(cache_key, 0)
        
        if requests >= max_requests:
            logger.warning(
                f"Rate limit exceeded for IP {ip} on {request.path}"
            )
            return HttpResponse(
                'Rate limit exceeded. Please try again later.',
                status=429
            )
        
        # Увеличиваем счетчик
        cache.set(cache_key, requests + 1, period)
        
        return self.get_response(request)
    
    def get_client_ip(self, request: HttpRequest) -> str:
        """Получение IP адреса клиента."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'unknown')
    
    def get_limit_type(self, request: HttpRequest) -> str:
        """Определение типа лимита в зависимости от пути."""
        if '/contacts/send/' in request.path:
            return 'contact'
        return 'default'


class SuspiciousActivityMiddleware:
    """
    Middleware для обнаружения подозрительной активности.
    
    Логирует подозрительные запросы и блокирует явные атаки.
    """
    
    SUSPICIOUS_PATTERNS = [
        'eval(', 'exec(', '<script', 'javascript:', 'onerror=',
        '../', '..\\', 'etc/passwd', 'cmd.exe', 'union select',
        'DROP TABLE', 'INSERT INTO', '--', '/*', '*/',
    ]
    
    def __init__(self, get_response: Callable):
        self.get_response = get_response
    
    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Проверяем GET и POST параметры
        suspicious = self.check_for_suspicious_content(request)
        
        if suspicious:
            ip = self.get_client_ip(request)
            logger.warning(
                f"Suspicious activity detected from IP {ip}: "
                f"Pattern '{suspicious}' in {request.path}"
            )
            
            # В продакшене можно заблокировать IP
            # return HttpResponse('Forbidden', status=403)
        
        return self.get_response(request)
    
    def check_for_suspicious_content(self, request: HttpRequest) -> str:
        """Проверка запроса на подозрительный контент."""
        # Проверяем GET параметры
        for key, value in request.GET.items():
            for pattern in self.SUSPICIOUS_PATTERNS:
                if pattern.lower() in str(value).lower():
                    return pattern
        
        # Проверяем POST параметры
        for key, value in request.POST.items():
            for pattern in self.SUSPICIOUS_PATTERNS:
                if pattern.lower() in str(value).lower():
                    return pattern
        
        return None
    
    def get_client_ip(self, request: HttpRequest) -> str:
        """Получение IP адреса клиента."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'unknown')

