const form = document.getElementById("add-product-form");
const add_product_toggle_btn = document.getElementById("add-product-toggle-btn");
const form_close_btn = document.querySelector("form .close-btn");
const tags_select = document.getElementById("tags_select");
const tags_container = document.getElementById("tags-container");

// Input fields values.
const food_name = document.getElementById("food-name");
const price = document.getElementById("price");
const quantity = document.getElementById("quantity");
const food_image = document.getElementById("image");


const create_food_tag = (tag_text) => {
  tag_text = tag_text.charAt(0).toUpperCase() + tag_text.slice(1);
  const tag = document.createElement("span");
  tag.classList.add("tag");
  let tag_content = `<span class="tag-text">${tag_text}</span>` +
    '<i class="close">&times;</i>';
  tag.innerHTML = tag_content;
  return tag;
}

add_product_toggle_btn.addEventListener('click', () => { toggle_component(form); });

form_close_btn.addEventListener('click', () => { close_component(form) });

// Dynamically create and add tags when tags are selected.
tags_select.onchange = function() {
  const selected_tags = parse_selected_tags();

  // Do nothing if the tag is aldreadly selected.
  if(selected_tags.includes(this.value)) {
    this.value = '';
    return false;
  }

  const tag = create_food_tag(this.value);
  tags_container.appendChild(tag);

  // Attach event listener to remove tag when close button is clicked.
  const tag_close_btn = tag.querySelector(".close");
  tag_close_btn.onclick =  () => { tags_container.removeChild(tag) };
  this.value = '';
};


// Parse selected tags.
function parse_selected_tags() {
  const selected_tags = new Array();
  const tags = tags_container.querySelectorAll(".tag > .tag-text");
  for(const tag of tags) 
    selected_tags.push(tag.innerHTML);
  return selected_tags;
}


form.onsubmit = () => {
  const food_tags = parse_selected_tags();
  let xhr = new XMLHttpRequest();
  xhr.open("POST", "/admin/foods/add", true);
  xhr.onreadystatechange = function() {
    if(this.readyState == 4) {
      if(this.status == 200) {
        // Once food is added clear all input field and selected tags.
        form.querySelectorAll('input').forEach((field) => field.value = '');
        tags_container.querySelectorAll('.tag').forEach((tag) => tag.remove());
      }
      const resp = JSON.parse(this.responseText);
      alert(resp.msg);
    }
  }

  let form_data = new FormData();
  form_data.append("name", food_name.value);
  form_data.append("quantity", quantity.value);
  form_data.append("price", price.value);
  form_data.append("tags", food_tags);
  form_data.append("image", food_image.files[0]);
  xhr.send(form_data);
  return false;
}


window.addEventListener('click', (event) => {
  if(event.target == modal_bg && 
      form.classList.contains('toggle'))
    close_component(form);
});