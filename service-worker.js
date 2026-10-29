const CACHE_NAME = 'epistemic-octahedron-complete-offline-v1';
const CACHE_PREFIX = 'epistemic-octahedron-complete-offline-';

const PRECACHE = [
  './',
  './index.html',
  './pwa.html',
  './pwa.webmanifest',
  './script.mp3'
];

async function refreshPrecache() {
  const cache = await caches.open(CACHE_NAME);
  const requests = PRECACHE.map(url => new Request(url, { cache: 'reload' }));
  await cache.addAll(requests);
}

self.addEventListener('install', event => {
  event.waitUntil(refreshPrecache().then(() => self.skipWaiting()));
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const names = await caches.keys();
    await Promise.all(
      names
        .filter(name => name.startsWith(CACHE_PREFIX) && name !== CACHE_NAME)
        .map(name => caches.delete(name))
    );
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', event => {
  const request = event.request;
  if (request.method !== 'GET') return;

  event.respondWith((async () => {
    const cached = await caches.match(request, { ignoreSearch: true });
    if (cached) return cached;

    try {
      const response = await fetch(request);
      if (response && response.ok && new URL(request.url).origin === self.location.origin) {
        const cache = await caches.open(CACHE_NAME);
        cache.put(request, response.clone()).catch(() => {});
      }
      return response;
    } catch (error) {
      if (request.mode === 'navigate') {
        return (await caches.match('./index.html')) || (await caches.match('./pwa.html'));
      }
      throw error;
    }
  })());
});

self.addEventListener('message', event => {
  if (!event.data || event.data.type !== 'UPDATE_CACHE') return;

  event.waitUntil((async () => {
    try {
      await refreshPrecache();
      if (event.ports && event.ports[0]) event.ports[0].postMessage({ ok: true });
    } catch (error) {
      if (event.ports && event.ports[0]) {
        event.ports[0].postMessage({ ok: false, message: String(error && error.message || error) });
      }
    }
  })());
});
