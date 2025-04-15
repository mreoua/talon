(function () {
    const currentScript = document.currentScript;
  
    const url = currentScript.dataset.url;
    const targetServiceCenter = currentScript.dataset.target;
    const eventName = currentScript.dataset.event;
  
    const dispatchResult = (detail) => {
      document.dispatchEvent(new CustomEvent(eventName, { detail }));
    };
  
    const handleResponse = (response) => {
      try {
        const parsed = typeof response === 'string' ? JSON.parse(response) : response;
        dispatchResult({ response: parsed });
      } catch (e) {
        dispatchResult({ response });
      }
    };
  
    if (!url || !eventName) return;
  
    if (typeof jQuery !== 'undefined') {
      jQuery.ajax({
        url,
        type: "GET",
        success: handleResponse,
        error: (_, __, error) => dispatchResult({ error: "AJAX error: " + error })
      });
    } else {
      const xhr = new XMLHttpRequest();
      xhr.open('GET', url, true);
      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          handleResponse(xhr.responseText);
        } else {
          dispatchResult({ error: "AJAX error: " + xhr.statusText });
        }
      };
      xhr.onerror = () => dispatchResult({ error: "AJAX network error" });
      xhr.send();
    }
  })();