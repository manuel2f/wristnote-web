(() => {
  // --- THEME TOGGLE LOGIC ---
  const THEME_KEY = 'wristnote-theme';
  const html = document.documentElement;
  const themeBtn = document.querySelector('[data-theme-toggle]');

  function getSystemTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    html.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);
    if (themeBtn) {
      themeBtn.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
      const sunIcon = themeBtn.querySelector('.icon-sun');
      const moonIcon = themeBtn.querySelector('.icon-moon');
      if (sunIcon && moonIcon) {
        sunIcon.style.display = theme === 'dark' ? 'block' : 'none';
        moonIcon.style.display = theme === 'dark' ? 'none' : 'block';
      }
    }
  }

  const savedTheme = localStorage.getItem(THEME_KEY) || getSystemTheme();
  applyTheme(savedTheme);

  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      const current = html.getAttribute('data-theme') || 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      applyTheme(next);
    });
  }

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (!localStorage.getItem(THEME_KEY)) {
      applyTheme(e.matches ? 'dark' : 'light');
    }
  });

  // --- MOBILE MENU TOGGLE ---
  const menuBtn = document.querySelector('[data-menu-toggle]');
  const mobileMenu = document.querySelector('[data-mobile-menu]');
  if (menuBtn && mobileMenu) {
    menuBtn.addEventListener('click', () => {
      const isOpen = mobileMenu.classList.toggle('is-open');
      menuBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    mobileMenu.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        mobileMenu.classList.remove('is-open');
        menuBtn.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // --- VIDEO MODAL ---
  const modalBackdrop = document.querySelector('[data-video-modal]');
  const openVideoBtns = document.querySelectorAll('[data-open-video]');
  const closeVideoBtn = document.querySelector('[data-close-video]');
  const videoFrameContainer = document.querySelector('[data-video-frame]');
  let lastFocused = null;

  // --- REDUCED MOTION: stop the looping hero video ---
  const heroVideo = document.querySelector('.mockup-video');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (heroVideo && reducedMotion.matches) {
    heroVideo.removeAttribute('autoplay');
    heroVideo.pause();
  }

  function openVideo(videoSrc, isYoutube = false) {
    if (!modalBackdrop || !videoFrameContainer) return;
    if (isYoutube) {
      videoFrameContainer.innerHTML = `
        <iframe 
          src="https://www.youtube-nocookie.com/embed/${videoSrc}?autoplay=1&rel=0" 
          title="WristNote Demo" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
          allowfullscreen>
        </iframe>`;
    } else {
      videoFrameContainer.innerHTML = `
        <video controls autoplay playsinline style="width:100%;height:100%;object-fit:contain;background:#000;">
          <source src="${videoSrc}" type="video/mp4">
        </video>`;
    }
    lastFocused = document.activeElement;
    modalBackdrop.classList.add('is-open');
    modalBackdrop.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    closeVideoBtn?.focus();
  }

  function closeVideo() {
    if (!modalBackdrop || !videoFrameContainer) return;
    modalBackdrop.classList.remove('is-open');
    modalBackdrop.setAttribute('aria-hidden', 'true');
    videoFrameContainer.innerHTML = '';
    document.body.style.overflow = '';
    lastFocused?.focus();
  }

  // Keep keyboard focus inside the open modal
  modalBackdrop?.addEventListener('keydown', (e) => {
    if (e.key !== 'Tab') return;
    const focusable = modalBackdrop.querySelectorAll('button, video[controls], iframe');
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });

  openVideoBtns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const videoSrc = btn.getAttribute('data-video-src');
      const youtubeId = btn.getAttribute('data-youtube-id');
      if (youtubeId) {
        openVideo(youtubeId, true);
      } else {
        openVideo(videoSrc, false);
      }
    });
  });

  if (closeVideoBtn) closeVideoBtn.addEventListener('click', closeVideo);
  if (modalBackdrop) {
    modalBackdrop.addEventListener('click', (e) => {
      if (e.target === modalBackdrop) closeVideo();
    });
  }
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modalBackdrop?.classList.contains('is-open')) {
      closeVideo();
    }
  });
})();
