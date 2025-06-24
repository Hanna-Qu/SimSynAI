import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

// 国际化配置
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import zhTranslation from './locales/zh.json';
import enTranslation from './locales/en.json';

// 初始化 i18next
i18n
  .use(initReactI18next)
  .init({
    resources: {
      zh: {
        translation: zhTranslation
      },
      en: {
        translation: enTranslation
      }
    },
    lng: 'zh', // 默认语言
    fallbackLng: 'zh',
    interpolation: {
      escapeValue: false
    }
  });

const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error('找不到root元素，无法挂载React应用');
}

const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// 性能测量
reportWebVitals(); 