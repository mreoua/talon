document.addEventListener('DOMContentLoaded', function() {
    const targetSelectorInput = document.getElementById('targetSelector');
    const intervalInput = document.getElementById('interval');
    const toggleButton = document.getElementById('toggleButton');
    const checkAudioButton = document.getElementById('checkAudioButton');
    const statusDiv = document.getElementById('status');
    const ajaxUrlInput = document.getElementById('ajaxUrl');
    const targetServiceCenterInput = document.getElementById('targetServiceCenter');
    
    // Загружаем сохраненные настройки
  chrome.storage.local.get([
    'interval', 
    'isActive', 
    'ajaxUrl',
    'targetServiceCenter'
  ], function(data) {
    if (data.interval) intervalInput.value = data.interval;
    if (data.ajaxUrl) ajaxUrlInput.value = data.ajaxUrl;
    if (data.targetServiceCenter) targetServiceCenterInput.value = data.targetServiceCenter;
    
    
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
        
        chrome.storage.local.set({
            interval: parseInt(intervalInput.value) || 30,
            ajaxUrl: ajaxUrlInput.value,
            targetServiceCenter: targetServiceCenterInput.value,
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

  checkAudioButton.addEventListener('click', function() {
        const audio = new Audio(chrome.runtime.getURL('audio/alarm.mp3'));
        audio.play();
  });
  
  // Прослушиваем сообщения от content.js
  chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'elementsFound') {
      alert(`Найдено элементов: ${request.count}`);
    }
  });