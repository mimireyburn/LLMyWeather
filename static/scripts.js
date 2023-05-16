document.addEventListener("DOMContentLoaded", function () {
  adjustFontSize();
});

function adjustFontSize() {
  const element = document.getElementById("screen-text");
  const text = element.innerHTML;

  let fontSize = 0;

  if (text.includes("<br>")) {
    const sentences = text.split("<br>");
    let maxSentenceLength = 0;

    sentences.forEach((sentence) => {
      if (sentence.length > maxSentenceLength) {
        maxSentenceLength = sentence.length;
      }
    });

    if (maxSentenceLength > 0) {
      fontSize = 600 / maxSentenceLength; // coefficient for sentence length
    }
  } else {
    const length = text.length;

    if (length > 0) {
      fontSize = 2600 / length; // coefficient for total text length
    }
  }

  element.style.fontSize = `${fontSize}px`;
}
