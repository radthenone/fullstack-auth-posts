import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { DevSupport } from '@react-buddy/ide-toolbox';
import { ComponentPreviews, useInitial } from './dev';
import App from './App.tsx';
import { Provider } from 'react-redux';
import store from 'app/store';

const element = document.getElementById('root') as HTMLElement;
const root = ReactDOM.createRoot(element);
root.render(
  <React.StrictMode>
    <DevSupport ComponentPreviews={ComponentPreviews} useInitialHook={useInitial}>
      <Provider store={store}>
        <App />
      </Provider>
    </DevSupport>
  </React.StrictMode>,
);
