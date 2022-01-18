const sidebar = document.getElementById("app-sidebar");
const sidebar_toggle_btn = document.getElementById("sidebar-toggle-btn");
const mobile_sidebar_toggle_btn = document.getElementById("mobile-sidebar-toggle-btn");
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


// Toggle and close sidebar's when the respective buttons are clicked.
sidebar_toggle_btn.onclick = () => toggle_component(sidebar);
mobile_sidebar_toggle_btn.onclick = () => toggle_component(sidebar);
sidebar_close_btn.onclick = () => close_component(sidebar);


// Close the sidebar when user clicks away from the sidebar when it is open.
window.addEventListener('click', (event) => {
  if(event.target == modal_bg && 
      sidebar.classList.contains('toggle'))
    close_component(sidebar);
});


// Attaches event listener for the foods which has a class name `food-card`.
function create_event_listeners_foods() {
  const foods = document.querySelectorAll('.food-card');
  foods.forEach((food) => food.addEventListener('click', function() {
    window.location = document.location.origin +
                        `/dashboard/foods/${food.dataset.foodId}`;
  }));
}


// Attach event listeners to the food cards when the DOM is loaded.
window.addEventListener('DOMContentLoaded', create_event_listeners_foods); 