import React from 'react';
import '../styles/Upload.css';

function Upload({ onFileUpload, loading, error }) {
  return (
    <div className="upload-section">
      <h2>Upload CSV File</h2>
      <div className="upload-card">
        <input
          type="file"
          accept=".csv"
          onChange={onFileUpload}
          disabled={loading}
          id="file-upload"
        />
        <label htmlFor="file-upload" className="upload-label">
          {loading ? 'Uploading...' : 'Choose CSV File'}
        </label>
        {error && <div className="upload-error">{error}</div>}
        <p className="upload-hint">
          CSV should contain: Equipment Name, Type, Flowrate, Pressure, Temperature
        </p>
      </div>
    </div>
  );
}

export default Upload;
