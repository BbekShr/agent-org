// Theme toggle (dark <-> light), copy buttons, section reveal, and the docs sidebar on phones.
(function () {
  var root = document.documentElement;
  var KEY = "agent-org-theme";
  var order = ["dark", "light"];

  function read() {
    try { return localStorage.getItem(KEY) === "light" ? "light" : "dark"; } catch (e) { return "dark"; }
  }
  function apply(mode) {
    if (mode === "light") root.setAttribute("data-theme", "light");
    else root.removeAttribute("data-theme");
    var btn = document.querySelector(".theme-toggle");
    if (btn) btn.textContent = "theme: " + mode;
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

  // Sections fade up as they arrive; with reduced motion the CSS leaves them visible.
  var revealed = document.querySelectorAll(".reveal");
  if (revealed.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -10% 0px", threshold: 0.08 });
    revealed.forEach(function (el) { io.observe(el); });
  } else {
    revealed.forEach(function (el) { el.classList.add("in"); });
  }

  // The docs sidebar ships open (desktop); collapse it on narrow screens.
  var side = document.querySelector(".side details");
  if (side && window.matchMedia("(max-width: 900px)").matches) {
    side.removeAttribute("open");
    side.addEventListener("click", function (e) {
      if (e.target.closest("a")) side.removeAttribute("open");
    });
  }
})();
