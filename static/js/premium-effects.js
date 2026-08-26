/* ============================================
   BÍBLIA STUDY — PREMIUM EFFECTS
   Ripple, page transitions, confetti, tilt cards
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* === RIPPLE EFFECT ON BUTTONS === */
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.btn-primary, .btn-accent, .btn-ghost, .btn-success, .btn-danger, .sidebar-link, .bottom-tab')
    if (!btn) return

    const ripple = document.createElement('span')
    const rect = btn.getBoundingClientRect()
    const size = Math.max(rect.width, rect.height) * 2
    ripple.style.cssText = `
      position: absolute; border-radius: 50%; pointer-events: none;
      width: ${size}px; height: ${size}px;
      left: ${e.clientX - rect.left - size/2}px;
      top: ${e.clientY - rect.top - size/2}px;
      background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
      transform: scale(0); animation: ripple-expand 0.6s ease-out forwards;
      z-index: 10;
    `
    btn.style.position = 'relative'
    btn.style.overflow = 'hidden'
    btn.appendChild(ripple)
    setTimeout(() => ripple.remove(), 700)
  })

  /* === PAGE TRANSITION ON LOAD === */
  const main = document.querySelector('[x-data]') || document.querySelector('main') || document.querySelector('.min-h-screen')
  if (main) {
    main.style.opacity = '0'
    main.style.transform = 'translateY(12px)'
    main.style.transition = 'opacity 0.4s ease, transform 0.4s ease'
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        main.style.opacity = '1'
        main.style.transform = 'translateY(0)'
      })
    })
  }

  /* === CARD TILT ON MOUSE MOVE (desktop only) === */
  if (window.matchMedia('(hover: hover)').matches) {
    document.addEventListener('mousemove', (e) => {
      const card = e.target.closest('.card-neon, .card-glow, .stat-card')
      if (!card) return
      const rect = card.getBoundingClientRect()
      const x = (e.clientX - rect.left) / rect.width - 0.5
      const y = (e.clientY - rect.top) / rect.height - 0.5
      card.style.transform = `perspective(600px) rotateY(${x * 4}deg) rotateX(${-y * 4}deg) scale(1.01)`
      card.style.transition = 'transform 0.1s ease'
    })

    document.addEventListener('mouseleave', (e) => {
      const card = e.target.closest('.card-neon, .card-glow, .stat-card')
      if (card) {
        card.style.transform = 'perspective(600px) rotateY(0) rotateX(0) scale(1)'
        card.style.transition = 'transform 0.4s ease'
      }
    }, true)
  }

  /* === CONFETTI BURST === */
  window.triggerConfetti = (x, y, count = 30) => {
    const colors = ['#00d4ff', '#00ff88', '#ff0080', '#a855f7', '#ffd700', '#ff6b35']
    for (let i = 0; i < count; i++) {
      const el = document.createElement('div')
      el.className = 'confetti-particle'
      const color = colors[Math.floor(Math.random() * colors.length)]
      const angle = (Math.PI * 2 * i) / count + (Math.random() - 0.5) * 0.5
      const velocity = 100 + Math.random() * 200
      const dx = Math.cos(angle) * velocity
      const dy = Math.sin(angle) * velocity
      el.style.cssText = `
        left: ${x}px; top: ${y}px; background: ${color};
        width: ${4 + Math.random() * 6}px; height: ${4 + Math.random() * 6}px;
        border-radius: ${Math.random() > 0.5 ? '50%' : '2px'};
        animation: none;
        --dx: ${dx}px; --dy: ${dy}px;
      `
      document.body.appendChild(el)
      el.animate([
        { transform: 'translate(0, 0) rotate(0deg) scale(1)', opacity: 1 },
        { transform: `translate(${dx}px, ${dy + 100}px) rotate(${360 + Math.random() * 720}deg) scale(0)`, opacity: 0 }
      ], { duration: 800 + Math.random() * 600, easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)' })
      setTimeout(() => el.remove(), 1500)
    }
  }

  /* === NUMBER COUNTER ANIMATION === */
  window.animateCounter = (el, target, duration = 1000, prefix = '') => {
    const start = parseInt(el.textContent.replace(/\D/g, '')) || 0
    const startTime = performance.now()
    function update(now) {
      const elapsed = now - startTime
      const progress = Math.min(elapsed / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      const current = Math.round(start + (target - start) * eased)
      el.textContent = prefix + current
      if (progress < 1) requestAnimationFrame(update)
    }
    requestAnimationFrame(update)
  }

  /* === SMOOTH SCROLL TO ELEMENT === */
  window.smoothScrollTo = (el) => {
    el.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }

  /* === BUTTON HOVER SOUND (delegated) === */
  document.addEventListener('mouseover', (e) => {
    if (e.target.closest('.btn-primary, .btn-accent, .sidebar-link, .bottom-tab')) {
      if (typeof SoundEngine !== 'undefined') SoundEngine.hover()
    }
  })

  /* === CLICK SOUND FOR ALL INTERACTIVE ELEMENTS === */
  document.addEventListener('click', (e) => {
    if (typeof SoundEngine === 'undefined') return
    if (e.target.closest('button, a, .sidebar-link, .bottom-tab, input[type="submit"]')) {
      SoundEngine.click()
    }
  })

  /* === MUSIC TOGGLE BUTTON (global) === */
  const musicBtn = document.getElementById('music-toggle')
  if (musicBtn) {
    musicBtn.addEventListener('click', (e) => {
      e.stopPropagation()
      const playing = SoundEngine.isMusicPlaying()
      if (playing) {
        SoundEngine.fadeOutMusic()
        musicBtn.innerHTML = '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 14l2-2m0 0l2-2m-2 2l2-2m-2 2l-2-2"/></svg>'
        musicBtn.title = 'Ativar música'
      } else {
        SoundEngine.fadeInMusic()
        musicBtn.innerHTML = '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg>'
        musicBtn.title = 'Desativar música'
      }
    })
  }
})
