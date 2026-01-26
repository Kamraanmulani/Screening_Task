"""
Main Window - Application main interface
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTabWidget, QMessageBox
)
from PyQt5.QtGui import QFont
from services.api_service import APIService
from ui.upload_tab import UploadTab
from ui.dashboard_tab import DashboardTab
from ui.history_tab import HistoryTab
from config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, token):
        super().__init__()
        self.api_service = APIService(token)
        self.current_dataset = None
        self.init_ui()
        self.load_initial_data()
    
    def init_ui(self):
        """Initialize the UI components"""
        self.setWindowTitle(f"{APP_NAME} - Desktop App")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout()
        
        # Header
        header_layout = self._create_header()
        main_layout.addLayout(header_layout)
        
        # Create tabs
        self.tabs = QTabWidget()
        self._create_tabs()
        main_layout.addWidget(self.tabs)
        
        central_widget.setLayout(main_layout)
    
    def _create_header(self):
        """Create the header with title and logout button"""
        header_layout = QHBoxLayout()
        
        title = QLabel(APP_NAME)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        header_layout.addWidget(title)
        
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.logout)
        header_layout.addWidget(logout_btn)
        header_layout.addStretch()
        
        return header_layout
    
    def _create_tabs(self):
        """Create and setup all tabs"""
        # Upload tab
        self.upload_tab = UploadTab(
            self.api_service,
            self.handle_upload_success
        )
        self.tabs.addTab(self.upload_tab, "Upload")
        
        # Dashboard tab
        self.dashboard_tab = DashboardTab(self.api_service)
        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        
        # History tab
        self.history_tab = HistoryTab(
            self.api_service,
            self.handle_view_dataset
        )
        self.tabs.addTab(self.history_tab, "History")
    
    def load_initial_data(self):
        """Load initial datasets on startup"""
        datasets = self.history_tab.load_datasets()
        if datasets and not self.current_dataset:
            self.current_dataset = datasets[0]
            self.dashboard_tab.update_dashboard(self.current_dataset)
    
    def handle_upload_success(self, dataset):
        """Handle successful file upload"""
        self.current_dataset = dataset
        self.dashboard_tab.update_dashboard(dataset)
        self.history_tab.load_datasets()
        self.tabs.setCurrentIndex(1)  # Switch to dashboard tab
    
    def handle_view_dataset(self, dataset):
        """Handle viewing a dataset from history"""
        self.current_dataset = dataset
        self.dashboard_tab.update_dashboard(dataset)
        self.tabs.setCurrentIndex(1)  # Switch to dashboard tab
    
    def logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self,
            'Logout',
            'Are you sure you want to logout?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.close()
            # Re-show login window
            from ui.login_window import LoginWindow
            from main import set_login_window
            
            login = LoginWindow()
            login.main_window_ref = None
            login.show()
            set_login_window(login)
