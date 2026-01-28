import React from 'react';
import { Bar, Pie, Line } from 'react-chartjs-2';
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
          'rgba(255, 99, 132, 0.8)',
          'rgba(54, 162, 235, 0.8)',
          'rgba(255, 206, 86, 0.8)',
          'rgba(75, 192, 192, 0.8)',
          'rgba(153, 102, 255, 0.8)',
          'rgba(255, 159, 64, 0.8)',
          'rgba(201, 203, 207, 0.8)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)',
          'rgba(201, 203, 207, 1)',
        ],
        borderWidth: 2,
        hoverOffset: 15,
      },
    ],
  };

  // Line chart - Parameter trends across equipment
  const equipment = dataset.equipment || [];
  const trendData = {
    labels: equipment.map(eq => eq.equipment_name),
    datasets: [
      {
        label: 'Flowrate',
        data: equipment.map(eq => eq.flowrate),
        borderColor: 'rgba(54, 162, 235, 1)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        tension: 0.4,
        borderWidth: 3,
        pointRadius: 5,
        pointHoverRadius: 7,
        pointBackgroundColor: 'rgba(54, 162, 235, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(54, 162, 235, 1)',
        fill: true,
      },
      {
        label: 'Pressure',
        data: equipment.map(eq => eq.pressure),
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        tension: 0.4,
        borderWidth: 3,
        pointRadius: 5,
        pointHoverRadius: 7,
        pointBackgroundColor: 'rgba(255, 99, 132, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(255, 99, 132, 1)',
        fill: true,
      },
      {
        label: 'Temperature',
        data: equipment.map(eq => eq.temperature),
        borderColor: 'rgba(255, 206, 86, 1)',
        backgroundColor: 'rgba(255, 206, 86, 0.2)',
        tension: 0.4,
        borderWidth: 3,
        pointRadius: 5,
        pointHoverRadius: 7,
        pointBackgroundColor: 'rgba(255, 206, 86, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(255, 206, 86, 1)',
        fill: true,
      },
    ],
  };

  // Horizontal bar chart - Top 5 equipment by flowrate
  const sortedEquipment = [...equipment].sort((a, b) => b.flowrate - a.flowrate).slice(0, 5);
  const topFlowrateData = {
    labels: sortedEquipment.map(eq => eq.equipment_name),
    datasets: [
      {
        label: 'Flowrate',
        data: sortedEquipment.map(eq => eq.flowrate),
        backgroundColor: [
          'rgba(153, 102, 255, 0.7)',
          'rgba(54, 162, 235, 0.7)',
          'rgba(255, 206, 86, 0.7)',
          'rgba(75, 192, 192, 0.7)',
          'rgba(255, 99, 132, 0.7)',
        ],
        borderColor: [
          'rgba(153, 102, 255, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(255, 99, 132, 1)',
        ],
        borderWidth: 2,
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
                  display: false,
                },
                tooltip: {
                  backgroundColor: 'rgba(0, 0, 0, 0.8)',
                  titleColor: '#fff',
                  bodyColor: '#fff',
                  borderColor: '#666',
                  borderWidth: 1,
                  padding: 12,
                  displayColors: true,
                  boxWidth: 15,
                  boxHeight: 15,
                  bodyFont: {
                    size: 14
                  },
                  titleFont: {
                    size: 15,
                    weight: 'bold'
                  },
                  callbacks: {
                    label: function(context) {
                      const label = context.dataset.label || '';
                      const value = context.parsed.y.toFixed(2);
                      return `${label}: ${value} units`;
                    },
                    afterLabel: function(context) {
                      // Add additional context about the parameter
                      const paramIndex = context.dataIndex;
                      const params = ['Flowrate', 'Pressure', 'Temperature'];
                      const values = [dataset.avg_flowrate, dataset.avg_pressure, dataset.avg_temperature];
                      const equipment = dataset.equipment || [];
                      
                      if (equipment.length > 0) {
                        const paramValues = equipment.map(eq => {
                          if (paramIndex === 0) return eq.flowrate;
                          if (paramIndex === 1) return eq.pressure;
                          return eq.temperature;
                        });
                        
                        const min = Math.min(...paramValues).toFixed(2);
                        const max = Math.max(...paramValues).toFixed(2);
                        
                        return `Range: ${min} - ${max}`;
                      }
                      return '';
                    }
                  }
                }
              },
              scales: {
                y: {
                  beginAtZero: true,
                  grace: '5%',
                  grid: {
                    color: 'rgba(0, 0, 0, 0.05)',
                    lineWidth: 1
                  },
                  ticks: {
                    font: {
                      size: 12
                    },
                    padding: 8
                  }
                },
                x: {
                  grid: {
                    display: false
                  },
                  ticks: {
                    font: {
                      size: 13,
                      weight: '500'
                    },
                    padding: 8
                  }
                }
              },
              layout: {
                padding: {
                  top: 25,
                  right: 10,
                  bottom: 10,
                  left: 10
                }
              }
            }} 
            plugins={[{
              id: 'barValueLabels',
              afterDatasetDraw(chart) {
                const { ctx } = chart;
                chart.getDatasetMeta(0).data.forEach((bar, index) => {
                  const value = chart.data.datasets[0].data[index].toFixed(2);
                  
                  ctx.save();
                  ctx.font = 'bold 13px Arial';
                  ctx.fillStyle = '#333';
                  ctx.textAlign = 'center';
                  ctx.textBaseline = 'bottom';
                  
                  // Position text above the bar with more space
                  ctx.fillText(value, bar.x, bar.y - 8);
                  
                  ctx.restore();
                });
              }
            }]}
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
                  labels: {
                    padding: 15,
                    font: {
                      size: 13,
                      weight: '500'
                    },
                    generateLabels: (chart) => {
                      const data = chart.data;
                      if (data.labels.length && data.datasets.length) {
                        const dataset = data.datasets[0];
                        const total = dataset.data.reduce((acc, val) => acc + val, 0);
                        return data.labels.map((label, i) => {
                          const value = dataset.data[i];
                          const percentage = ((value / total) * 100).toFixed(1);
                          return {
                            text: `${label}: ${value} (${percentage}%)`,
                            fillStyle: dataset.backgroundColor[i],
                            strokeStyle: dataset.borderColor[i],
                            lineWidth: 2,
                            hidden: false,
                            index: i
                          };
                        });
                      }
                      return [];
                    }
                  }
                },
                tooltip: {
                  callbacks: {
                    label: function(context) {
                      const label = context.label || '';
                      const value = context.parsed;
                      const total = context.dataset.data.reduce((acc, val) => acc + val, 0);
                      const percentage = ((value / total) * 100).toFixed(1);
                      return `${label}: ${value} units (${percentage}%)`;
                    }
                  },
                  backgroundColor: 'rgba(0, 0, 0, 0.8)',
                  titleColor: '#fff',
                  bodyColor: '#fff',
                  borderColor: '#666',
                  borderWidth: 1,
                  padding: 12,
                  displayColors: true,
                  boxWidth: 15,
                  boxHeight: 15,
                  bodyFont: {
                    size: 14
                  },
                  titleFont: {
                    size: 15,
                    weight: 'bold'
                  }
                }
              }
            }} 
            plugins={[{
              id: 'percentageLabels',
              afterDatasetDraw(chart) {
                const { ctx, data } = chart;
                const dataset = data.datasets[0];
                const total = dataset.data.reduce((acc, val) => acc + val, 0);
                
                chart.getDatasetMeta(0).data.forEach((arc, index) => {
                  const value = dataset.data[index];
                  const percentage = ((value / total) * 100).toFixed(1);
                  
                  // Get the midpoint of the arc
                  const { x, y } = arc.tooltipPosition();
                  
                  // Draw percentage text
                  ctx.save();
                  ctx.font = 'bold 14px Arial';
                  ctx.fillStyle = '#fff';
                  ctx.textAlign = 'center';
                  ctx.textBaseline = 'middle';
                  
                  // Draw text with shadow for better visibility
                  ctx.shadowColor = 'rgba(0, 0, 0, 0.7)';
                  ctx.shadowBlur = 4;
                  ctx.fillText(`${percentage}%`, x, y);
                  
                  ctx.restore();
                });
              }
            }]}
          />
        </div>
      </div>

      <div className="charts-grid">
        <div className="chart-card chart-wide">
          <h3>Parameter Trends Across Equipment</h3>
          <Line 
            data={trendData} 
            options={{ 
              responsive: true, 
              maintainAspectRatio: true,
              interaction: {
                mode: 'index',
                intersect: false,
              },
              plugins: {
                legend: {
                  display: true,
                  position: 'top',
                  labels: {
                    padding: 15,
                    font: {
                      size: 13,
                      weight: '500'
                    },
                    usePointStyle: true,
                    pointStyle: 'circle',
                    boxWidth: 8,
                    boxHeight: 8
                  }
                },
                tooltip: {
                  backgroundColor: 'rgba(0, 0, 0, 0.9)',
                  titleColor: '#fff',
                  bodyColor: '#fff',
                  borderColor: '#666',
                  borderWidth: 1,
                  padding: 15,
                  displayColors: true,
                  boxWidth: 15,
                  boxHeight: 15,
                  bodyFont: {
                    size: 13
                  },
                  titleFont: {
                    size: 14,
                    weight: 'bold'
                  },
                  callbacks: {
                    title: function(tooltipItems) {
                      return `Equipment: ${tooltipItems[0].label}`;
                    },
                    label: function(context) {
                      const label = context.dataset.label || '';
                      const value = context.parsed.y.toFixed(2);
                      
                      // Calculate deviation from average
                      const allValues = context.dataset.data;
                      const avg = (allValues.reduce((a, b) => a + b, 0) / allValues.length).toFixed(2);
                      const deviation = (value - avg).toFixed(2);
                      const sign = deviation > 0 ? '+' : '';
                      
                      return `${label}: ${value} (${sign}${deviation} from avg ${avg})`;
                    },
                    afterBody: function(tooltipItems) {
                      const dataIndex = tooltipItems[0].dataIndex;
                      const eq = equipment[dataIndex];
                      return `\nType: ${eq.equipment_type}`;
                    }
                  }
                }
              },
              scales: {
                y: {
                  beginAtZero: true,
                  grid: {
                    color: 'rgba(0, 0, 0, 0.05)',
                    lineWidth: 1
                  },
                  ticks: {
                    font: {
                      size: 12
                    },
                    padding: 8
                  },
                  title: {
                    display: true,
                    text: 'Value',
                    font: {
                      size: 13,
                      weight: 'bold'
                    },
                    padding: 10
                  }
                },
                x: {
                  grid: {
                    color: 'rgba(0, 0, 0, 0.05)',
                    lineWidth: 1
                  },
                  ticks: {
                    font: {
                      size: 11
                    },
                    padding: 8,
                    maxRotation: 45,
                    minRotation: 45
                  },
                  title: {
                    display: true,
                    text: 'Equipment',
                    font: {
                      size: 13,
                      weight: 'bold'
                    },
                    padding: 10
                  }
                }
              }
            }} 
          />
        </div>
      </div>

      <div className="charts-grid">
        <div className="chart-card chart-wide">
          <h3>Top 5 Equipment by Flowrate</h3>
          <Bar 
            data={topFlowrateData} 
            options={{ 
              indexAxis: 'y',
              responsive: true, 
              maintainAspectRatio: true,
              plugins: {
                legend: {
                  display: false,
                },
                tooltip: {
                  backgroundColor: 'rgba(0, 0, 0, 0.9)',
                  titleColor: '#fff',
                  bodyColor: '#fff',
                  borderColor: '#666',
                  borderWidth: 1,
                  padding: 15,
                  displayColors: true,
                  boxWidth: 15,
                  boxHeight: 15,
                  bodyFont: {
                    size: 13
                  },
                  titleFont: {
                    size: 14,
                    weight: 'bold'
                  },
                  callbacks: {
                    title: function(tooltipItems) {
                      const index = tooltipItems[0].dataIndex;
                      const eq = sortedEquipment[index];
                      return `${eq.equipment_name} (${eq.equipment_type})`;
                    },
                    label: function(context) {
                      const value = context.parsed.x.toFixed(2);
                      const index = context.dataIndex;
                      const eq = sortedEquipment[index];
                      const avgFlowrate = dataset.avg_flowrate.toFixed(2);
                      const deviation = (eq.flowrate - dataset.avg_flowrate).toFixed(2);
                      const percentAboveAvg = (((eq.flowrate - dataset.avg_flowrate) / dataset.avg_flowrate) * 100).toFixed(1);
                      
                      return [
                        `Flowrate: ${value}`,
                        `Deviation: +${deviation} (+${percentAboveAvg}% above avg)`,
                        `Average Flowrate: ${avgFlowrate}`
                      ];
                    },
                    afterBody: function(tooltipItems) {
                      const index = tooltipItems[0].dataIndex;
                      const eq = sortedEquipment[index];
                      return `\nPressure: ${eq.pressure.toFixed(2)}\nTemperature: ${eq.temperature.toFixed(2)}`;
                    }
                  }
                }
              },
              scales: {
                x: {
                  beginAtZero: true,
                  grid: {
                    color: 'rgba(0, 0, 0, 0.08)',
                    lineWidth: 1
                  },
                  ticks: {
                    font: {
                      size: 12
                    },
                    padding: 8
                  },
                  title: {
                    display: true,
                    text: 'Flowrate',
                    font: {
                      size: 13,
                      weight: 'bold'
                    },
                    padding: 10
                  }
                },
                y: {
                  grid: {
                    display: false
                  },
                  ticks: {
                    font: {
                      size: 13,
                      weight: '500'
                    },
                    padding: 10
                  }
                }
              }
            }}
            plugins={[{
              id: 'horizontalBarValues',
              afterDatasetDraw(chart) {
                const { ctx } = chart;
                chart.getDatasetMeta(0).data.forEach((bar, index) => {
                  const value = chart.data.datasets[0].data[index].toFixed(2);
                  
                  ctx.save();
                  ctx.font = 'bold 13px Arial';
                  ctx.fillStyle = '#333';
                  ctx.textAlign = 'left';
                  ctx.textBaseline = 'middle';
                  
                  // Position text at the end of the bar
                  ctx.fillText(value, bar.x + 5, bar.y);
                  
                  ctx.restore();
                });
              }
            }]}
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
