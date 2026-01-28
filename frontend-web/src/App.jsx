import React, { useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { useAuth } from './hooks/useAuth';
import { useDatasets } from './hooks/useDatasets';
import Login from './components/Login';
import Navbar from './components/Navbar';
import Upload from './components/Upload';
import Dashboard from './components/Dashboard';
import History from './components/History';
import './App.css';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

function App() {
  const [view, setView] = useState('upload');
  
  // Authentication logic
  const {
    isAuthenticated,
    username,
    password,
    error: authError,
    setUsername,
    setPassword,
    login,
    logout,
  } = useAuth();

  // Dataset management logic
  const {
    datasets,
    currentDataset,
    loading,
    error: datasetError,
    setCurrentDataset,
    uploadFile,
    downloadReport,
  } = useDatasets(isAuthenticated);

  // Handlers
  const handleLogin = async (e) => {
    const success = await login(e);
    if (success) {
      setView('upload');
    }
  };

  const handleLogout = () => {
    logout();
    setCurrentDataset(null);
    setView('upload');
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      await uploadFile(file);
      setView('dashboard');
    } catch (err) {
      console.error('Upload failed:', err);
    }
  };

  // Render login screen if not authenticated
  if (!isAuthenticated) {
    return (
      <Login
        username={username}
        password={password}
        onUsernameChange={setUsername}
        onPasswordChange={setPassword}
        onSubmit={handleLogin}
        error={authError}
      />
    );
  }

  // Render main application
  return (
    <div className="app">
      <Navbar 
        view={view} 
        onViewChange={setView} 
        onLogout={handleLogout} 
      />

      <div className="content">
        {view === 'upload' && (
          <Upload 
            onFileUpload={handleFileUpload} 
            loading={loading} 
            error={datasetError} 
          />
        )}

        {view === 'dashboard' && currentDataset && (
          <Dashboard 
            dataset={currentDataset} 
            onDownloadReport={downloadReport} 
          />
        )}

        {view === 'history' && (
          <History 
            datasets={datasets} 
            onSelectDataset={setCurrentDataset} 
            onViewDashboard={() => setView('dashboard')} 
          />
        )}
      </div>
    </div>
  );
}

export default App;