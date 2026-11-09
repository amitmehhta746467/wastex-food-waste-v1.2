document.addEventListener('DOMContentLoaded', function () {
  // Mobile menu
  var burger = document.querySelector('.burger');
  var nav = document.querySelector('.nav nav');
  if (burger && nav) burger.addEventListener('click', function () { nav.classList.toggle('open'); });

  // Reveal on scroll
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });

  // Animated counters
  var cio = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el = e.target, target = parseInt(el.dataset.count || '0', 10), start = null;
      function tick(ts) {
        if (!start) start = ts;
        var p = Math.min((ts - start) / 1400, 1);
        el.textContent = Math.floor(target * p).toLocaleString('en-IN') + (p === 1 ? '+' : '');
        if (p < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
      cio.unobserve(el);
    });
  }, { threshold: 0.4 });
  document.querySelectorAll('[data-count]').forEach(function (el) { cio.observe(el); });

  // FAQ accordion
  document.querySelectorAll('.faq-item button').forEach(function (btn) {
    btn.addEventListener('click', function () { btn.parentElement.classList.toggle('open'); });
  });

  // Impact calculator: 1 kg leftover food ≈ 2.5 meals potential / 2.5 kg CO2e if landfilled
  var range = document.getElementById('calc-kg');
  if (range) {
    var kgOut = document.getElementById('calc-kg-val'),
        meals = document.getElementById('calc-meals'),
        co2 = document.getElementById('calc-co2'),
        compost = document.getElementById('calc-compost');
    function update() {
      var kg = parseInt(range.value, 10);
      kgOut.textContent = kg + ' kg';
      meals.textContent = Math.round(kg * 2.5).toLocaleString('en-IN');
      co2.textContent = (kg * 2.5).toLocaleString('en-IN') + ' kg';
      compost.textContent = Math.round(kg * 0.3) + ' kg';
    }
    range.addEventListener('input', update);
    update();
  }
});

  // 3D tilt on cards (fine pointers only, respects reduced motion)
  if (window.matchMedia('(pointer:fine)').matches &&
      !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll('[data-tilt]').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5;
        var y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = 'perspective(900px) rotateY(' + (x * 7) + 'deg) rotateX(' + (-y * 7) + 'deg) translateY(-5px)';
      });
      el.addEventListener('pointerleave', function () { el.style.transform = ''; });
    });
  }
