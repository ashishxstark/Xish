import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  en: { translation: { hello: 'Hello, I’m Xish AI ⚡', startChatting: 'Start Chatting' } },
  es: { translation: { hello: 'Hola, soy Xish AI ⚡', startChatting: 'Comenzar chat' } },
};

i18n.use(initReactI18next).init({
  resources,
  lng: 'en',
  fallbackLng: 'en',
  interpolation: { escapeValue: false },
});

export default i18n;
