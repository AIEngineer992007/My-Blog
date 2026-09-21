document.addEventListener('DOMContentLoaded', function () {
  const toggle = document.getElementById('navToggle');
  const collapse = document.getElementById('navCollapse');

  if (!toggle || !collapse) return;

  toggle.addEventListener('click', function () {
    const isOpen = collapse.classList.toggle('open');
    toggle.classList.toggle('open', isOpen);
    toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    toggle.setAttribute('aria-label', isOpen ? 'Đóng menu' : 'Mở menu');
  });
});