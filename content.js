// Загрузка настроек из хранилища
chrome.storage.local.get(['targetSelector', 'interval', 'isActive'], function(data) {
    // Если мониторинг активен
    if (data.isActive) {
      // Проверяем наличие целевых элементов
      checkForTargetElements(data.targetSelector);
      
      // Устанавливаем интервал для перезагрузки страницы
      setTimeout(() => {
        location.reload();
      }, data.interval * 1000);
    }
  });
  
  // Функция для проверки наличия целевых элементов
  function checkForTargetElements(selector) {
    if (!selector) return;
    
    const elements = document.querySelectorAll(selector);
    
    if (elements && elements.length > 0) {
      // Найдены целевые элементы
      console.log('Найдены целевые элементы:', elements);
      
      // Воспроизводим звуковой сигнал
      const audio = new Audio(chrome.runtime.getURL('audio/alert.mp3'));
      audio.play();
      
      // Отправляем уведомление в popup
      chrome.runtime.sendMessage({
        action: 'elementsFound',
        count: elements.length
      });
    }
  }