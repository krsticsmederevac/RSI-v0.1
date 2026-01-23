# Deployment Guide for Crypto Technical Analysis PWA

## Quick Start

Your Progressive Web App has been built and is ready to deploy. The production build is in the `dist/` directory.

## Local Testing

Test the PWA locally before deployment:

```bash
npm run build
npx http-server dist
```

Then open `http://localhost:8080` in your browser.

## Install on Android

### Using the Built-in App Installer

1. **Serve the app locally** (or use a deployed URL):
   ```bash
   npx http-server dist
   ```

2. **Open in Chrome on Android**:
   - Enter the URL in Chrome
   - Wait for the app to load completely
   - Tap the menu (three dots)
   - Select "Install app"

3. **Grant Permissions** and the app will be installed on your home screen

## Deployment Options

### Option 1: Vercel (Fastest & Easiest)

```bash
npm install -g vercel
vercel
```

Follow the prompts and your app will be live in seconds.

**URL Format**: `https://your-project-name.vercel.app`

### Option 2: Netlify

```bash
npm install -g netlify-cli
netlify deploy --prod --dir dist
```

**URL Format**: `https://your-site-name.netlify.app`

### Option 3: GitHub Pages

1. Create a repository on GitHub
2. Update `vite.config.js`:
   ```javascript
   export default defineConfig({
     base: '/repo-name/', // your repo name
     // ... rest of config
   })
   ```
3. Run:
   ```bash
   npm run build
   git add dist
   git commit -m "Build PWA"
   git push origin main
   ```
4. Go to repository Settings → Pages → Deploy from branch → Select main/dist

### Option 4: Traditional Hosting (Apache, Nginx, etc.)

1. Build the app:
   ```bash
   npm run build
   ```

2. Upload the `dist/` folder to your server

3. Configure your server:

**Nginx**:
```nginx
server {
  listen 80;
  server_name your-domain.com;

  root /var/www/crypto-ta/dist;
  index index.html;

  location / {
    try_files $uri $uri/ /index.html;
  }

  # Cache busting for assets
  location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
  }

  # Service worker - no cache
  location = /sw.js {
    add_header Cache-Control "no-cache, no-store, must-revalidate";
  }
}
```

**Apache** (in `.htaccess`):
```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>

# Cache control
<FilesMatch "\.(js|css|png|jpg|jpeg|gif|ico|svg)$">
  Header set Cache-Control "max-age=31536000, public"
</FilesMatch>

<FilesMatch "\.html$">
  Header set Cache-Control "max-age=0, no-cache, no-store, must-revalidate"
</FilesMatch>

<FilesMatch "^sw\.js$">
  Header set Cache-Control "no-cache, no-store, must-revalidate"
</FilesMatch>
```

### Option 5: Docker

Create a `Dockerfile`:
```dockerfile
# Build stage
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install --legacy-peer-deps
COPY . .
RUN npm run build

# Production stage
FROM caddy:latest
COPY --from=builder /app/dist /srv

# Optional: Create Caddyfile for more control
COPY Caddyfile /etc/caddy/Caddyfile
```

Create `Caddyfile`:
```
:80 {
  root * /srv
  encode gzip

  file_server {
    index index.html
  }

  # Rewrite to index.html for SPA routing
  try_files {path} /index.html

  # Cache control
  header /assets/* Cache-Control "public, max-age=31536000, immutable"
  header /sw.js Cache-Control "no-cache, no-store, must-revalidate"
}
```

Build and run:
```bash
docker build -t crypto-ta .
docker run -p 80:80 crypto-ta
```

## Installation on Android (from Deployed URL)

Once deployed, users can install the app:

1. **Open in Chrome**: Visit your deployed URL
2. **Wait for Install Prompt**: Chrome will show an install button when ready
3. **Tap Install**: Select "Install app"
4. **Grant Permissions**: Allow the necessary permissions
5. **App Installed**: The app appears on home screen

## PWA Features Enabled

✅ Installable on Android/iOS
✅ Works offline (cached resources)
✅ Custom app icons
✅ Standalone display mode
✅ Service worker caching
✅ App shortcuts
✅ Dark theme optimized

## Monitoring

After deployment, check:

1. **Lighthouse PWA Score**: Open DevTools → Lighthouse → PWA
2. **Manifest Valid**: DevTools → Application → Manifest
3. **Service Worker**: DevTools → Application → Service Workers
4. **Performance**: Run Lighthouse performance audit

## Custom Domain

### Using Vercel
```bash
vercel domains add your-domain.com
# Follow DNS setup instructions
```

### Using Netlify
1. Go to Netlify dashboard
2. Domain settings → Custom domain
3. Update DNS records

## HTTPS

All PWA features require HTTPS (except localhost). Most hosting providers:
- Vercel: Automatic HTTPS
- Netlify: Automatic HTTPS
- GitHub Pages: Automatic HTTPS
- Self-hosted: Use Let's Encrypt with Certbot

## Environment Variables

If you need API keys, create a `.env.local` file:
```
VITE_SUPABASE_URL=your_url
VITE_SUPABASE_ANON_KEY=your_key
```

## Troubleshooting

**App won't install**:
- Check that you're using HTTPS
- Verify manifest.json is accessible
- Clear browser cache
- Try in Incognito mode

**Service worker not working**:
- Check browser console for errors
- Verify service worker scope
- Clear all caches: DevTools → Application → Storage → Clear site data

**Offline not working**:
- Service worker needs time to cache
- Use DevTools Network tab to simulate offline
- Check DevTools → Application → Cache Storage

## Next Steps

1. Deploy using one of the methods above
2. Test on Android device
3. Monitor performance and user metrics
4. Consider adding real crypto data API integration
5. Set up analytics to track usage

## Support

For issues, check:
- Browser console for errors
- DevTools → Application tab
- Network tab for failed requests
- Lighthouse audit results
