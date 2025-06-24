import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

// Mock react-router-dom
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  BrowserRouter: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  useNavigate: () => jest.fn(),
  useLocation: () => ({ pathname: '/login' }),
}));

// Mock react-i18next
jest.mock('react-i18next', () => ({
  useTranslation: () => ({
    t: (key: string) => key,
    i18n: {
      changeLanguage: () => new Promise(() => {}),
      language: 'zh'
    }
  }),
  initReactI18next: {
    type: '3rdParty',
    init: () => {}
  }
}));

// Mock react-responsive
jest.mock('react-responsive', () => ({
  useMediaQuery: () => false
}));

test('renders without crashing', () => {
  const { container } = render(<App />);
  // 应用应该能够渲染而不崩溃
  expect(container).toBeTruthy();
}); 