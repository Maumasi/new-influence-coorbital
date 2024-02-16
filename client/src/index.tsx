import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import './index.scss';
import reducer from './services/reducers';
import App from './App';
import reportWebVitals from './reportWebVitals';
import {Scene} from './components/Canvas2';



const rootElement = document.getElementById('root');
reportWebVitals(console.log);


if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  const store = configureStore({ reducer });


  

  root.render(
    <React.StrictMode>
      <Provider store={store}>
        <Router>
          <Routes>
            <Route path="/" element={<Scene />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Router>
      </Provider>
    </React.StrictMode>
  );






  // const root = ReactDOM.createRoot(rootElement);
  // root.render(
  //   <React.StrictMode>
  //     <BrowserRouter basename="/">
  //       <App />
  //     </BrowserRouter>
  //   </React.StrictMode>
  // );
}
