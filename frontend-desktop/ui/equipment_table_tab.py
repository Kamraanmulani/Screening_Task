"""
Equipment Table Tab - Display equipment data in table format
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, 
    QTableWidgetItem, QLabel
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from config import EQUIPMENT_HEADERS


class EquipmentTableTab(QWidget):
    """Tab for displaying equipment data in table format"""
    
    def __init__(self):
        super().__init__()
        self.current_dataset = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components"""
        self.layout = QVBoxLayout()
        
        # Dataset info
        self.dataset_info_label = QLabel("No dataset loaded")
        self.dataset_info_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.layout.addWidget(self.dataset_info_label)
        
        # Equipment table
        self.equipment_table = QTableWidget()
        self.equipment_table.setMinimumHeight(400)
        self.layout.addWidget(self.equipment_table)
        
        self.setLayout(self.layout)
    
    def update_table(self, dataset):
        """Update table with dataset information"""
        if not dataset:
            return
        
        self.current_dataset = dataset
        
        # Update dataset info
        self.dataset_info_label.setText(
            f"Dataset: {dataset['filename']} | "
            f"Uploaded: {dataset['upload_date']} | "
            f"Total Equipment: {dataset['total_count']}"
        )
        
        # Update table
        self._update_equipment_table(dataset)
    
    def _update_equipment_table(self, dataset):
        """Update the equipment table"""
        equipment = dataset.get('equipment', [])
        self.equipment_table.setRowCount(len(equipment))
        self.equipment_table.setColumnCount(5)
        self.equipment_table.setHorizontalHeaderLabels(EQUIPMENT_HEADERS)
        
        # Style the table for better visibility
        self.equipment_table.setAlternatingRowColors(True)
        self.equipment_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #d0d0d0;
                font-size: 12pt;
                border: 2px solid #cccccc;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e0e0e0;
            }
            QTableWidget::item:selected {
                background-color: #000000;
                color: white;
            }
            QHeaderView::section {
                background-color: #000000;
                color: white;
                padding: 10px;
                border: 1px solid #666666;
                font-size: 13pt;
                font-weight: bold;
            }
            QTableWidget::item:alternate {
                background-color: #f5f5f5;
            }
        """)
        
        # Set minimum row height for better readability
        self.equipment_table.verticalHeader().setDefaultSectionSize(40)
        
        for i, eq in enumerate(equipment):
            # Create read-only items
            item_name = QTableWidgetItem(eq['equipment_name'])
            item_name.setFlags(item_name.flags() & ~Qt.ItemIsEditable)
            
            item_type = QTableWidgetItem(eq['equipment_type'])
            item_type.setFlags(item_type.flags() & ~Qt.ItemIsEditable)
            
            item_flowrate = QTableWidgetItem(f"{eq['flowrate']:.2f}")
            item_flowrate.setFlags(item_flowrate.flags() & ~Qt.ItemIsEditable)
            
            item_pressure = QTableWidgetItem(f"{eq['pressure']:.2f}")
            item_pressure.setFlags(item_pressure.flags() & ~Qt.ItemIsEditable)
            
            item_temperature = QTableWidgetItem(f"{eq['temperature']:.2f}")
            item_temperature.setFlags(item_temperature.flags() & ~Qt.ItemIsEditable)
            
            self.equipment_table.setItem(i, 0, item_name)
            self.equipment_table.setItem(i, 1, item_type)
            self.equipment_table.setItem(i, 2, item_flowrate)
            self.equipment_table.setItem(i, 3, item_pressure)
            self.equipment_table.setItem(i, 4, item_temperature)
        
        self.equipment_table.resizeColumnsToContents()
        self.equipment_table.horizontalHeader().setStretchLastSection(True)
