// Загрузка настроек из хранилища
chrome.storage.local.get([
    'interval', 
    'isActive', 
    'ajaxUrl',
    'targetServiceCenter'
], function(data) {
    // Если мониторинг активен
    if (data.isActive) {
        executeAjaxRequest(data.ajaxUrl, data.targetServiceCenter)
        .then(result => {
          console.log('AJAX ответ обработан:', result);
          
          if (result.found) {
            console.log('НАЙДЕН ЦЕЛЕВОЙ СЕРВИСНЫЙ ЦЕНТР:', result.serviceCenterData);
            
            // Воспроизводим звуковой сигнал
            const audio = new Audio(chrome.runtime.getURL('audio/alert.mp3'));
            audio.play();
            
          }
          
          // Устанавливаем интервал для перезагрузки страницы
          setTimeout(() => {
            location.reload();
          }, data.interval * 1000);
        })
        .catch(error => {
          console.error('Ошибка AJAX запроса:', error);
          
          setTimeout(() => {
            location.reload();
          }, data.interval * 1000);
        });
    }
  });

  function executeAjaxRequest(url, targetServiceCenter) {
    return new Promise((resolve, reject) => {
      const eventName = 'ajaxResponse_' + Math.random().toString(36).substring(2);
  
      document.addEventListener(eventName, function handler(e) {
        const detail = e.detail;
        if (detail.error) {
          reject(new Error(detail.error));
        } else {
          const centers = Array.isArray(detail.response)
            ? detail.response
            : detail.response?.data || [detail.response];
  
          const foundCenter = centers.find(c => c?.srvCenterName?.includes(targetServiceCenter));
          resolve({
            found: !!foundCenter,
            serviceCenterData: foundCenter,
            allCenters: centers
          });
        }
      }, { once: true });
  
      const script = document.createElement('script');
      script.src = chrome.runtime.getURL('injected.js');
      script.dataset.url = url;
      script.dataset.target = targetServiceCenter;
      script.dataset.event = eventName;
  
      (document.head || document.documentElement).appendChild(script);
      script.remove(); // удалим после выполнения
    });
  }
  
  