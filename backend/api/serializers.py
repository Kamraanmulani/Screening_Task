from rest_framework import serializers
from .models import Dataset, Equipment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']

class DatasetSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(many=True, read_only=True)
    equipment_types_dict = serializers.SerializerMethodField()
    data_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'filename', 'upload_date', 'total_count',
            'avg_flowrate', 'avg_pressure', 'avg_temperature',
            'equipment_types_dict', 'equipment', 'data_list'
        ]
    
    def get_equipment_types_dict(self, obj):
        return obj.get_equipment_types()
    
    def get_data_list(self, obj):
        return obj.get_data()

class DatasetSummarySerializer(serializers.ModelSerializer):
    equipment_types_dict = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'filename', 'upload_date', 'total_count',
            'avg_flowrate', 'avg_pressure', 'avg_temperature',
            'equipment_types_dict'
        ]
    
    def get_equipment_types_dict(self, obj):
        return obj.get_equipment_types()