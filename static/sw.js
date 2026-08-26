const CACHE_NAME = 'biblia-v2';
const STATIC_ASSETS = [
  '/static/css/output.css',
  '/static/js/app.js',
  '/static/js/sounds.js',
  '/static/js/premium-effects.js',
  '/static/manifest.json',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // Never cache API calls, navigation, or cross-origin
  if (url.pathname.startsWith('/chat/') ||
      url.pathname.startsWith('/cursos/') ||
      url.pathname.startsWith('/gamificacao/') ||
      url.pathname.startsWith('/admin/') ||
      url.pathname.startsWith('/api/') ||
      event.request.mode === 'navigate' ||
      event.request.destination === 'document') {
    event.respondWith(fetch(event.request).catch(() => caches.match(event.request)));
    return;
  }

  // Cache-first for static assets only
  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) return cached;
      return fetch(event.request).then((response) => {
        if (response && response.status === 200 && response.type === 'basic') {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        }
        return response;
      });
    })
  );
});
