import { useState, useEffect } from 'react';
import { authAPI } from '../services/api';

export const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    if (authAPI.isAuthenticated()) {
      setIsAuthenticated(true);
    }
  }, []);

  const login = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const data = await authAPI.login(username, password);
      authAPI.setToken(data.access);
      setIsAuthenticated(true);
      return true;
    } catch (err) {
      setError('Invalid credentials');
      return false;
    }
  };

  const logout = () => {
    authAPI.logout();
    setIsAuthenticated(false);
    setUsername('');
    setPassword('');
  };

  return {
    isAuthenticated,
    username,
    password,
    error,
    setUsername,
    setPassword,
    login,
    logout,
  };
};
