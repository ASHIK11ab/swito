const sidebar = document.getElementById("app-sidebar");
const sidebar_toggle_btn = document.getElementById("sidebar-toggle-btn");
const mobile_sidebar_toggle_btn = document.getElementById("mobile-sidebar-toggle-btn");
const sidebar_close_btn = document.getElementById("sidebar-close-btn");
const search_form = document.getElementById("search-form")
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


// Creates the food section using the foods data.
function create_foods_section(foods) {
  const section = document.createElement('section');
  section.setAttribute('class', 'foods-section');
  section.innerHTML += 
  `<h2 class="section-title">Recommended For You</h2>`;

  let foods_container = "";
  // Dynamically creates list of food cards.
  for(const food of foods) {
    foods_container +=
    `<div class="food-card" data-food-id="${food.id}">` +
      `<div class="food-image">` +
        `<img src="${food.img_url}" alt="${food.name}" image - Swito">` +
      `</div>` +
      `<div class="card-body">` +
        `<span class="food-name">${food.name}</span>` +
        `<span class="food-tag">${food.tag}</span>` +
        `<span class="food-price">${food.price}</span>` +
      `</div>` +
    `</div>`;
  }

  section.innerHTML += `<div class="foods">${foods_container}</div>`;
  return section
}


search_form.onsubmit = function() {
  let xhr = new XMLHttpRequest();
  xhr.open('POST', '/dashboard', true)
  xhr.onreadystatechange = function() {
    if(this.readyState == 4 && this.status == 200) {
      const resp = JSON.parse(this.responseText);
      const main_container = document.querySelector('.main-container');
      const section = create_foods_section(resp);
      main_container.appendChild(section)
    }
  }

  let formData = new FormData();
  const query = document.getElementById("query").value;
  formData.append("query", query);

  xhr.send(formData);
  return false;
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