/* ============================================
   BÍBLIA STUDY — App.js (utility functions only)
   Alpine.js components are defined inline in
   each template's {% block extra_scripts %}.
   ============================================ */

/* Service Worker Registration */
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/static/sw.js').catch(() => {})
  })
}
