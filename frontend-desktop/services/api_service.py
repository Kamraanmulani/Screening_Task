"""
API Service Layer - Handles all HTTP requests to the backend
"""
import requests
from config import API_URL, REQUEST_TIMEOUT


class APIService:
    """Handles all API communications with the backend"""
    
    def __init__(self, token=None):
        self.token = token
    
    def set_token(self, token):
        """Set authentication token"""
        self.token = token
    
    def get_headers(self):
        """Get authentication headers"""
        if self.token:
            return {'Authorization': f'Bearer {self.token}'}
        return {}
    
    # Authentication
    def login(self, username, password):
        """Login user and get access token"""
        response = requests.post(
            f"{API_URL}/token/",
            json={"username": username, "password": password}
        )
        return response
    
    # Datasets
    def get_datasets(self):
        """Get all datasets for the authenticated user"""
        response = requests.get(
            f"{API_URL}/datasets/",
            headers=self.get_headers()
        )
        return response
    
    def upload_dataset(self, file_path):
        """Upload a CSV file"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{API_URL}/datasets/",
                files=files,
                headers=self.get_headers()
            )
        return response
    
    def download_report(self, dataset_id):
        """Download PDF report for a dataset"""
        response = requests.get(
            f"{API_URL}/datasets/{dataset_id}/report/",
            headers=self.get_headers(),
            timeout=REQUEST_TIMEOUT
        )
        return response
