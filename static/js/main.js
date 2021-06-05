function display_dropdown() {
  let content = document.getElementById('content');
  if (content.className === 'close') {
    content.style.display = "block";
    content.className = 'open';
  }
  else {
    content.style.display = 'none';
    content.className = 'close'
  }

}