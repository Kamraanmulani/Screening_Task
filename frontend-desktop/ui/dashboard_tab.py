"""
Dashboard Tab - Data visualization interface
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QTableWidget, QTableWidgetItem, QGroupBox,
    QFormLayout, QFileDialog, QMessageBox, QScrollArea
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from config import EQUIPMENT_HEADERS, PDF_FILTER


class DashboardTab(QWidget):
    """Tab for displaying dataset dashboard with charts and statistics"""
    
    def __init__(self, api_service):
        super().__init__()
        self.api_service = api_service
        self.current_dataset = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components"""
        # Main layout for the tab
        main_layout = QVBoxLayout()
        
        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Create a widget to hold all content
        content_widget = QWidget()
        self.layout = QVBoxLayout()
        
        # Dataset info
        self.dataset_info_label = QLabel("No dataset loaded")
        self.dataset_info_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.layout.addWidget(self.dataset_info_label)
        
        # Download report button
        download_btn = QPushButton("Download PDF Report")
        download_btn.clicked.connect(self.download_report)
        self.layout.addWidget(download_btn)
        
        # Statistics
        self.stats_group = QGroupBox("Summary Statistics")
        self.stats_layout = QFormLayout()
        self.stats_group.setLayout(self.stats_layout)
        self.layout.addWidget(self.stats_group)
        
        # Charts
        charts_layout = QHBoxLayout()
        
        # Bar chart
        self.bar_figure = Figure(figsize=(6, 4))
        self.bar_canvas = FigureCanvas(self.bar_figure)
        charts_layout.addWidget(self.bar_canvas)
        
        # Pie chart
        self.pie_figure = Figure(figsize=(6, 4))
        self.pie_canvas = FigureCanvas(self.pie_figure)
        charts_layout.addWidget(self.pie_canvas)
        
        self.layout.addLayout(charts_layout)
        
        # New charts row
        new_charts_layout = QHBoxLayout()
        
        # Line chart - Parameter trends
        self.line_figure = Figure(figsize=(7, 3.5))
        self.line_canvas = FigureCanvas(self.line_figure)
        new_charts_layout.addWidget(self.line_canvas)
        
        # Horizontal bar chart - Top 5
        self.top5_figure = Figure(figsize=(6, 4))
        self.top5_canvas = FigureCanvas(self.top5_figure)
        new_charts_layout.addWidget(self.top5_canvas)
        
        self.layout.addLayout(new_charts_layout)
        
        # Set the layout to content widget
        content_widget.setLayout(self.layout)
        
        # Set content widget to scroll area
        scroll_area.setWidget(content_widget)
        
        # Add scroll area to main layout
        main_layout.addWidget(scroll_area)
        
        self.setLayout(main_layout)
    
    def update_dashboard(self, dataset):
        """Update dashboard with dataset information"""
        if not dataset:
            return
        
        self.current_dataset = dataset
        
        # Update dataset info
        self.dataset_info_label.setText(
            f"Dataset: {dataset['filename']} | "
            f"Uploaded: {dataset['upload_date']} | "
            f"Total Equipment: {dataset['total_count']}"
        )
        
        # Update statistics
        self._update_statistics(dataset)
        
        # Update charts
        self._update_bar_chart(dataset)
        self._update_pie_chart(dataset)
        self._update_line_chart(dataset)
        self._update_top5_chart(dataset)
    
    def _update_statistics(self, dataset):
        """Update the statistics section"""
        # Clear existing statistics
        for i in reversed(range(self.stats_layout.count())):
            self.stats_layout.itemAt(i).widget().setParent(None)
        
        # Add new statistics
        self.stats_layout.addRow("Total Equipment:", QLabel(str(dataset['total_count'])))
        self.stats_layout.addRow("Avg Flowrate:", QLabel(f"{dataset['avg_flowrate']:.2f}"))
        self.stats_layout.addRow("Avg Pressure:", QLabel(f"{dataset['avg_pressure']:.2f}"))
        self.stats_layout.addRow("Avg Temperature:", QLabel(f"{dataset['avg_temperature']:.2f}"))
    
    def _update_bar_chart(self, dataset):
        """Update the bar chart"""
        self.bar_figure.clear()
        ax = self.bar_figure.add_subplot(111)
        
        parameters = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            dataset['avg_flowrate'],
            dataset['avg_pressure'],
            dataset['avg_temperature']
        ]
        
        ax.bar(parameters, values, color=['#36a2eb', '#ff6384', '#ffce56'])
        ax.set_title('Average Parameters')
        ax.set_ylabel('Value')
        
        self.bar_canvas.draw()
    
    def _update_pie_chart(self, dataset):
        """Update the pie chart"""
        self.pie_figure.clear()
        ax = self.pie_figure.add_subplot(111)
        
        equipment_types = dataset.get('equipment_types_dict', {})
        if equipment_types:
            ax.pie(
                equipment_types.values(),
                labels=equipment_types.keys(),
                autopct='%1.1f%%',
                startangle=90
            )
            ax.set_title('Equipment Type Distribution')
        
        self.pie_canvas.draw()
    
    def _update_line_chart(self, dataset):
        """Update the line chart - parameter trends"""
        self.line_figure.clear()
        ax = self.line_figure.add_subplot(111)
        
        equipment = dataset.get('equipment', [])
        if equipment:
            equipment_names = [eq['equipment_name'] for eq in equipment]
            flowrates = [eq['flowrate'] for eq in equipment]
            pressures = [eq['pressure'] for eq in equipment]
            temperatures = [eq['temperature'] for eq in equipment]
            
            x_positions = range(len(equipment_names))
            
            ax.plot(x_positions, flowrates, marker='o', label='Flowrate', 
                   color='#36a2eb', linewidth=2, markersize=6)
            ax.plot(x_positions, pressures, marker='s', label='Pressure', 
                   color='#ff6384', linewidth=2, markersize=6)
            ax.plot(x_positions, temperatures, marker='^', label='Temperature', 
                   color='#ffce56', linewidth=2, markersize=6)
            
            ax.set_title('Parameter Trends Across Equipment', fontweight='bold')
            ax.set_xlabel('Equipment')
            ax.set_ylabel('Value')
            ax.set_xticks(x_positions)
            ax.set_xticklabels(equipment_names, rotation=45, ha='right')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
        self.line_figure.tight_layout()
        self.line_canvas.draw()
    
    def _update_top5_chart(self, dataset):
        """Update the horizontal bar chart - top 5 equipment"""
        self.top5_figure.clear()
        ax = self.top5_figure.add_subplot(111)
        
        equipment = dataset.get('equipment', [])
        if equipment:
            # Sort by flowrate and get top 5
            sorted_equipment = sorted(equipment, key=lambda x: x['flowrate'], reverse=True)[:5]
            
            names = [eq['equipment_name'] for eq in sorted_equipment]
            flowrates = [eq['flowrate'] for eq in sorted_equipment]
            
            # Create horizontal bar chart with colorful bars
            y_positions = range(len(names))
            colors = ['#9966ff', '#36a2eb', '#ffce56', '#4bc0c0', '#ff6384']
            ax.barh(y_positions, flowrates, color=colors[:len(names)], 
                   edgecolor='black', linewidth=1.5)
            
            ax.set_title('Top 5 Equipment by Flowrate', fontweight='bold', fontsize=12)
            ax.set_xlabel('Flowrate', fontsize=11)
            ax.set_yticks(y_positions)
            ax.set_yticklabels(names, fontsize=10)
            ax.invert_yaxis()  # Highest at top
            ax.grid(True, axis='x', alpha=0.3)
            
        self.top5_figure.tight_layout()
        self.top5_canvas.draw()
    
    def download_report(self):
        """Download PDF report for current dataset"""
        if not self.current_dataset:
            QMessageBox.warning(self, "Warning", "No dataset selected")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            "Chemical Equipment Analysis Report.pdf",
            PDF_FILTER
        )
        
        if filename:
            self._save_pdf_report(filename)
    
    def _save_pdf_report(self, filename):
        """Save the PDF report to file"""
        try:
            print(f"Downloading report for dataset ID: {self.current_dataset['id']}")
            
            response = self.api_service.download_report(self.current_dataset['id'])
            
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {response.headers.get('content-type')}")
            
            if response.status_code == 200:
                # Ensure the file has .pdf extension
                if not filename.endswith('.pdf'):
                    filename += '.pdf'
                
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                print(f"PDF saved to: {filename}")
                QMessageBox.information(
                    self,
                    "Success",
                    f"Report downloaded successfully!\n\nSaved to:\n{filename}"
                )
            elif response.status_code == 401:
                QMessageBox.warning(self, "Error", "Session expired. Please login again.")
            elif response.status_code == 404:
                QMessageBox.warning(self, "Error", "Report not found. Dataset may have been deleted.")
            else:
                self._handle_download_error(response)
        except Exception as e:
            self._handle_exception(e)
    
    def _handle_download_error(self, response):
        """Handle download error responses"""
        error_msg = f"Failed to download report.\nStatus code: {response.status_code}"
        try:
            error_data = response.json()
            error_msg += f"\nError: {error_data.get('error', 'Unknown error')}"
        except:
            pass
        QMessageBox.warning(self, "Error", error_msg)
    
    def _handle_exception(self, e):
        """Handle exceptions during download"""
        import requests
        
        print(f"Exception: {type(e).__name__}: {str(e)}")
        
        if isinstance(e, requests.exceptions.Timeout):
            QMessageBox.critical(
                self,
                "Error",
                "Request timed out. The server may be slow or unavailable."
            )
        elif isinstance(e, requests.exceptions.ConnectionError):
            QMessageBox.critical(
                self,
                "Error",
                "Connection error. Please check if the backend server is running."
            )
        else:
            QMessageBox.critical(self, "Error", f"Error downloading report:\n{str(e)}")
