"""
History Tab - Display upload history
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt5.QtGui import QFont
from config import HISTORY_HEADERS


class HistoryTab(QWidget):
    """Tab for displaying dataset history"""
    
    def __init__(self, api_service, on_view_dataset):
        super().__init__()
        self.api_service = api_service
        self.on_view_dataset = on_view_dataset
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout()
        
        label = QLabel("Upload History (Last 5)")
        label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(label)
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(HISTORY_HEADERS)
        self.history_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.history_table)
        
        self.setLayout(layout)
    
    def load_datasets(self):
        """Load and display datasets"""
        try:
            response = self.api_service.get_datasets()
            
            if response.status_code == 200:
                datasets = response.json()
                self.update_table(datasets)
                return datasets
            else:
                QMessageBox.warning(self, "Error", "Failed to load datasets")
                return []
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading datasets: {str(e)}")
            return []
    
    def update_table(self, datasets):
        """Update the history table with datasets"""
        self.history_table.setRowCount(len(datasets))
        
        for i, dataset in enumerate(datasets):
            self.history_table.setItem(i, 0, QTableWidgetItem(dataset['filename']))
            self.history_table.setItem(i, 1, QTableWidgetItem(dataset['upload_date']))
            self.history_table.setItem(i, 2, QTableWidgetItem(str(dataset['total_count'])))
            
            view_btn = QPushButton("View")
            view_btn.clicked.connect(lambda checked, d=dataset: self._handle_view(d))
            self.history_table.setCellWidget(i, 3, view_btn)
    
    def _handle_view(self, dataset):
        """Handle view button click"""
        self.on_view_dataset(dataset)
