/* ═══════════════════════════════════════════════════════════
   PillNav – React Bits Component Logics with GSAP
   INACAP Sede Maipú · N.A.P.I
═══════════════════════════════════════════════════════════ */

(function () {
  function initPillNav() {
    if (typeof gsap === 'undefined') {
      console.warn('GSAP no está cargado. Se requiere GSAP para las animaciones de PillNav.');
      return;
    }

    const nav = document.querySelector('.pill-nav');
    if (!nav) return;

    const pills = nav.querySelectorAll('.pill');
    const timelines = [];
    const activeTweens = [];

    function computePillLayout() {
      pills.forEach((pill, i) => {
        const circle = pill.querySelector('.hover-circle');
        const label = pill.querySelector('.pill-label');
        const hoverLabel = pill.querySelector('.pill-label-hover');
        if (!circle) return;

        const rect = pill.getBoundingClientRect();
        const w = rect.width;
        const h = rect.height;
        if (w === 0 || h === 0) return;

        const R = ((w * w) / 4 + h * h) / (2 * h);
        const D = Math.ceil(2 * R) + 2;
        const delta = Math.ceil(R - Math.sqrt(Math.max(0, R * R - (w * w) / 4))) + 1;
        const originY = D - delta;

        circle.style.width = `${D}px`;
        circle.style.height = `${D}px`;
        circle.style.bottom = `-${delta}px`;

        gsap.set(circle, {
          xPercent: -50,
          scale: 0,
          transformOrigin: `50% ${originY}px`
        });

        if (label) gsap.set(label, { y: 0 });
        if (hoverLabel) gsap.set(hoverLabel, { y: h + 12, opacity: 0 });

        if (timelines[i]) timelines[i].kill();

        const tl = gsap.timeline({ paused: true });
        tl.to(circle, { scale: 1.2, xPercent: -50, duration: 0.35, ease: 'power2.out', overwrite: 'auto' }, 0);
        if (label) {
          tl.to(label, { y: -(h + 8), duration: 0.35, ease: 'power2.out', overwrite: 'auto' }, 0);
        }
        if (hoverLabel) {
          gsap.set(hoverLabel, { y: Math.ceil(h + 20), opacity: 0 });
          tl.to(hoverLabel, { y: 0, opacity: 1, duration: 0.35, ease: 'power2.out', overwrite: 'auto' }, 0);
        }

        timelines[i] = tl;
      });
    }

    // Calcular geometría y enlazar resize
    computePillLayout();
    window.addEventListener('resize', computePillLayout);
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(computePillLayout).catch(() => {});
    }

    // Listeners de hover interactivo en cada píldora
    pills.forEach((pill, i) => {
      pill.addEventListener('mouseenter', () => {
        const tl = timelines[i];
        if (!tl) return;
        if (activeTweens[i]) activeTweens[i].kill();
        activeTweens[i] = tl.tweenTo(tl.duration(), {
          duration: 0.3,
          ease: 'power2.out',
          overwrite: 'auto'
        });
      });

      pill.addEventListener('mouseleave', () => {
        const tl = timelines[i];
        if (!tl) return;
        if (activeTweens[i]) activeTweens[i].kill();
        activeTweens[i] = tl.tweenTo(0, {
          duration: 0.25,
          ease: 'power2.out',
          overwrite: 'auto'
        });
      });

      pill.addEventListener('click', () => {
        pills.forEach(p => p.classList.remove('is-active'));
        pill.classList.add('is-active');
      });
    });

    // Logo estático institucional (sin rotación ni movimiento)

    // Animación inicial de entrada suave para la barra de píldoras
    const navItems = nav.querySelector('.pill-nav-items');
    if (navItems) {
      gsap.from(navItems, {
        opacity: 0,
        y: -10,
        duration: 0.6,
        ease: 'power3.out',
        clearProps: 'all'
      });
    }

    // ScrollSpy para actualizar píldora activa según la sección visible
    const sections = ['inicio', 'sobre-nosotros', 'origen', 'napi'];
    const sectionEls = sections.map(id => document.getElementById(id)).filter(Boolean);

    function updateActiveOnScroll() {
      const scrollPos = window.scrollY + 140;
      let currentId = 'inicio';
      for (const sec of sectionEls) {
        if (sec.offsetTop <= scrollPos) {
          currentId = sec.id;
        }
      }
      pills.forEach(pill => {
        const href = pill.getAttribute('href');
        if (href === `#${currentId}`) {
          pill.classList.add('is-active');
        } else {
          pill.classList.remove('is-active');
        }
      });
    }

    window.addEventListener('scroll', updateActiveOnScroll, { passive: true });
    updateActiveOnScroll();
    // Toggle del menú móvil animado con GSAP
    window.toggleMobileMenu = function () {
      const menu = document.getElementById('mobileMenu');
      if (!menu) return;
      const isHidden = menu.classList.contains('hidden');

      if (isHidden) {
        menu.classList.remove('hidden');
        if (typeof gsap !== 'undefined') {
          gsap.fromTo(
            menu,
            { opacity: 0, y: -12, scale: 0.98 },
            { opacity: 1, y: 0, scale: 1, duration: 0.25, ease: 'power2.out' }
          );
        }
      } else {
        if (typeof gsap !== 'undefined') {
          gsap.to(menu, {
            opacity: 0,
            y: -10,
            scale: 0.98,
            duration: 0.2,
            ease: 'power2.in',
            onComplete: () => {
              menu.classList.add('hidden');
            }
          });
        } else {
          menu.classList.add('hidden');
        }
      }
    };
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPillNav);
  } else {
    initPillNav();
  }
})();
