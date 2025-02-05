self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('v1').then((cache) => {
            return cache.addAll([
                'main.html',
                'style.css',
                'icon_192_192.png',
                'icon_512_512.png',
                'index.html',
                'login.css',
                'admin.css',
                'admin.html',
                'register.html',
                
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
