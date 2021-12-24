const add_tag_btn = document.querySelector('#add-tag-btn');
const add_tag_form = document.querySelector('#add-tag-form');
const form_close_btn = add_tag_form.querySelector('.close-btn');

/* Creates a new tag which renders when request to the 
  server is successfull to avoid reloading of page to 
  get updated data. */
function create_tag(tag_text) {
  const tag = document.createElement("span");
  tag.classList.add("tag");
  let tag_content = `<span class="tag-text">${tag_text}</span>`;
  tag.innerHTML = tag_content;
  return tag;
}

// Send data to server asynchronously through AJAX.
add_tag_form.onsubmit = () => {
  const tag = document.querySelector('#tag-name').value;
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/admin/products/tags/add", true);

  xhr.onreadystatechange = function() {
    if(this.readyState == 4) {
      // On successfull request.
      if(this.status == 200) {
        /* Increasing the count of tags by 1. Since request
          is sent throught AJAX. Avoids the need for new request
          to see updated content */
        let cnt = document.querySelector("#tags-cnt").innerHTML;
        cnt = parseInt(cnt, 10);
        cnt += 1
        document.querySelector("#tags-cnt").innerHTML = cnt;

        // Appending the new tag to aldready displayed tags.
        const new_tag = create_tag(tag);
        document.querySelector(".food_tags").appendChild(new_tag);
        alert('Tag added successfully')
        close_component(add_tag_form);
      }
      else {
        let resp = JSON.parse(this.responseText);
        alert(resp.msg);
      }
    }
  };

  let form_data = new FormData();
  form_data.append('name', tag);

  xhr.send(form_data);
  return false;
}

add_tag_btn.onclick = () => toggle_component(add_tag_form);
form_close_btn.onclick = () => close_component(add_tag_form);
window.onclick = (event) => {
  if(event.target == modal_bg && 
      add_tag_form.classList.contains("toggle"))
      close_component(add_tag_form)
}