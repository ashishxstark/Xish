export default {
  name: 'Xish AI',
  slug: 'xish-ai',
  scheme: 'xishai',
  version: '1.0.0',
  orientation: 'portrait',
  icon: './assets/icon.png',
  userInterfaceStyle: 'automatic',
  splash: {
    image: './assets/splash.png',
    resizeMode: 'contain',
    backgroundColor: '#0A0A0A'
  },
  ios: {
    supportsTablet: true
  },
  android: {
    adaptiveIcon: {
      foregroundImage: './assets/adaptive-icon.png',
      backgroundColor: '#0A0A0A'
    }
  },
  web: {
    bundler: 'metro',
    favicon: './assets/favicon.png'
  },
  extra: {
    eas: {
      projectId: '00000000-0000-0000-0000-000000000000'
    }
  },
  experiments: {
    typedRoutes: true
  }
}
