const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelector(".nav-links");
const navItems = document.querySelectorAll(".nav-links a");
const sections = document.querySelectorAll("main section[id]");

function closeMenu() {
  document.body.classList.remove("nav-open");
  navLinks.classList.remove("is-open");
  navToggle.setAttribute("aria-expanded", "false");
}

navToggle.addEventListener("click", () => {
  const isOpen = navLinks.classList.toggle("is-open");
  document.body.classList.toggle("nav-open", isOpen);
  navToggle.setAttribute("aria-expanded", String(isOpen));
});

navItems.forEach((link) => {
  link.addEventListener("click", closeMenu);
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeMenu();
  }
});

const sectionObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) {
        return;
      }

      const activeLink = document.querySelector(`.nav-links a[href="#${entry.target.id}"]`);

      navItems.forEach((link) => {
        link.classList.toggle("is-active", link === activeLink);
      });
    });
  },
  {
    rootMargin: "-45% 0px -45% 0px",
    threshold: 0,
  }
);

sections.forEach((section) => sectionObserver.observe(section));
