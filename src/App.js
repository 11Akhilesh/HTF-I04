import React from 'react';
import { Routes, Route } from 'react-router-dom';
import FrontPage from './components/Frontpage';
import Dashboard from './components/Dashboard';
import 'bootstrap/dist/css/bootstrap.min.css'; 

function App() {
  return (
    <Routes>
      <Route path="/" element={<FrontPage />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  );
}

export default App;
