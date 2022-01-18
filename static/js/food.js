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