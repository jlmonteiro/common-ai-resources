document.addEventListener("DOMContentLoaded", function () {
  var siteHost = window.location.hostname;
  document.querySelectorAll('a[href^="https://"]').forEach(function (a) {
    if (a.hostname !== siteHost) {
      a.setAttribute("target", "_blank");
      a.setAttribute("rel", "noopener noreferrer");
    }
  });
});
