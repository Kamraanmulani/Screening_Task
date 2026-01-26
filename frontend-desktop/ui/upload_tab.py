"""
Upload Tab - File upload interface
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QGroupBox, QFileDialog, QMessageBox
)
from config import CSV_FILTER


class UploadTab(QWidget):
    """Tab for uploading CSV files"""
    
    def __init__(self, api_service, on_upload_success):
        super().__init__()
        self.api_service = api_service
        self.on_upload_success = on_upload_success
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout()
        
        # Upload section
        upload_group = QGroupBox("Upload CSV File")
        upload_layout = QVBoxLayout()
        
        info_label = QLabel("CSV should contain: Equipment Name, Type, Flowrate, Pressure, Temperature")
        upload_layout.addWidget(info_label)
        
        upload_btn = QPushButton("Choose CSV File")
        upload_btn.clicked.connect(self.upload_file)
        upload_layout.addWidget(upload_btn)
        
        upload_group.setLayout(upload_layout)
        layout.addWidget(upload_group)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def upload_file(self):
        """Handle file upload"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", CSV_FILTER
        )
        
        if filename:
            try:
                response = self.api_service.upload_dataset(filename)
                
                if response.status_code == 201:
                    dataset = response.json()
                    self.on_upload_success(dataset)
                    QMessageBox.information(self, "Success", "File uploaded successfully!")
                else:
                    error_msg = response.json().get('error', 'Unknown error')
                    QMessageBox.warning(self, "Error", f"Upload failed: {error_msg}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error uploading file: {str(e)}")
