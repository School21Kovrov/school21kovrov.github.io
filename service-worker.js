self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('v1').then((cache) => {
            return cache.addAll([
                'main.html',
                'style.css',
                'icon-192x192.png',
                'icon-512x512.png',
                // Добавьте другие файлы, которые нужно кэшировать
            ]);
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});