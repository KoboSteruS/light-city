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
        // Получаем данные из window.portfolioData (приоритет)
        if (window.portfolioData && window.portfolioData.items && window.portfolioData.items.length > 0) {
            portfolioItems = window.portfolioData.items;
        } else {
            // Если данных нет, собираем их из DOM
            // Поддерживаем оба формата: обычные карточки и grid-элементы
            portfolioItems = Array.from(document.querySelectorAll('.portfolio-work-card')).map((card, index) => {
                // Проверяем, это grid-элемент или обычная карточка
                const isGridItem = card.classList.contains('portfolio-album-item');
                let img, title, description, service, client;
                
                if (isGridItem) {
                    // Для grid-элементов пытаемся найти данные в window.portfolioData по ID
                    const portfolioId = parseInt(card.dataset.portfolioId);
                    if (portfolioId && window.portfolioData && window.portfolioData.items) {
                        const dataItem = window.portfolioData.items.find(item => item.id === portfolioId);
                        if (dataItem) {
                            title = dataItem.title || '';
                            description = dataItem.description || '';
                            service = dataItem.service || '';
                            client = dataItem.client || '';
                        }
                    }
                    img = card.querySelector('img');
                } else {
                    // Для обычных карточек берем из DOM
                    img = card.querySelector('.portfolio-work-image img');
                    title = card.querySelector('.portfolio-work-title')?.textContent.trim() || '';
                    description = card.querySelector('.portfolio-work-description')?.textContent.trim() || '';
                    service = card.querySelector('.portfolio-work-service')?.textContent.trim() || '';
                    client = card.querySelector('.portfolio-work-client span')?.textContent.trim() || '';
                }
                
                return {
                    id: parseInt(card.dataset.portfolioId) || index,
                    title: title,
                    description: description,
                    image: img ? img.src : '',
                    service: service,
                    client: client
                };
            });
        }

        // Если работ нет, выходим
        if (portfolioItems.length === 0) {
            return;
        }

        const modal = document.getElementById('portfolioModal');
        if (!modal) {
            return;
        }

        // Обработчики для карточек
        document.querySelectorAll('.portfolio-work-card').forEach((card, index) => {
            card.style.cursor = 'pointer';
            card.addEventListener('click', function(e) {
                // Не открываем модалку, если клик по ссылке внутри
                if (e.target.tagName === 'A' || e.target.closest('a')) {
                    return;
                }
                
                // Не открываем, если клик по кнопке или интерактивному элементу
                if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
                    return;
                }
                
                // Находим индекс работы в общем массиве portfolioData
                const portfolioId = parseInt(this.dataset.portfolioId);
                if (portfolioId && window.portfolioData && window.portfolioData.items) {
                    // Ищем по ID в window.portfolioData
                    currentIndex = window.portfolioData.items.findIndex(item => item.id === portfolioId);
                    if (currentIndex === -1) {
                        // Если не нашли по ID, пробуем по индексу
                        currentIndex = parseInt(this.dataset.portfolioIndex) || index;
                    }
                } else {
                    currentIndex = parseInt(this.dataset.portfolioIndex) || index;
                }
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
        const bsModal = new bootstrap.Modal(modal);
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
        if (index < 0 || index >= portfolioItems.length) {
            return;
        }

        currentIndex = index;
        const item = portfolioItems[currentIndex];

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
            const bsModal = new bootstrap.Modal(modal);
            bsModal.show();
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
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initPortfolioModal);
    } else {
        initPortfolioModal();
    }

})();
