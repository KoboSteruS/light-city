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
        // Получаем данные из window.portfolioData
        if (window.portfolioData && window.portfolioData.items) {
            portfolioItems = window.portfolioData.items;
        } else {
            // Если данных нет, собираем их из DOM
            portfolioItems = Array.from(document.querySelectorAll('.portfolio-work-card')).map((card, index) => {
                const img = card.querySelector('.portfolio-work-image img');
                const title = card.querySelector('.portfolio-work-title')?.textContent.trim() || '';
                const description = card.querySelector('.portfolio-work-description')?.textContent.trim() || '';
                const service = card.querySelector('.portfolio-work-service')?.textContent.trim() || '';
                const client = card.querySelector('.portfolio-work-client span')?.textContent.trim() || '';
                
                return {
                    id: card.dataset.portfolioId || index,
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
                
                currentIndex = parseInt(this.dataset.portfolioIndex) || index;
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

        if (modalTitle) {
            modalTitle.textContent = item.title || '';
        }

        if (modalDescription) {
            modalDescription.textContent = item.description || '';
            modalDescription.style.display = item.description ? 'block' : 'none';
        }

        if (modalService) {
            modalService.textContent = item.service || '';
            modalService.style.display = item.service ? 'inline-block' : 'none';
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

        if (modalTitle) {
            modalTitle.textContent = item.title || '';
        }

        if (modalDescription) {
            modalDescription.textContent = item.description || '';
            modalDescription.style.display = item.description ? 'block' : 'none';
        }

        if (modalService) {
            modalService.textContent = item.service || '';
            modalService.style.display = item.service ? 'inline-block' : 'none';
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
