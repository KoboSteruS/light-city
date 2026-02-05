/**
 * Скрывает предупреждение о версии CKEditor
 */
(function() {
    'use strict';
    
    function hideCKEditorWarning() {
        // Ищем предупреждение CKEditor по тексту
        const warningElements = document.querySelectorAll('div, span, p');
        
        for (let i = 0; i < warningElements.length; i++) {
            const element = warningElements[i];
            const text = element.textContent || element.innerText;
            
            // Проверяем, содержит ли элемент предупреждение о версии CKEditor
            if (text.includes('CKEditor') && text.includes('not secure') && text.includes('version')) {
                // Скрываем элемент
                element.style.display = 'none';
                element.remove(); // Полностью удаляем из DOM
            }
        }
        
        // Также проверяем через CKEDITOR API, если он доступен
        if (typeof CKEDITOR !== 'undefined') {
            // Отключаем проверку версии через API
            if (CKEDITOR.config) {
                CKEDITOR.config.versionCheck = false;
            }
            
            // Слушаем события создания редактора
            CKEDITOR.on('instanceReady', function() {
                hideCKEditorWarning();
            });
        }
    }
    
    // Запускаем сразу при загрузке
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', hideCKEditorWarning);
    } else {
        hideCKEditorWarning();
    }
    
    // Также запускаем через небольшую задержку на случай, если CKEditor загружается асинхронно
    setTimeout(hideCKEditorWarning, 1000);
    setTimeout(hideCKEditorWarning, 2000);
    setTimeout(hideCKEditorWarning, 3000);
    
    // Используем MutationObserver для отслеживания динамически добавляемых элементов
    if (typeof MutationObserver !== 'undefined') {
        const observer = new MutationObserver(function(mutations) {
            hideCKEditorWarning();
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
})();
