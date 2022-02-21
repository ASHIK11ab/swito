const buy_now_btn = document.querySelector('#buy-now-btn');
const add_to_cart_btn = document.querySelector('#add-to-cart-btn');
const food_id = document.querySelector('section.food').dataset.foodId;
const food_quantity = document.querySelector('#quantity-cnt');

buy_now_btn.onclick = function() {
  quantity = Number.parseInt(food_quantity.value);
  if(quantity < 1) {
    alert("Enter a minimum quantity of 1");
    return false;
  }
  
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/dashboard/orders/new", true);

  xhr.onreadystatechange = function() {
    if(this.readyState == 4) {
      console.log(this.responseText);
      const resp = JSON.parse(this.responseText);
      alert(resp.msg);
    }
  }

  let form_data = new FormData();
  form_data.append("food-id", food_id);
  form_data.append("quantity", quantity);

  xhr.send(form_data);
}


add_to_cart_btn.onclick = function() {
  quantity = Number.parseInt(food_quantity.value);
  if(quantity < 1) {
    alert("Enter a minimum quantity of 1");
    return false;
  }

  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/dashboard/cart/add", true);

  xhr.onreadystatechange = function() {
    if(this.readyState == 4) {
      const resp = JSON.parse(this.responseText);
      alert(resp.msg);
    }
  }

  let form_data = new FormData();
  form_data.append("food-id", food_id);
  form_data.append("quantity", quantity);

  xhr.send(form_data);
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