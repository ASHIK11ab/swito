const sidebar = document.getElementById("app-sidebar");
const sidebar_toggle_btn = document.getElementById("sidebar-toggle-btn");
const mobile_sidebar_toggle_btn = document.getElementById(
                                    "mobile-sidebar-toggle-btn");
const sidebar_close_btn = document.getElementById("sidebar-close-btn");
let modal_bg = undefined;

// Creates a semi-transparent background.
function create_modal_bg() {
  modal_bg = document.createElement("div");
  modal_bg.setAttribute("class", "modal-bg");
  document.body.appendChild(modal_bg);
}

// Removes the modal background.
function remove_modal_bg() {
  document.body.removeChild(modal_bg);
  modal_bg = undefined;
}

function toggle_component(component) {
  create_modal_bg();
  component.classList.add('toggle');
}

function close_component(component) {
  remove_modal_bg();
  component.classList.remove('toggle');
}

sidebar_toggle_btn.onclick = () => toggle_component(sidebar);
mobile_sidebar_toggle_btn.onclick = () => toggle_component(sidebar);
sidebar_close_btn.onclick = () => close_component(sidebar);

window.addEventListener('click', (event) => {
  if(event.target == modal_bg && 
      sidebar.classList.contains('toggle'))
    close_component(sidebar);
});