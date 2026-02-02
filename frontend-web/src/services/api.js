import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Get auth token from localStorage
const getAuthHeader = () => {
  const token = localStorage.getItem('token');
  return { Authorization: `Bearer ${token}` };
};

// Authentication APIs
export const authAPI = {
  login: async (username, password) => {
    const response = await axios.post(`${API_URL}/token/`, {
      username,
      password,
    });
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('token');
  },

  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  },

  setToken: (token) => {
    localStorage.setItem('token', token);
  },
};

// Dataset APIs
export const datasetAPI = {
  getAll: async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('No authentication token found');
    }
    const response = await axios.get(`${API_URL}/datasets/`, {
      headers: getAuthHeader(),
    });
    return response.data;
  },

  upload: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await axios.post(`${API_URL}/datasets/`, formData, {
      headers: {
        ...getAuthHeader(),
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  downloadReport: async (datasetId) => {
    const response = await axios.get(
      `${API_URL}/datasets/${datasetId}/report/`,
      {
        headers: getAuthHeader(),
        responseType: 'blob',
      }
    );
    return response.data;
  },
};

// Utility function for downloading files
export const downloadFile = (blob, filename) => {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};
