import React from 'react';
import { Bar, Pie } from 'react-chartjs-2';
import '../styles/Dashboard.css';

function Dashboard({ dataset, onDownloadReport }) {
  const avgData = {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [
      {
        label: 'Average Values',
        data: [dataset.avg_flowrate, dataset.avg_pressure, dataset.avg_temperature],
        backgroundColor: ['rgba(54, 162, 235, 0.6)', 'rgba(255, 99, 132, 0.6)', 'rgba(255, 206, 86, 0.6)'],
        borderColor: ['rgba(54, 162, 235, 1)', 'rgba(255, 99, 132, 1)', 'rgba(255, 206, 86, 1)'],
        borderWidth: 1,
      },
    ],
  };

  const typeData = {
    labels: Object.keys(dataset.equipment_types_dict || {}),
    datasets: [
      {
        data: Object.values(dataset.equipment_types_dict || {}),
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
        ],
      },
    ],
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div>
          <h2>{dataset.filename}</h2>
          <p>Uploaded: {new Date(dataset.upload_date).toLocaleString()}</p>
        </div>
        <button onClick={() => onDownloadReport(dataset.id)} className="btn-download">
          Download PDF Report
        </button>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Equipment</h3>
          <p className="stat-value">{dataset.total_count}</p>
        </div>
        <div className="stat-card">
          <h3>Avg Flowrate</h3>
          <p className="stat-value">{dataset.avg_flowrate.toFixed(2)}</p>
        </div>
        <div className="stat-card">
          <h3>Avg Pressure</h3>
          <p className="stat-value">{dataset.avg_pressure.toFixed(2)}</p>
        </div>
        <div className="stat-card">
          <h3>Avg Temperature</h3>
          <p className="stat-value">{dataset.avg_temperature.toFixed(2)}</p>
        </div>
      </div>

      <div className="charts-grid">
        <div className="chart-card">
          <h3>Average Parameters</h3>
          <Bar 
            data={avgData} 
            options={{ 
              responsive: true, 
              maintainAspectRatio: true,
              plugins: {
                legend: {
                  display: true,
                  position: 'top',
                }
              },
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }} 
          />
        </div>
        <div className="chart-card">
          <h3>Equipment Type Distribution</h3>
          <Pie 
            data={typeData} 
            options={{ 
              responsive: true, 
              maintainAspectRatio: true,
              plugins: {
                legend: {
                  position: 'right',
                }
              }
            }} 
          />
        </div>
      </div>

      <div className="table-card">
        <h3>Equipment Details</h3>
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Equipment Name</th>
                <th>Type</th>
                <th>Flowrate</th>
                <th>Pressure</th>
                <th>Temperature</th>
              </tr>
            </thead>
            <tbody>
              {dataset.equipment?.map((eq) => (
                <tr key={eq.id}>
                  <td>{eq.equipment_name}</td>
                  <td>{eq.equipment_type}</td>
                  <td>{eq.flowrate.toFixed(2)}</td>
                  <td>{eq.pressure.toFixed(2)}</td>
                  <td>{eq.temperature.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
