import React from 'react';
import { useNavigate } from 'react-router-dom';
import bgImage from './image.png';
import '../App.css'; // Corrected the import path

const FrontPage = () => {
  const navigate = useNavigate();

  const handleStart = () => {
    navigate('/dashboard');
  };

  return (
    <div style={styles.container}>
      {/* Navbar */}
      <nav style={styles.navbar}>
        <div style={styles.brand}>RouteSphere</div>
        <div style={styles.navLinks}>
        <button className="button-35" onClick={() => navigate('/about')}>About Us</button>
<button className="button-35" onClick={() => navigate('/contact')}>Contact</button>
<button className="button-35" onClick={() => navigate('/help')}>Help</button>


        </div>
      </nav>

      {/* Hero Content */}
      <div style={styles.hero}>
        <h1 className="fade-in" style={styles.title}>AI Logistics Planner</h1>
        <p className="fade-in-delay" style={styles.subtitle}>Optimize speed, cost & sustainability in real-time.</p>
        <button className="button-35 fade-in-more-delay" onClick={handleStart}>Start Planning</button>
        </div>
    </div>
  );
};

const styles = {
  container: {
    height: '100vh',
    backgroundImage: `url(${bgImage})`, // Fixed syntax
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    color: '#fff',
    fontFamily: 'Segoe UI, sans-serif',
    position: 'relative'
  },
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
    gap: '1.5rem'
  },
  navLink: {
    color: '#fff',
    textDecoration: 'none',
    fontSize: '1rem',
    background: 'none',
    border: 'none',
    cursor: 'pointer',
    padding: 0
  },
  hero: {
    textAlign: 'center',
    paddingTop: '25vh',
    backgroundColor: 'rgba(0, 0, 0, 0.3)',
    height: '100%',
  },
  title: {
    fontSize: '3rem',
    marginBottom: '10px',
    textShadow: '2px 2px 4px rgba(0,0,0,0.6)'
  },
  subtitle: {
    fontSize: '1.2rem',
    marginBottom: '30px',
    textShadow: '1px 1px 2px rgba(0,0,0,0.5)'
  },
  button: {
    fontSize: '1rem',
    padding: '12px 24px',
    cursor: 'pointer',
    border: 'none',
    borderRadius: '8px',
    backgroundColor: '#2563eb',
    color: '#fff',
    boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
  }
};

export default FrontPage;