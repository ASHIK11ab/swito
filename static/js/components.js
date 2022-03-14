/* This javascript adds the functionalities to the dynamically
created components */

// Creates and returns notification component.
function create_notification(text, status) {
  let icon_select = {
    'success': 'tick',
    'failure': 'close-btn',
    'warning': 'warning'
  };

  const icon = icon_select[status];

  const notification = document.createElement('div');
  notification.classList.add('notification', status);
  notification.innerHTML = 
      `<div class="border"></div>` +
      `<i class="icon ${icon}-icon"></i>` +
      `<span class="notification-text">${text}</span>` +
      `<span id="close-notification-btn">&times;</span>`;
  return notification;
}
    

function toggle_notification(notification) {
  // Add the notification component to the DOM.
  notification.classList.add('toggle');
  document.body.appendChild(notification);

  notification.querySelector('#close-notification-btn').onclick = () => {
    notification.classList.remove('toggle');
  }

  // Auto remove notification after 6 seconds.
  setTimeout(() => {notification.remove();}, 6000);
}