window.addEventListener('DOMContentLoaded', () => {
  // Get the similar foods asynchronously using AJAX.
  const xhr = new XMLHttpRequest();
  xhr.open("GET", `${document.location.pathname}?request-type=similar-foods`, true);
  xhr.onreadystatechange = function() {
    if(this.readyState == 4 && this.status == 200) {
      // Render the response to DOM.
      const resp = JSON.parse(this.responseText);
      const main_container = document.querySelector('.main-container');
      const section = create_foods_section(resp);
      main_container.appendChild(section);
      create_event_listeners_foods();
    }
  }
  xhr.send();
});