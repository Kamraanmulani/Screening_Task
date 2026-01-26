import React from 'react';
import '../styles/Login.css';

function Login({ username, password, onUsernameChange, onPasswordChange, onSubmit, error }) {
  return (
    <div className="login-container">
      <div className="login-card">
        <h1>Chemical Equipment Visualizer</h1>
        <p className="login-subtitle">IIT Bombay Internship Task</p>
        <form onSubmit={onSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => onUsernameChange(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => onPasswordChange(e.target.value)}
              required
            />
          </div>
          {error && <div className="error-message">{error}</div>}
          <button type="submit" className="login-btn">
            Login
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
