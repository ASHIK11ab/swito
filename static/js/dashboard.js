const sidebar = document.getElementById("app-sidebar");
const sidebar_toggle_btn = document.getElementById("sidebar-toggle-btn");
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

function toggle_sidebar() {
  create_modal_bg();
  sidebar.classList.add("toggle-sidebar-left");
}

function close_sidebar() {
  remove_modal_bg();
  sidebar.classList.remove("toggle-sidebar-left");
}

sidebar_toggle_btn.addEventListener("click", toggle_sidebar);
sidebar_close_btn.addEventListener("click", close_sidebar);