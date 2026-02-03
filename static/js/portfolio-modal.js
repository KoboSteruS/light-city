/**
 * Модальное окно для просмотра работ портфолио
 * 
 * Функционал:
 * - Открытие модального окна при клике на карточку
 * - Переключение работ стрелками влево/вправо
 * - Учет фильтров (показываются только работы из текущего списка)
 * - Навигация клавиатурой (стрелки влево/вправо, Escape)
 */

(function() {
    'use strict';

    let currentIndex = 0;
    let portfolioItems = [];

    /**
     * Инициализация модального окна
     */
    function initPortfolioModal() {
        console.log('Initializing portfolio modal...');
        
        // Получаем данные из window.portfolioData (приоритет)
        if (window.portfolioData && window.portfolioData.items && Array.isArray(window.portfolioData.items) && window.portfolioData.items.length > 0) {
            portfolioItems = window.portfolioData.items;
            console.log('Loaded from window.portfolioData:', portfolioItems.length, 'items');
        } else {
            console.log('window.portfolioData not found or empty');
            return;
        }

        // Если работ нет, выходим
        if (!portfolioItems || portfolioItems.length === 0) {
            console.log('No portfolio items found');
            return;
        }

        const modal = document.getElementById('portfolioModal');
        if (!modal) {
            console.error('Modal element not found');
            return;
        }

        // Обработчики для карточек
        const cards = document.querySelectorAll('.portfolio-work-card');
        console.log('Found', cards.length, 'portfolio cards');
        
        cards.forEach((card, index) => {
            card.style.cursor = 'pointer';
            
            card.addEventListener('click', function(e) {
                console.log('=== CARD CLICKED ===');
                console.log('Card:', this);
                console.log('Target:', e.target);
                console.log('Dataset:', this.dataset);
                
                // Не открываем модалку, если клик по ссылке внутри
                if (e.target.tagName === 'A' || e.target.closest('a')) {
                    console.log('Click on link, ignoring');
                    return;
                }
                
                // Не открываем, если клик по кнопке или интерактивному элементу
                if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
                    console.log('Click on button, ignoring');
                    return;
                }
                
                e.preventDefault();
                e.stopPropagation();
                
                // Находим индекс работы в общем массиве portfolioData
                // Сначала пробуем найти по ID
                let portfolioId = null;
                const portfolioIdAttr = this.getAttribute('data-portfolio-id');
                if (portfolioIdAttr) {
                    portfolioId = parseInt(portfolioIdAttr, 10);
                }
                
                console.log('Portfolio ID from attribute:', portfolioIdAttr);
                console.log('Portfolio ID parsed:', portfolioId);
                console.log('Portfolio items count:', portfolioItems.length);
                
                // Если ID валидный, ищем по ID
                if (portfolioId && !isNaN(portfolioId)) {
                    currentIndex = portfolioItems.findIndex(item => {
                        const itemId = typeof item.id === 'string' ? parseInt(item.id, 10) : item.id;
                        return itemId === portfolioId;
                    });
                    console.log('Found index by ID:', currentIndex);
                } else {
                    currentIndex = -1;
                    console.log('No valid ID, will use DOM index');
                }
                
                // Если не нашли по ID, используем fallback - индекс в DOM
                if (currentIndex === -1) {
                    const allCards = Array.from(document.querySelectorAll('.portfolio-work-card'));
                    const domIndex = allCards.indexOf(this);
                    console.log('Not found by ID, DOM index:', domIndex);
                    
                    // Если индекс в DOM валидный и соответствует portfolioItems
                    if (domIndex >= 0 && domIndex < portfolioItems.length) {
                        currentIndex = domIndex;
                        console.log('Using DOM index:', currentIndex);
                    } else {
                        // Последний fallback - используем 0
                        currentIndex = 0;
                        console.log('Using fallback index 0');
                    }
                }
                
                // Проверяем, что индекс валидный
                if (currentIndex < 0 || currentIndex >= portfolioItems.length) {
                    console.error('Invalid index:', currentIndex, 'Total items:', portfolioItems.length);
                    // Попробуем открыть с индексом 0
                    if (portfolioItems.length > 0) {
                        console.log('Trying to open with index 0');
                        currentIndex = 0;
                    } else {
                        return;
                    }
                }
                
                console.log('Final index:', currentIndex);
                console.log('Item:', portfolioItems[currentIndex]);
                console.log('Calling openModal...');
                openModal(currentIndex);
            });
        });

        // Обработчики для стрелок навигации
        const prevBtn = document.getElementById('portfolioModalPrev');
        const nextBtn = document.getElementById('portfolioModalNext');

        if (prevBtn) {
            prevBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                navigateToPrev();
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                navigateToNext();
            });
        }

        // Обработка клавиатуры
        document.addEventListener('keydown', function(e) {
            if (!modal.classList.contains('show')) {
                return;
            }

            if (e.key === 'ArrowLeft') {
                e.preventDefault();
                navigateToPrev();
            } else if (e.key === 'ArrowRight') {
                e.preventDefault();
                navigateToNext();
            } else if (e.key === 'Escape') {
                // Bootstrap сам закроет модалку
            }
        });

        // Обновление состояния стрелок при открытии модалки
        modal.addEventListener('show.bs.modal', function() {
            updateNavigationButtons();
        });

        modal.addEventListener('shown.bs.modal', function() {
            // Фокус на модалке для работы клавиатуры
            modal.focus();
        });
    }

    /**
     * Открытие модального окна с указанной работой
     */
    function openModal(index) {
        console.log('openModal called with index:', index);
        
        if (index < 0 || index >= portfolioItems.length) {
            console.error('Invalid index in openModal:', index);
            return;
        }

        currentIndex = index;
        const item = portfolioItems[currentIndex];
        console.log('Opening modal for item:', item);

        // Обновляем содержимое модалки
        const modalImage = document.getElementById('portfolioModalImage');
        const modalTitle = document.getElementById('portfolioModalTitle');
        const modalDescription = document.getElementById('portfolioModalDescription');
        const modalService = document.getElementById('portfolioModalService');
        const modalClient = document.getElementById('portfolioModalClient');

        if (modalImage) {
            modalImage.src = item.image || '';
            modalImage.alt = item.title || 'Работа';
        }

        // Формируем понятное название для пользователя
        if (modalTitle) {
            let displayTitle = item.title || '';
            // Если название выглядит как техническое (содержит # или "Пример работы"), заменяем на более понятное
            if (displayTitle.includes('#') || displayTitle.toLowerCase().includes('пример')) {
                // Используем название услуги, если есть
                if (item.service) {
                    displayTitle = item.service;
                } else {
                    // Или просто убираем технические части
                    displayTitle = displayTitle.replace(/#\d+/g, '').replace(/пример работы:/gi, '').trim();
                    if (!displayTitle) {
                        displayTitle = 'Наша работа';
                    }
                }
            }
            // Если title все еще пустой, используем название услуги или дефолтное значение
            if (!displayTitle) {
                displayTitle = item.service || 'Наша работа';
            }
            modalTitle.textContent = displayTitle;
        }

        // Очищаем описание от технических комментариев
        if (modalDescription) {
            let description = item.description || '';
            // Убираем HTML теги (если остались после striptags)
            description = description.replace(/<[^>]*>/g, '');
            // Убираем технические фразы
            description = description.replace(/пример работы:.*?[\.\n]/gi, '');
            description = description.replace(/пример работы.*?[\.\n]/gi, '');
            description = description.trim();
            
            // Нормализуем сравнение - убираем лишние пробелы и приводим к нижнему регистру
            const normalizedDescription = description.toLowerCase().trim();
            const normalizedService = (item.service || '').toLowerCase().trim();
            
            // Если описание пустое, совпадает с названием услуги или содержит только название услуги, не показываем его
            if (!description || normalizedDescription === normalizedService || (normalizedDescription.includes(normalizedService) && normalizedDescription.length <= normalizedService.length + 5)) {
                modalDescription.style.display = 'none';
            } else {
                modalDescription.textContent = description;
                modalDescription.style.display = 'block';
            }
        }

        // Бейдж услуги - показываем только если название услуги отличается от заголовка
        if (modalService) {
            const titleText = modalTitle ? modalTitle.textContent : '';
            // Показываем бейдж только если название услуги отличается от заголовка
            if (item.service && item.service !== titleText) {
                modalService.textContent = item.service;
                modalService.style.display = 'inline-block';
            } else {
                modalService.style.display = 'none';
            }
        }

        if (modalClient) {
            if (item.client) {
                modalClient.innerHTML = '<i class="bi bi-briefcase"></i> <span>' + item.client + '</span>';
                modalClient.style.display = 'flex';
            } else {
                modalClient.style.display = 'none';
            }
        }

        // Открываем модалку
        const modal = document.getElementById('portfolioModal');
        if (modal) {
            console.log('Showing Bootstrap modal');
            
            // Проверяем, есть ли Bootstrap
            if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
                // Используем существующий экземпляр или создаем новый
                let bsModal = bootstrap.Modal.getInstance(modal);
                if (!bsModal) {
                    bsModal = new bootstrap.Modal(modal, {
                        backdrop: true,
                        keyboard: true,
                        focus: true
                    });
                }
                bsModal.show();
            } else {
                // Fallback: открываем через классы
                console.log('Bootstrap not found, using fallback');
                modal.classList.add('show');
                modal.style.display = 'block';
                document.body.classList.add('modal-open');
                const backdrop = document.createElement('div');
                backdrop.className = 'modal-backdrop fade show';
                document.body.appendChild(backdrop);
            }
        } else {
            console.error('Modal element not found in openModal');
        }

        updateNavigationButtons();
    }

    /**
     * Переход к предыдущей работе
     */
    function navigateToPrev() {
        if (portfolioItems.length === 0) {
            return;
        }

        currentIndex = (currentIndex - 1 + portfolioItems.length) % portfolioItems.length;
        updateModalContent();
        updateNavigationButtons();
    }

    /**
     * Переход к следующей работе
     */
    function navigateToNext() {
        if (portfolioItems.length === 0) {
            return;
        }

        currentIndex = (currentIndex + 1) % portfolioItems.length;
        updateModalContent();
        updateNavigationButtons();
    }

    /**
     * Обновление содержимого модального окна
     */
    function updateModalContent() {
        if (currentIndex < 0 || currentIndex >= portfolioItems.length) {
            return;
        }

        const item = portfolioItems[currentIndex];

        const modalImage = document.getElementById('portfolioModalImage');
        const modalTitle = document.getElementById('portfolioModalTitle');
        const modalDescription = document.getElementById('portfolioModalDescription');
        const modalService = document.getElementById('portfolioModalService');
        const modalClient = document.getElementById('portfolioModalClient');

        if (modalImage) {
            // Плавная смена изображения
            modalImage.style.opacity = '0';
            setTimeout(() => {
                modalImage.src = item.image || '';
                modalImage.alt = item.title || 'Работа';
                modalImage.style.opacity = '1';
            }, 150);
        }

        // Формируем понятное название для пользователя
        if (modalTitle) {
            let displayTitle = item.title || '';
            // Если название выглядит как техническое (содержит # или "Пример работы"), заменяем на более понятное
            if (displayTitle.includes('#') || displayTitle.toLowerCase().includes('пример')) {
                // Используем название услуги, если есть
                if (item.service) {
                    displayTitle = item.service;
                } else {
                    // Или просто убираем технические части
                    displayTitle = displayTitle.replace(/#\d+/g, '').replace(/пример работы:/gi, '').trim();
                    if (!displayTitle) {
                        displayTitle = 'Наша работа';
                    }
                }
            }
            // Если title все еще пустой, используем название услуги или дефолтное значение
            if (!displayTitle) {
                displayTitle = item.service || 'Наша работа';
            }
            modalTitle.textContent = displayTitle;
        }

        // Очищаем описание от технических комментариев
        if (modalDescription) {
            let description = item.description || '';
            // Убираем HTML теги (если остались после striptags)
            description = description.replace(/<[^>]*>/g, '');
            // Убираем технические фразы
            description = description.replace(/пример работы:.*?[\.\n]/gi, '');
            description = description.replace(/пример работы.*?[\.\n]/gi, '');
            description = description.trim();
            
            // Нормализуем сравнение - убираем лишние пробелы и приводим к нижнему регистру
            const normalizedDescription = description.toLowerCase().trim();
            const normalizedService = (item.service || '').toLowerCase().trim();
            
            // Если описание пустое, совпадает с названием услуги или содержит только название услуги, не показываем его
            if (!description || normalizedDescription === normalizedService || (normalizedDescription.includes(normalizedService) && normalizedDescription.length <= normalizedService.length + 5)) {
                modalDescription.style.display = 'none';
            } else {
                modalDescription.textContent = description;
                modalDescription.style.display = 'block';
            }
        }

        // Бейдж услуги - показываем только если название услуги отличается от заголовка
        if (modalService) {
            const titleText = modalTitle ? modalTitle.textContent : '';
            // Показываем бейдж только если название услуги отличается от заголовка
            if (item.service && item.service !== titleText) {
                modalService.textContent = item.service;
                modalService.style.display = 'inline-block';
            } else {
                modalService.style.display = 'none';
            }
        }

        if (modalClient) {
            if (item.client) {
                modalClient.innerHTML = '<i class="bi bi-briefcase"></i> <span>' + item.client + '</span>';
                modalClient.style.display = 'flex';
            } else {
                modalClient.style.display = 'none';
            }
        }
    }

    /**
     * Обновление состояния кнопок навигации
     */
    function updateNavigationButtons() {
        const prevBtn = document.getElementById('portfolioModalPrev');
        const nextBtn = document.getElementById('portfolioModalNext');

        if (portfolioItems.length <= 1) {
            // Если работа одна, скрываем стрелки
            if (prevBtn) prevBtn.style.display = 'none';
            if (nextBtn) nextBtn.style.display = 'none';
        } else {
            // Показываем стрелки
            if (prevBtn) prevBtn.style.display = 'flex';
            if (nextBtn) nextBtn.style.display = 'flex';
        }
    }

    // Инициализация при загрузке DOM
    console.log('Portfolio modal script loaded');
    
    // Делаем функцию доступной глобально для вызова из inline-скрипта
    window.initPortfolioModal = initPortfolioModal;
    
    // Уведомляем, что скрипт готов
    window.dispatchEvent(new Event('portfolioModalReady'));
    
    // Также пробуем инициализировать автоматически
    function initialize() {
        console.log('Auto-initializing portfolio modal...');
        console.log('Document ready state:', document.readyState);
        console.log('Window portfolioData:', window.portfolioData);
        
        // Ждем немного, чтобы убедиться, что все готово
        setTimeout(function() {
            console.log('Starting auto-initialization after delay...');
            if (window.portfolioData && window.portfolioData.items && window.portfolioData.items.length > 0) {
                console.log('Portfolio data available:', window.portfolioData.items.length, 'items');
            } else {
                console.warn('Portfolio data not available, will try to collect from DOM');
            }
            initPortfolioModal();
        }, 100);
    }

    // Проверяем состояние документа
    if (document.readyState === 'loading') {
        console.log('Document is loading, waiting for DOMContentLoaded...');
        document.addEventListener('DOMContentLoaded', function() {
            console.log('DOMContentLoaded fired');
            initialize();
        });
    } else {
        console.log('Document already loaded, auto-initializing...');
        initialize();
    }

})();
