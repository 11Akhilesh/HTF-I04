import React, { useState } from 'react';
import Navbar from './Navbar';
import '../App.css';
import Loader from './Loader';

function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [source, setSource] = useState('');
  const [destination, setDestination] = useState('');
  const [preference, setPreference] = useState('4');
  const [routeSegments, setRouteSegments] = useState([]);
  const [summary, setSummary] = useState(null);

  const preferenceMap = {
    '1': 'fastest',
    '2': 'economic',
    '3': 'emissionless',
    '4': 'best',
  };

  const handleFetchRoutes = async () => {
    setLoading(true);
    setSummary(null);
    setRouteSegments([]);
    try {
      const response = await fetch(`http://localhost:5000/get-routes?source=${source}&destination=${destination}&length=50&width=50&height=50&weight=10`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });

      const data = await response.json();
      const selectedRoute = data[preferenceMap[preference]];

      if (selectedRoute && selectedRoute.length > 0) {
        const total_cost = selectedRoute.reduce((sum, seg) => sum + seg.cost_inr, 0);
        const total_duration = selectedRoute.reduce((sum, seg) => sum + seg.duration_hr, 0);
        const total_emissions = selectedRoute.reduce((sum, seg) => sum + seg.emissions_kg, 0);

        setSummary({ total_cost, total_duration, total_emissions });
        setRouteSegments(selectedRoute);
      }
    } catch (err) {
      console.error('Error fetching routes:', err);
    }
    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <Navbar />
      <div style={styles.content}>
        <h1 style={styles.heading}>📊 Logistics Aggregator Dashboard</h1>

        <div style={styles.form}>
          <input
            style={styles.input}
            type="text"
            placeholder="Enter Source"
            value={source}
            onChange={(e) => setSource(e.target.value)}
          />
          <input
            style={styles.input}
            type="text"
            placeholder="Enter Destination"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
          />
          <select
            style={styles.input}
            value={preference}
            onChange={(e) => setPreference(e.target.value)}
          >
            <option value="1">Fastest</option>
            <option value="2">Cheapest</option>
            <option value="3">Greenest</option>
            <option value="4">Balanced</option>
          </select>
          <button onClick={handleFetchRoutes} style={styles.button}>Get Optimized Routes</button>
        </div>

        {loading ? (
          <Loader />
        ) : (
          <>
            {summary && (
              <div style={styles.summaryCard}>
                <h2>📦 Route Summary</h2>
                <p><strong>Total Cost:</strong> ₹{summary.total_cost.toFixed(2)}</p>
                <p><strong>Total Duration:</strong> {summary.total_duration.toFixed(1)} hrs</p>
                <p><strong>Total Emissions:</strong> {summary.total_emissions.toFixed(2)} kg CO₂</p>
              </div>
            )}

            <div style={styles.results}>
              {routeSegments.length > 0 ? (
                routeSegments.map((seg, idx) => (
                  <div key={idx} style={styles.routeCard}>
                    <h3>🚚 Segment {idx + 1}</h3>
                    <p><strong>Mode:</strong> {seg.mode}</p>
                    <p><strong>From:</strong> {seg.from}</p>
                    <p><strong>To:</strong> {seg.to}</p>
                    <p><strong>Distance:</strong> {seg.distance_km.toFixed(2)} km</p>
                    <p><strong>Duration:</strong> {seg.duration_hr.toFixed(2)} hrs</p>
                    <p><strong>Cost:</strong> ₹{seg.cost_inr.toFixed(2)}</p>
                    <p><strong>Emissions:</strong> {seg.emissions_kg.toFixed(2)} kg CO₂</p>
                    <p><strong>Source Model:</strong> {seg.source_model}</p>
                  </div>
                ))
              ) : (
                <p>No routes found.</p>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    background: 'linear-gradient(to bottom right, #0f172a, #1e293b)',
    color: '#fff',
    fontFamily: 'Segoe UI, sans-serif',
  },
  content: {
    padding: '2rem',
    textAlign: 'center',
  },
  heading: {
    fontSize: '2.5rem',
    marginBottom: '1rem',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
    maxWidth: '400px',
    margin: 'auto',
  },
  input: {
    padding: '0.75rem',
    borderRadius: '8px',
    border: 'none',
    fontSize: '1rem',
  },
  button: {
    padding: '0.75rem',
    backgroundColor: '#3b82f6',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '1rem',
    cursor: 'pointer',
  },
  results: {
    marginTop: '2rem',
  },
  summaryCard: {
    backgroundColor: '#0f172a',
    padding: '1rem',
    borderRadius: '12px',
    margin: '1rem auto',
    maxWidth: '500px',
    boxShadow: '0 4px 8px rgba(0,0,0,0.3)',
  },
  routeCard: {
    backgroundColor: '#1e293b',
    borderRadius: '12px',
    padding: '1rem',
    marginBottom: '1rem',
    boxShadow: '0 4px 8px rgba(0,0,0,0.3)',
    maxWidth: '500px',
    margin: '1rem auto',
  },
};

export default Dashboard;
