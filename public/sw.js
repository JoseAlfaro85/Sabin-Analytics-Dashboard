const CACHE_NAME = "sabin-dashboard-2026-05-2026-06-17t12-39-56";
const APP_SHELL = [
  "/",
  "/app",
  "/DASHBOARD_PREVIEW.html",
  "/REPORTS.html",
  "/ADS.html",
  "/PROGRAMS_REPORT.html",
  "/EXECUTIVE_REPORT.html",
  "/BOARD_REPORT.html",
  "/SOCIAL_LISTENING.html",
  "/SETTINGS.html",
  "/HELP.html",
  "/manifest.webmanifest",
  "/app-icon.svg",
  "/assets/sabin-logo-color.png",
  "/assets/sabin-logo-white.png",
  "/assets/sabin-logo-black.png",
  "/data/dashboard_manifest.json",
  "/data/latest_dashboard.json"
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(APP_SHELL.map((path) => new Request(path, { cache: 'reload' }))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.map((key) => key === CACHE_NAME ? undefined : caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

async function putIfUsable(cache, request, response) {
  if (response && response.ok) {
    await cache.put(request, response.clone());
  }
  return response;
}

async function networkFirst(request, fallbackPath) {
  const cache = await caches.open(CACHE_NAME);
  try {
    return await putIfUsable(cache, request, await fetch(request));
  } catch (error) {
    return await cache.match(request) || await cache.match(fallbackPath || '/DASHBOARD_PREVIEW.html') || Response.error();
  }
}

async function staleWhileRevalidate(request) {
  const cache = await caches.open(CACHE_NAME);
  const cached = await cache.match(request);
  const refresh = fetch(request)
    .then((response) => putIfUsable(cache, request, response))
    .catch(() => undefined);
  if (cached) {
    return cached;
  }
  return await refresh || Response.error();
}

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') {
    return;
  }
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) {
    return;
  }
  if (event.request.mode === 'navigate') {
    event.respondWith(networkFirst(event.request, '/DASHBOARD_PREVIEW.html'));
    return;
  }
  if (APP_SHELL.includes(url.pathname) || url.pathname.startsWith('/data/')) {
    event.respondWith(staleWhileRevalidate(event.request));
  }
});
