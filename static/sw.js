cacheVersion = "v254";
swVersion = "v6";

this.addEventListener("install", function(event){
    event.waitUntil(
        caches.open(cacheVersion).then(function(cache){
            return cache.addAll([
                "/",
                "index.html",
                "createUser.html",
                "manifest.json",
                "narrow-style.css",
                "wide-style.css",
                "scripts.js",
                "sw.js",
                "images/icon512-Rounded-Gray.png",
                "https://fonts.gstatic.com/s/sourcesanspro/v10/ODelI1aHBYDBqgeIAH2zlJbPFduIYtoLzwST68uhz_Y.woff2",
                "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/fonts/fontawesome-webfont.woff2?v=4.7.0",
                "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/fonts/fontawesome-webfont.woff?v=4.7.0",
                "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/fonts/fontawesome-webfont.ttf?v=4.7.0",
                "https://fonts.googleapis.com/css?family=Source+Sans+Pro",
                "jquery.min.js"
            ]);
        })
    );
    console.log("Service Worker Installed");
    skipWaiting();
});

this.addEventListener('activate', function(event) {
    var cacheWhitelist = [cacheVersion];
    event.waitUntil(
        caches.keys().then(function(keyList) {
            return Promise.all(keyList.map(function(key) {
                if (cacheWhitelist.indexOf(key) === -1) {
                return caches.delete(key);
                }
            }));
        })
    );
    console.log("Service Worker " + swVersion+ ", using cache " + cacheVersion);
});

this.addEventListener('fetch', function(event) {
    event.respondWith(
        // magic goes here
        caches.match(event.request).then(function(response){
            return response || fetch(event.request);
        }).catch(function(event){
            return(new Response("<div class='task' style='height:auto;width:auto;'><h2>📶❌😞</h2></div>"));
        })
    );
    console.log("Fetch Request Made");
});

self.addEventListener("push", function(event){
    console.log("Push notification receieved")
    data = event.data.text().split(";");
    title = data[3];
    text = data[0];
    icon = data[2];
    var promise = self.registration.showNotification(title, {
        "body":text,
        "icon":icon,
        "vibrate": [500,110,500],
        });
    event.waitUntil(promise);
});

self.addEventListener('notificationclick', function(event) {
    const clickedNotification = event.notification;
    clickedNotification.close();
    var url = "https://pihome.zapto.org/dev/"
    event.waitUntil(
        clients.matchAll({type: 'window'}).then( windowClients => {
        // Check if there is already a window/tab open with the target URL
        for (var i = 0; i < windowClients.length; i++) {
            var client = windowClients[i];
            // If so, just focus it.
            if (client.url === url && 'focus' in client) {
                return client.focus();
            }
        }
        if (clients.openWindow) {
            return clients.openWindow(url);}
        }));
});
