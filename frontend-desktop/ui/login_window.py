"""
Login Window - Authentication UI
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, 
    QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from services.api_service import APIService
from config import APP_NAME, APP_SUBTITLE


class LoginWindow(QWidget):
    """Login window for user authentication"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.api_service = APIService()
        self.main_window_ref = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components"""
        self.setWindowTitle(f"Login - {APP_NAME}")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(APP_NAME)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel(APP_SUBTITLE)
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self.handle_login)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        
        # Login button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)
        
        self.setLayout(layout)
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return
        
        try:
            response = self.api_service.login(username, password)
            
            if response.status_code == 200:
                token = response.json()['access']
                # Import here to avoid circular dependency
                from ui.main_window import MainWindow
                
                # Store main window reference to prevent garbage collection
                global _main_window
                from main import set_main_window
                self.main_window_ref = MainWindow(token)
                set_main_window(self.main_window_ref)
                self.main_window_ref.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Invalid credentials")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Connection error: {str(e)}")
