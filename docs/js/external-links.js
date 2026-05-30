document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll('a[href^="https://"]').forEach(function (a) {
    a.setAttribute("target", "_blank");
    a.setAttribute("rel", "noopener noreferrer");
  });
});
