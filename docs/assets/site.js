// Theme toggle (auto -> light -> dark), copy buttons, and the docs sidebar on phones.
(function () {
  var root = document.documentElement;
  var KEY = "agent-org-theme";
  var order = ["auto", "light", "dark"];

  function read() {
    try { return localStorage.getItem(KEY) || "auto"; } catch (e) { return "auto"; }
  }
  function apply(mode) {
    if (mode === "auto") root.removeAttribute("data-theme");
    else root.setAttribute("data-theme", mode);
    var btn = document.querySelector(".theme-toggle");
    if (btn) btn.textContent = "Theme: " + mode;
  }
  apply(read());

  document.addEventListener("click", function (e) {
    var toggle = e.target.closest(".theme-toggle");
    if (toggle) {
      var next = order[(order.indexOf(read()) + 1) % order.length];
      try { localStorage.setItem(KEY, next); } catch (err) { /* private mode: still apply */ }
      apply(next);
      return;
    }
    var copy = e.target.closest(".copy");
    if (copy) {
      var pre = copy.parentElement.querySelector("pre");
      var text = pre ? pre.innerText.replace(/^\$ /gm, "") : "";
      var done = function () {
        copy.textContent = "Copied";
        copy.setAttribute("data-done", "");
        setTimeout(function () { copy.textContent = "Copy"; copy.removeAttribute("data-done"); }, 1600);
      };
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () { copy.textContent = "Select and copy"; });
      else copy.textContent = "Select and copy";
    }
  });

  // The docs sidebar ships open (desktop); collapse it on narrow screens.
  var side = document.querySelector(".side details");
  if (side && window.matchMedia("(max-width: 900px)").matches) {
    side.removeAttribute("open");
    side.addEventListener("click", function (e) {
      if (e.target.closest("a")) side.removeAttribute("open");
    });
  }
})();
