import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import SignUp from './components/SignUp';
import Header from './components/Header';
import Features from './components/Features';
import Footer from './components/Footer';
import Dashboard from './pages/Dashboard'; // Update the path if necessary
import './App.css';

const App = () => {
  return (
    <Router>
      <Header />
      <Features />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />
      </Routes>
      <Footer />
    </Router>
  );
};

export default App;
