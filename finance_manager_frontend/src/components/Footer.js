import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <p>&copy; {new Date().getFullYear()} Finance Manager. All rights reserved.</p>
      <a href="/contact">Contact Us</a>
    </footer>
  );
};

export default Footer;
