from django.db import models
from django.contrib.auth.models import User
import json

class Dataset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')
    filename = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    data = models.TextField()  # Store JSON data
    
    # Summary statistics
    total_count = models.IntegerField(default=0)
    avg_flowrate = models.FloatField(default=0.0)
    avg_pressure = models.FloatField(default=0.0)
    avg_temperature = models.FloatField(default=0.0)
    equipment_types = models.TextField(default='{}')  # JSON string
    
    class Meta:
        ordering = ['-upload_date']
        
    def __str__(self):
        return f"{self.filename} - {self.upload_date.strftime('%Y-%m-%d %H:%M')}"
    
    def get_data(self):
        """Return data as Python object"""
        return json.loads(self.data)
    
    def set_data(self, data_list):
        """Set data from Python list"""
        self.data = json.dumps(data_list)
    
    def get_equipment_types(self):
        """Return equipment types distribution as dict"""
        return json.loads(self.equipment_types)
    
    def set_equipment_types(self, types_dict):
        """Set equipment types from dict"""
        self.equipment_types = json.dumps(types_dict)

class Equipment(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='equipment')
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"