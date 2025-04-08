// src/Navbar.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css'; // Ensure button-35 styles are available

const Navbar = () => {
  const navigate = useNavigate();

  return (
    <nav style={styles.navbar}>
      <div style={styles.brand}>RouteSphere</div>
      <div style={styles.navLinks}>
        <button className="button-35" onClick={() => navigate('/dashboard')}>Dashboard</button>
        <button className="button-35" onClick={() => navigate('/about')}>About Us</button>
        <button className="button-35" onClick={() => navigate('/contact')}>Contact</button>
        <button className="button-35" onClick={() => navigate('/help')}>Help</button>
      </div>
    </nav>
  );
};

const styles = {
  navbar: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '1rem 2rem',
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
    color: '#fff'
  },
  brand: {
    fontSize: '1.5rem',
    fontWeight: 'bold'
  },
  navLinks: {
    display: 'flex',
    gap: '1rem'
  }
};

export default Navbar;
