/**
 * TILAK.DEV — client behaviors (adapted from the approved mockup).
 * No dependencies. Every page remains fully readable with JS disabled:
 * content is never hidden behind JavaScript (the .no-js baseline shows it).
 */
(function () {
  var root = document.documentElement;

  /* Theme toggle: honors prefers-color-scheme until the visitor chooses. */
  var toggle = document.querySelector(".theme-toggle");
  var lightIcon =
    '<circle cx="12" cy="12" r="3.8"/><path d="M12 2v2.3M12 19.7V22M4.93 4.93l1.63 1.63M17.44 17.44l1.63 1.63M2 12h2.3M19.7 12H22M4.93 19.07l1.63-1.63M17.44 6.56l1.63-1.63"/>';
  var darkIcon =
    '<path d="M20.4 15.2A8.4 8.4 0 0 1 8.8 3.6a8.4 8.4 0 1 0 11.6 11.6Z"/>';
  var mq = window.matchMedia("(prefers-color-scheme: light)");

  function currentTheme() {
    return root.getAttribute("data-theme") || (mq.matches ? "light" : "dark");
  }
  function updateToggle() {
    if (!toggle) return;
    var isDark = currentTheme() === "dark";
    toggle.setAttribute(
      "aria-label",
      isDark ? "Switch to light paper theme" : "Switch to dark blueprint theme"
    );
    toggle.querySelector("svg").innerHTML = isDark ? lightIcon : darkIcon;
  }
  if (toggle) {
    updateToggle();
    toggle.addEventListener("click", function () {
      root.setAttribute(
        "data-theme",
        currentTheme() === "dark" ? "light" : "dark"
      );
      updateToggle();
    });
    if (mq.addEventListener) {
      mq.addEventListener("change", function () {
        if (!root.hasAttribute("data-theme")) updateToggle();
      });
    }
  }

  /* Brand name appears once the hero has scrolled past the nav. */
  var siteNav = document.querySelector(".site-nav");
  var hero = document.querySelector(".hero");
  var brandFramePending = false;
  function updateBrandName() {
    if (!siteNav || !hero) {
      document.body.classList.add("brand-always");
      if (siteNav) siteNav.classList.add("brand-name-visible");
      return;
    }
    var pastHero =
      hero.getBoundingClientRect().top <= siteNav.offsetHeight;
    siteNav.classList.toggle("brand-name-visible", pastHero);
    brandFramePending = false;
  }
  function queueBrandUpdate() {
    if (brandFramePending) return;
    brandFramePending = true;
    window.requestAnimationFrame(updateBrandName);
  }
  if (siteNav) {
    window.addEventListener("scroll", queueBrandUpdate, { passive: true });
    window.addEventListener("resize", queueBrandUpdate);
    updateBrandName();
  }

  /* Mobile menu */
  var menuToggle = document.querySelector(".menu-toggle");
  var mobileMenu = document.querySelector(".mobile-menu");
  function closeMenu() {
    if (!menuToggle || !mobileMenu) return;
    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.setAttribute("aria-label", "Open navigation");
    mobileMenu.hidden = true;
  }
  if (menuToggle && mobileMenu) {
    menuToggle.addEventListener("click", function () {
      var opening = menuToggle.getAttribute("aria-expanded") !== "true";
      menuToggle.setAttribute("aria-expanded", opening ? "true" : "false");
      menuToggle.setAttribute(
        "aria-label",
        opening ? "Close navigation" : "Open navigation"
      );
      mobileMenu.hidden = !opening;
    });
    mobileMenu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", closeMenu);
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") closeMenu();
    });
    var desktopMQ = window.matchMedia("(min-width: 981px)");
    if (desktopMQ.addEventListener) {
      desktopMQ.addEventListener("change", function (event) {
        if (event.matches) closeMenu();
      });
    }
  }

  /* Copy email (contact section on the homepage only). */
  var copyButton = document.querySelector(".copy-email");
  var copyStatus = document.querySelector(".copy-status");
  var emailAddress = ["iam", "tilak", "patel"]
    .join("")
    .concat("@")
    .concat(["gmail", "com"].join("."));
  function showCopyStatus(message) {
    if (!copyStatus) return;
    copyStatus.textContent = message;
    window.setTimeout(function () {
      copyStatus.textContent = "";
    }, 3200);
  }
  if (copyButton && copyStatus) {
    copyButton.addEventListener("click", function () {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard
          .writeText(emailAddress)
          .then(function () {
            showCopyStatus("Email copied to clipboard.");
          })
          .catch(function () {
            showCopyStatus("Copy unavailable. Use the mail link instead.");
          });
        return;
      }
      var field = document.createElement("textarea");
      field.value = emailAddress;
      field.setAttribute("readonly", "");
      field.style.position = "fixed";
      field.style.opacity = "0";
      document.body.appendChild(field);
      field.select();
      var copied = document.execCommand("copy");
      document.body.removeChild(field);
      showCopyStatus(
        copied ? "Email copied to clipboard." : "Copy unavailable. Use the mail link instead."
      );
    });
  }

  /* Scroll-in reveals. Reduced-motion and no-JS visitors see full content. */
  var reveals = document.querySelectorAll(".reveal");
  var reduced =
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced || !("IntersectionObserver" in window) || !root.classList.contains("js")) {
    reveals.forEach(function (el) {
      el.classList.add("visible");
    });
  } else {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.08 }
    );
    reveals.forEach(function (el) {
      observer.observe(el);
    });
  }
})();
