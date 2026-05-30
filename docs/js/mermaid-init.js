document.addEventListener("DOMContentLoaded", function () {
  mermaid.initialize({ startOnLoad: false });
  mermaid.run({ querySelector: ".mermaid code" });
});
