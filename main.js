/* ═══ Smylee — interactie & React Bits ports (vanilla JS) ═══ */

// Mobile nav
function toggleNav(){
  var links = document.getElementById('navLinks');
  var btn = document.querySelector('.mobile-toggle');
  var open = links.classList.toggle('open');
  if(btn) btn.setAttribute('aria-expanded', open ? 'true' : 'false');
}
function closeNav(){
  document.getElementById('navLinks').classList.remove('open');
  var btn = document.querySelector('.mobile-toggle');
  if(btn) btn.setAttribute('aria-expanded', 'false');
}

// Nav shadow on scroll
window.addEventListener('scroll', function(){
  var n = document.getElementById('nav');
  if(n) n.classList.toggle('scrolled', window.scrollY > 10);
});

// Fade-in on scroll
(function(){
  var els = document.querySelectorAll('.fade-in');
  if(!('IntersectionObserver' in window)){ els.forEach(function(e){ e.classList.add('visible'); }); return; }
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(en){ if(en.isIntersecting){ en.target.classList.add('visible'); io.unobserve(en.target); } });
  }, {threshold:0, rootMargin:'0px 0px -4% 0px'});
  els.forEach(function(e){ io.observe(e); });
  // Safety: force visible after 2.5s so nothing is ever left hidden
  setTimeout(function(){ els.forEach(function(e){ e.classList.add('visible'); }); }, 2500);
})();

// Count Up
function animateCount(el){
  var target = parseFloat(el.getAttribute('data-count'));
  var decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
  var suffix = el.getAttribute('data-suffix') || '';
  var dur = 1400, t0 = performance.now();
  function tick(now){
    var p = Math.min((now - t0) / dur, 1);
    var eased = 1 - Math.pow(1 - p, 3);
    var val = target * eased;
    el.textContent = (decimals ? val.toFixed(decimals) : Math.round(val).toString()) + suffix;
    if(p < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
(function(){
  var els = document.querySelectorAll('[data-count]');
  if(!('IntersectionObserver' in window)){ els.forEach(function(e){ e.textContent = e.getAttribute('data-count') + (e.getAttribute('data-suffix')||''); }); return; }
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if(en.isIntersecting && !en.target.dataset.done){ en.target.dataset.done='1'; animateCount(en.target); }
    });
  }, {threshold:.4});
  els.forEach(function(e){ io.observe(e); });
})();

// Magnet CTA
(function(){
  if(!window.matchMedia || !window.matchMedia('(pointer:fine)').matches) return;
  document.querySelectorAll('.magnet').forEach(function(btn){
    btn.addEventListener('mousemove', function(e){
      var r = btn.getBoundingClientRect();
      var x = (e.clientX - r.left - r.width/2) / (r.width/2);
      var y = (e.clientY - r.top - r.height/2) / (r.height/2);
      btn.style.transform = 'translate(' + (x*6).toFixed(1) + 'px,' + (y*6).toFixed(1) + 'px)';
    });
    btn.addEventListener('mouseleave', function(){ btn.style.transform = ''; });
  });
})();

// Click Spark
(function(){
  document.querySelectorAll('.click-spark-btn').forEach(function(btn){
    btn.addEventListener('click', function(e){
      var r = btn.getBoundingClientRect();
      var x = e.clientX - r.left, y = e.clientY - r.top;
      for(var i=0;i<9;i++){
        var s = document.createElement('span');
        s.className = 'click-spark';
        s.style.left = x + 'px'; s.style.top = y + 'px';
        var a = (Math.PI*2*i)/9, d = 13 + Math.random()*20;
        s.style.setProperty('--dx', (Math.cos(a)*d).toFixed(1) + 'px');
        s.style.setProperty('--dy', (Math.sin(a)*d).toFixed(1) + 'px');
        btn.appendChild(s);
        (function(node){ setTimeout(function(){ node.remove(); }, 620); })(s);
      }
    });
  });
})();

// Tilted cards
(function(){
  if(!window.matchMedia || !window.matchMedia('(pointer:fine)').matches) return;
  document.querySelectorAll('.tilt-card').forEach(function(card){
    card.addEventListener('mousemove', function(e){
      var r = card.getBoundingClientRect();
      var rx = (e.clientY - r.top - r.height/2) / r.height;
      var ry = (e.clientX - r.left - r.width/2) / r.width;
      card.style.transform = 'rotateX(' + (-rx*7).toFixed(2) + 'deg) rotateY(' + (ry*7).toFixed(2) + 'deg)';
    });
    card.addEventListener('mouseleave', function(){ card.style.transform = ''; });
  });
})();

// Before/After slider
(function(){
  var wrap = document.querySelector('.ba-wrap');
  if(!wrap) return;
  var after = wrap.querySelector('.ba-after');
  var handle = wrap.querySelector('.ba-handle');
  function setPos(pct){
    pct = Math.max(0, Math.min(100, pct));
    after.style.clipPath = 'inset(0 0 0 ' + pct + '%)';
    handle.style.left = pct + '%';
  }
  var dragging = false;
  function move(e){
    var r = wrap.getBoundingClientRect();
    var x = (e.touches ? e.touches[0].clientX : e.clientX) - r.left;
    setPos((x / r.width) * 100);
  }
  wrap.addEventListener('pointerdown', function(e){ dragging = true; move(e); wrap.setPointerCapture(e.pointerId); });
  wrap.addEventListener('pointermove', function(e){ if(dragging) move(e); });
  wrap.addEventListener('pointerup', function(){ dragging = false; });
  wrap.addEventListener('pointercancel', function(){ dragging = false; });
  setPos(50);
})();

// FAQ accordion
function toggleFaq(btn){
  var item = btn.closest('.faq-item');
  var ans = item.querySelector('.faq-a');
  var open = btn.classList.contains('open');
  // close others
  document.querySelectorAll('.faq-q.open').forEach(function(q){
    q.classList.remove('open');
    q.setAttribute('aria-expanded','false');
    q.closest('.faq-item').querySelector('.faq-a').style.maxHeight = null;
  });
  if(!open){ btn.classList.add('open'); btn.setAttribute('aria-expanded','true'); ans.style.maxHeight = ans.scrollHeight + 'px'; }
}
