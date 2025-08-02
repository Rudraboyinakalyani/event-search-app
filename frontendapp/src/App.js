import React from 'react';
import SearchPage from './components/Search';
import UploadPage from './components/UploadPage';
import './components/Search.css';

import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';


function App() {
  return (
    <Router>
      <nav>
        <Link to="/">Upload</Link> | <Link to="/search">Search</Link>
      </nav>
      <Routes>
        <Route path="/" element={<UploadPage />} />
        <Route path="/search" element={<SearchPage />} />
      </Routes>
    </Router>
  );
}

export default App;

