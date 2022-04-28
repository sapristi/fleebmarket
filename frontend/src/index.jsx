import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import {App, ItemsApp} from './App';
import reportWebVitals from './reportWebVitals';
import { RecoilRoot } from 'recoil';
import { BrowserRouter, Routes, Route} from "react-router-dom";

const container = document.getElementById('root');
const root = createRoot(container);
root.render(
  <React.StrictMode>
    <RecoilRoot>
    <BrowserRouter>
      <Routes>
        <Route path="search" element={<App />} />
        <Route path="search_item" element={<ItemsApp />} />
      </Routes>
    </BrowserRouter>
    </RecoilRoot>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
