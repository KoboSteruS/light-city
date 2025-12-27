"""
Тесты для моделей главного приложения.

Пример структуры тестов для проекта.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.main.models import Slider, AboutUs, SiteSettings


class SliderModelTest(TestCase):
    """Тесты для модели Slider."""
    
    def setUp(self):
        """Подготовка данных для тестов."""
        self.slider = Slider.objects.create(
            title='Тестовый слайд',
            subtitle='Подзаголовок',
            button_text='Узнать больше',
            button_link='#test',
            order=1,
            is_active=True
        )
    
    def test_slider_creation(self):
        """Тест создания слайда."""
        self.assertEqual(self.slider.title, 'Тестовый слайд')
        self.assertEqual(self.slider.order, 1)
        self.assertTrue(self.slider.is_active)
        self.assertIsNotNone(self.slider.uuid)
        self.assertIsNotNone(self.slider.created_at)
        self.assertIsNotNone(self.slider.updated_at)
    
    def test_slider_str(self):
        """Тест строкового представления."""
        self.assertEqual(str(self.slider), 'Тестовый слайд')
    
    def test_slider_ordering(self):
        """Тест сортировки слайдов."""
        slider2 = Slider.objects.create(
            title='Второй слайд',
            order=0,
            is_active=True
        )
        slides = list(Slider.objects.all())
        self.assertEqual(slides[0], slider2)
        self.assertEqual(slides[1], self.slider)
    
    def test_active_slides_filter(self):
        """Тест фильтрации активных слайдов."""
        Slider.objects.create(
            title='Неактивный слайд',
            order=2,
            is_active=False
        )
        active_slides = Slider.objects.filter(is_active=True)
        self.assertEqual(active_slides.count(), 1)
        self.assertEqual(active_slides.first().title, 'Тестовый слайд')


class AboutUsModelTest(TestCase):
    """Тесты для модели AboutUs."""
    
    def test_about_singleton(self):
        """Тест Singleton паттерна."""
        about1 = AboutUs.objects.create(
            title='О нас 1',
            description='Описание 1',
            is_active=True
        )
        
        # Создаем вторую запись
        about2 = AboutUs.objects.create(
            title='О нас 2',
            description='Описание 2',
            is_active=True
        )
        
        # Первая должна стать неактивной
        about1.refresh_from_db()
        self.assertFalse(about1.is_active)
        self.assertTrue(about2.is_active)
    
    def test_about_str(self):
        """Тест строкового представления."""
        about = AboutUs.objects.create(
            title='О компании',
            description='Описание',
            is_active=True
        )
        self.assertEqual(str(about), 'О компании')


class SiteSettingsModelTest(TestCase):
    """Тесты для модели SiteSettings."""
    
    def test_settings_creation(self):
        """Тест создания настроек."""
        settings = SiteSettings.objects.create(
            site_name='Тест',
            phone='+79991234567',
            email='test@test.ru',
            address='Тестовый адрес',
            working_hours='9:00-18:00',
            is_active=True
        )
        
        self.assertEqual(settings.site_name, 'Тест')
        self.assertEqual(settings.phone, '+79991234567')
        self.assertIsNotNone(settings.uuid)
    
    def test_settings_singleton(self):
        """Тест Singleton паттерна для настроек."""
        settings1 = SiteSettings.objects.create(
            site_name='Настройки 1',
            phone='+79991111111',
            email='test1@test.ru',
            address='Адрес 1',
            is_active=True
        )
        
        settings2 = SiteSettings.objects.create(
            site_name='Настройки 2',
            phone='+79992222222',
            email='test2@test.ru',
            address='Адрес 2',
            is_active=True
        )
        
        # Первая должна стать неактивной
        settings1.refresh_from_db()
        self.assertFalse(settings1.is_active)
        self.assertTrue(settings2.is_active)
    
    def test_invalid_phone(self):
        """Тест валидации телефона."""
        # TODO: Добавить валидацию в модель
        # settings = SiteSettings(
        #     site_name='Тест',
        #     phone='invalid',
        #     email='test@test.ru',
        #     address='Адрес',
        # )
        # with self.assertRaises(ValidationError):
        #     settings.full_clean()
        pass


# TODO: Добавить тесты для остальных моделей:
# - Service
# - Category
# - PortfolioItem
# - ContactMessage

# TODO: Добавить тесты для views
# TODO: Добавить тесты для middleware
# TODO: Добавить интеграционные тесты

