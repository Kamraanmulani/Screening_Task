import React from 'react';
import '../styles/History.css';

function History({ datasets, onSelectDataset, onViewDashboard }) {
  return (
    <div className="history-section">
      <h2>Upload History (Last 5)</h2>
      <div className="history-grid">
        {datasets.map((dataset) => (
          <div key={dataset.id} className="history-card">
            <h3>{dataset.filename}</h3>
            <p>Uploaded: {new Date(dataset.upload_date).toLocaleString()}</p>
            <p>Total Equipment: {dataset.total_count}</p>
            <button
              onClick={() => {
                onSelectDataset(dataset);
                onViewDashboard();
              }}
              className="btn-view"
            >
              View Details
            </button>
          </div>
        ))}
        {datasets.length === 0 && <p className="no-data">No datasets uploaded yet.</p>}
      </div>
    </div>
  );
}

export default History;
