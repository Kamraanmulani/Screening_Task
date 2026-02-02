import { useState, useEffect } from 'react';
import { datasetAPI, downloadFile } from '../services/api';

export const useDatasets = (isAuthenticated) => {
  const [datasets, setDatasets] = useState([]);
  const [currentDataset, setCurrentDataset] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isAuthenticated) {
      loadDatasets();
    }
  }, [isAuthenticated]);

  const loadDatasets = async () => {
    if (!isAuthenticated) {
      return;
    }
    try {
      const data = await datasetAPI.getAll();
      setDatasets(data);
      if (data.length > 0) {
        setCurrentDataset(data[0]);
      }
    } catch (err) {
      console.error('Error loading datasets:', err);
      if (err.response?.status === 401) {
        console.log('Authentication token invalid or expired');
      }
    }
  };

  const uploadFile = async (file) => {
    setLoading(true);
    setError('');
    try {
      const data = await datasetAPI.upload(file);
      setCurrentDataset(data);
      await loadDatasets();
      setError('');
      return data;
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Error uploading file';
      setError(errorMsg);
      throw new Error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = async (datasetId) => {
    try {
      console.log('Downloading report for dataset:', datasetId);
      
      const blob = await datasetAPI.downloadReport(datasetId);
      
      console.log('Response received, creating PDF blob');
      
      const pdfBlob = new Blob([blob], { type: 'application/pdf' });
      downloadFile(pdfBlob, 'Chemical Equipment Analysis Report.pdf');
      
      console.log('PDF download initiated successfully');
      alert('PDF report downloaded successfully!');
    } catch (err) {
      console.error('Error downloading report:', err);
      const errorMsg = err.response?.data?.error || err.message || 'Error downloading report';
      setError(errorMsg);
      alert('Failed to download PDF report: ' + errorMsg);
    }
  };

  return {
    datasets,
    currentDataset,
    loading,
    error,
    setCurrentDataset,
    loadDatasets,
    uploadFile,
    downloadReport,
  };
};
