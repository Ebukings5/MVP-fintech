import React from 'react';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <h1>Finance Manager</h1>
      <p>Your personal financial assistant</p>
      <a href="/signup" className="btn-primary">Get Started</a>
      <a href="/login" className="btn-secondary">Login</a>
    </header>
  );
};

export default Header;
