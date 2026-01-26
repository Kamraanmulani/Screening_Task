"""
Chemical Equipment Visualizer - Desktop Application
Main entry point for the PyQt5 application
"""
import sys
from PyQt5.QtWidgets import QApplication
from ui.login_window import LoginWindow

# Global references to prevent garbage collection
_login_window = None
_main_window = None


def set_login_window(window):
    """Set the global login window reference"""
    global _login_window
    _login_window = window


def set_main_window(window):
    """Set the global main window reference"""
    global _main_window
    _main_window = window


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Create and show login window
    global _login_window
    _login_window = LoginWindow()
    _login_window.show()
    
    # Start application event loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
