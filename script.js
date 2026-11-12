// Only a little motion. Everything still works without JavaScript.
(() => {
  const year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());
  if (!("IntersectionObserver" in window) || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const sections = document.querySelectorAll(".section");
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("shown");
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.05, rootMargin: "0px 0px -18px 0px" });
  sections.forEach(section => observer.observe(section));
  requestAnimationFrame(() => document.documentElement.classList.add("motion-ready"));
})();
