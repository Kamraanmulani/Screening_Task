import React from 'react';
import '../styles/Navbar.css';

function Navbar({ view, onViewChange, onLogout }) {
  return (
    <nav className="navbar">
      <h1>Chemical Equipment Visualizer</h1>
      <div className="nav-links">
        <button 
          onClick={() => onViewChange('upload')} 
          className={view === 'upload' ? 'active' : ''}
        >
          Upload
        </button>
        <button 
          onClick={() => onViewChange('dashboard')} 
          className={view === 'dashboard' ? 'active' : ''}
        >
          Dashboard
        </button>
        <button 
          onClick={() => onViewChange('history')} 
          className={view === 'history' ? 'active' : ''}
        >
          History
        </button>
        <button onClick={onLogout} className="btn-logout">
          Logout
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
