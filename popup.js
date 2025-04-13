document.addEventListener('DOMContentLoaded', function() {
    const targetSelectorInput = document.getElementById('targetSelector');
    const intervalInput = document.getElementById('interval');
    const toggleButton = document.getElementById('toggleButton');
    const statusDiv = document.getElementById('status');
    
    // Загружаем сохраненные настройки
    chrome.storage.local.get(['targetSelector', 'interval', 'isActive'], function(data) {
      if (data.targetSelector) targetSelectorInput.value = data.targetSelector;
      if (data.interval) intervalInput.value = data.interval;
      
      if (data.isActive) {
        statusDiv.textContent = 'Мониторинг активен';
        statusDiv.className = 'status active';
        toggleButton.textContent = 'Остановить мониторинг';
      }
    });
    
    // Обработчик кнопки
    toggleButton.addEventListener('click', function() {
      chrome.storage.local.get(['isActive'], function(data) {
        const newState = !data.isActive;
        
        // Сохраняем новые настройки
        chrome.storage.local.set({
          targetSelector: targetSelectorInput.value,
          interval: parseInt(intervalInput.value) || 30,
          isActive: newState
        });
        
        if (newState) {
          statusDiv.textContent = 'Мониторинг активен';
          statusDiv.className = 'status active';
          toggleButton.textContent = 'Остановить мониторинг';
          
          // Перезагружаем текущую вкладку для запуска мониторинга
          chrome.tabs.reload();
        } else {
          statusDiv.textContent = 'Мониторинг неактивен';
          statusDiv.className = 'status inactive';
          toggleButton.textContent = 'Запустить мониторинг';
        }
      });
    });
  });
  
  // Прослушиваем сообщения от content.js
  chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'elementsFound') {
      alert(`Найдено элементов: ${request.count}`);
    }
  });