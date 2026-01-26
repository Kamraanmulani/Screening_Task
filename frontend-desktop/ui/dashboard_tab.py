"""
Dashboard Tab - Data visualization interface
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QTableWidget, QTableWidgetItem, QGroupBox,
    QFormLayout, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QFont
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
        
        # Table
        self.equipment_table = QTableWidget()
        self.layout.addWidget(self.equipment_table)
        
        self.setLayout(self.layout)
    
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
        
        # Update table
        self._update_equipment_table(dataset)
    
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
    
    def _update_equipment_table(self, dataset):
        """Update the equipment table"""
        equipment = dataset.get('equipment', [])
        self.equipment_table.setRowCount(len(equipment))
        self.equipment_table.setColumnCount(5)
        self.equipment_table.setHorizontalHeaderLabels(EQUIPMENT_HEADERS)
        
        for i, eq in enumerate(equipment):
            self.equipment_table.setItem(i, 0, QTableWidgetItem(eq['equipment_name']))
            self.equipment_table.setItem(i, 1, QTableWidgetItem(eq['equipment_type']))
            self.equipment_table.setItem(i, 2, QTableWidgetItem(f"{eq['flowrate']:.2f}"))
            self.equipment_table.setItem(i, 3, QTableWidgetItem(f"{eq['pressure']:.2f}"))
            self.equipment_table.setItem(i, 4, QTableWidgetItem(f"{eq['temperature']:.2f}"))
        
        self.equipment_table.resizeColumnsToContents()
    
    def download_report(self):
        """Download PDF report for current dataset"""
        if not self.current_dataset:
            QMessageBox.warning(self, "Warning", "No dataset selected")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            f"equipment_report_{self.current_dataset['id']}.pdf",
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
