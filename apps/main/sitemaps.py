"""
Sitemap для SEO оптимизации.
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.services.models import Service
from apps.portfolio.models import PortfolioItem


class StaticViewSitemap(Sitemap):
    """
    Sitemap для статических страниц.
    """
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return [
            'main:home',
            'main:about',
            'services:catalog',
            'portfolio:list',
            'main:privacy',
        ]

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    """
    Sitemap для страниц услуг.
    """
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Service.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class PortfolioSitemap(Sitemap):
    """
    Sitemap для работ портфолио.
    """
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return PortfolioItem.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

