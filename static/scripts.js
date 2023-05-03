document.addEventListener("DOMContentLoaded", function () {
  adjustFontSize();
});

function adjustFontSize() {
  const element = document.getElementById("overlay-text");
  const text = element.innerHTML;

  const length = text.length;
  let fontSize = 16; // Default font size in pixels.

  if (length > 0) {
    fontSize = 2600 / length;
  }

  element.style.fontSize = `${fontSize}px`;
}
