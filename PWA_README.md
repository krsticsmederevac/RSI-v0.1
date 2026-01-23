# Crypto Technical Analysis PWA

A Progressive Web App for real-time cryptocurrency technical analysis with multiple indicators and timeframes.

## Features

- **Single Timeframe Analysis**: Analyze coins across a single timeframe with multiple technical indicators (RSI, Bollinger Bands, EMA, SMA, CCI, Price Change)
- **Multi-Timeframe Analysis**: View indicators across multiple timeframes simultaneously with heatmaps
- **RSI Filtering**: Filter coins by RSI values to find trading opportunities
- **Fully Responsive**: Works perfectly on desktop, tablet, and mobile devices
- **PWA Capabilities**: Install as a native app on Android and iOS
- **Offline Support**: Service worker caching for better performance

## Installation on Android

### Method 1: Chrome Browser (Recommended)

1. Open this app in Chrome on your Android device
2. Tap the menu icon (three dots) in the top right
3. Select "Install app" or "Add to Home screen"
4. Confirm the installation
5. The app will appear on your home screen

### Method 2: Firefox Browser

1. Open this app in Firefox on your Android device
2. Tap the menu icon (three dots) in the top right
3. Select "Install"
4. The app will appear on your home screen

### Method 3: Web Installation Link

Alternatively, you can add a bookmark shortcut:
1. Tap the menu icon
2. Select "Add bookmark" or "Add to Home screen"
3. The shortcut will appear on your home screen

## Building from Source

### Prerequisites
- Node.js 16+ and npm

### Installation

```bash
npm install
```

### Development

Run the development server:
```bash
npm run dev
```

The app will open at `http://localhost:3000`

### Production Build

```bash
npm run build
```

The production build will be generated in the `dist/` directory.

## Deployment

The PWA can be deployed to any static hosting service:

### Vercel (Recommended for fastest deployment)
```bash
npm install -g vercel
vercel
```

### Netlify
```bash
npm install -g netlify-cli
netlify deploy --prod --dir dist
```

### GitHub Pages
1. Build the project: `npm run build`
2. Push the `dist` folder to your GitHub Pages branch

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM caddy:latest
COPY --from=0 /app/dist /srv
```

## Project Structure

```
src/
├── main.jsx              # React entry point
├── App.jsx              # Main app component
├── App.css              # App styles
├── pages/
│   ├── Home.jsx         # Home page
│   ├── SingleTF.jsx     # Single timeframe analysis
│   ├── MultiTF.jsx      # Multi-timeframe analysis
│   └── FilterRSI.jsx    # RSI filtering tool
└── index.css            # Global styles

public/
├── manifest.json        # PWA manifest
└── sw.js               # Service worker

index.html              # HTML entry point
vite.config.js          # Vite configuration
package.json            # Dependencies
```

## Technologies Used

- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Chart.js & react-chartjs-2**: Charting library
- **Lucide React**: Icon library
- **Service Workers**: Offline functionality and caching
- **PWA**: Progressive Web App features

## Features Details

### Single Timeframe Analysis
- Select multiple coins
- Choose timeframe
- Sort by coin name or value
- View technical indicators

### Multi-Timeframe Analysis
- View multiple timeframes simultaneously
- Heatmap visualizations
- Compare indicators across timeframes
- Tabbed interface for different indicator types

### RSI Filtering
- Set RSI range (0-100)
- Inverse range option
- Filter coins by RSI criteria
- Sort results by value or coin

## Browser Support

The PWA works best on:
- Chrome/Chromium 51+
- Firefox 55+
- Safari 15.1+
- Edge 79+

## Performance

- Lightweight bundle (~50KB gzipped)
- Fast load times with service worker caching
- Optimized for mobile performance
- Progressive enhancement

## Tips

For best performance:
1. Keep the app updated in your app drawer
2. Enable notifications for market updates
3. Use 4G/5G or WiFi for faster data loading
4. Clear app cache periodically if storage is low

## Support

For issues or feature requests, check the original Streamlit version of this app or open an issue in the repository.

## License

This PWA version maintains compatibility with the original Streamlit application while providing a native app experience on mobile devices.
