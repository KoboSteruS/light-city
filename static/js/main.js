/**
 * Яркий Город - Главные скрипты
 * 
 * Обработка интерактивности и анимаций
 */

(function() {
    'use strict';

    /**
     * Инициализация при загрузке DOM
     */
    document.addEventListener('DOMContentLoaded', function() {
        initSmoothScroll();
        initScrollEffects();
        initFormValidation();
        initPhoneMask();
        initLazyLoading();
    });

    /**
     * Плавная прокрутка к якорям
     */
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                
                // Игнорируем якоря bootstrap (модальные окна и т.д.)
                if (href === '#' || href.startsWith('#bs-')) {
                    return;
                }
                
                const targetElement = document.querySelector(href);
                if (targetElement) {
                    e.preventDefault();
                    const headerOffset = 80;
                    const elementPosition = targetElement.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    /**
     * Эффекты при скролле
     */
    function initScrollEffects() {
        const header = document.querySelector('.header');
        
        window.addEventListener('scroll', function() {
            if (window.scrollY > 100) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }

    /**
     * Валидация формы обратной связи
     */
    function initFormValidation() {
        const form = document.querySelector('.contact-form');
        
        if (!form) return;
        
        form.addEventListener('submit', function(e) {
            const phoneInput = form.querySelector('input[name="phone"]');
            const messageInput = form.querySelector('textarea[name="message"]');
            
            let isValid = true;
            
            // Валидация телефона
            if (phoneInput) {
                const phoneValue = phoneInput.value.replace(/\D/g, '');
                if (phoneValue.length < 10) {
                    showError(phoneInput, 'Введите корректный номер телефона');
                    isValid = false;
                } else {
                    clearError(phoneInput);
                }
            }
            
            // Валидация сообщения
            if (messageInput && messageInput.value.trim().length < 10) {
                showError(messageInput, 'Сообщение должно содержать минимум 10 символов');
                isValid = false;
            } else if (messageInput) {
                clearError(messageInput);
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    }

    /**
     * Показать ошибку валидации
     */
    function showError(input, message) {
        clearError(input);
        
        input.classList.add('is-invalid');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        
        input.parentNode.appendChild(errorDiv);
    }

    /**
     * Очистить ошибку валидации
     */
    function clearError(input) {
        input.classList.remove('is-invalid');
        
        const errorDiv = input.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    }

    /**
     * Маска для телефона
     */
    function initPhoneMask() {
        const phoneInputs = document.querySelectorAll('input[type="tel"], input[name="phone"]');
        
        phoneInputs.forEach(input => {
            input.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                
                if (value.length === 0) {
                    e.target.value = '';
                    return;
                }
                
                // Форматирование: +7 (999) 999-99-99
                let formattedValue = '+7';
                
                if (value.length > 1) {
                    formattedValue += ' (' + value.substring(1, 4);
                }
                if (value.length >= 5) {
                    formattedValue += ') ' + value.substring(4, 7);
                }
                if (value.length >= 8) {
                    formattedValue += '-' + value.substring(7, 9);
                }
                if (value.length >= 10) {
                    formattedValue += '-' + value.substring(9, 11);
                }
                
                e.target.value = formattedValue;
            });
            
            input.addEventListener('keydown', function(e) {
                if (e.key === 'Backspace' && e.target.value === '+7') {
                    e.preventDefault();
                }
            });
        });
    }

    /**
     * Ленивая загрузка изображений
     */
    function initLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.removeAttribute('data-src');
                        }
                        observer.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    /**
     * Анимация чисел (счетчики)
     */
    function animateValue(element, start, end, duration) {
        let startTimestamp = null;
        
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            element.textContent = Math.floor(progress * (end - start) + start);
            
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        
        window.requestAnimationFrame(step);
    }

    /**
     * Проверка видимости элемента
     */
    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    /**
     * Обработка CSRF токена для AJAX запросов
     */
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Экспорт утилит в глобальную область (если нужно)
    window.YarkoGorod = {
        getCookie: getCookie,
        animateValue: animateValue,
        isElementInViewport: isElementInViewport
    };

})();

/**
 * Обработка прелоадера (если есть)
 */
window.addEventListener('load', function() {
    const preloader = document.querySelector('.preloader');
    if (preloader) {
        preloader.classList.add('fade-out');
        setTimeout(() => {
            preloader.style.display = 'none';
        }, 300);
    }
});

/**
 * Консольное сообщение для разработчиков
 */
console.log('%cЯркий Город', 'font-size: 24px; font-weight: bold; color: #F8D12C;');
console.log('%cРекламное агентство полного цикла', 'font-size: 14px; color: #2C3E50;');
console.log('🎨 Сайт разработан с ❤️');

