from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse
from django.db.models import Count
from .models import Dataset, Equipment
from .serializers import DatasetSerializer, DatasetSummarySerializer, EquipmentSerializer
import pandas as pd
import json
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from datetime import datetime

class DatasetViewSet(viewsets.ModelViewSet):
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return datasets for current user, ordered by upload date"""
        return Dataset.objects.filter(user=self.request.user).order_by('-upload_date')
    
    def list(self, request, *args, **kwargs):
        """List only last 5 datasets"""
        queryset = self.filter_queryset(self.get_queryset())[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle CSV upload"""
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        csv_file = request.FILES['file']
        
        # Validate file type
        if not csv_file.name.endswith('.csv'):
            return Response(
                {'error': 'File must be CSV format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Read CSV using pandas
            df = pd.read_csv(csv_file)
            
            # Validate required columns
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return Response(
                    {'error': f'Missing required columns: {", ".join(missing_columns)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Clean data - remove any rows with missing values
            df = df.dropna()
            
            # Convert to appropriate types
            df['Flowrate'] = pd.to_numeric(df['Flowrate'], errors='coerce')
            df['Pressure'] = pd.to_numeric(df['Pressure'], errors='coerce')
            df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce')
            df = df.dropna()  # Remove rows that couldn't be converted
            
            if len(df) == 0:
                return Response(
                    {'error': 'No valid data found in CSV'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Calculate statistics
            total_count = len(df)
            avg_flowrate = float(df['Flowrate'].mean())
            avg_pressure = float(df['Pressure'].mean())
            avg_temperature = float(df['Temperature'].mean())
            equipment_types = df['Type'].value_counts().to_dict()
            
            # Create dataset
            dataset = Dataset.objects.create(
                user=request.user,
                filename=csv_file.name,
                total_count=total_count,
                avg_flowrate=avg_flowrate,
                avg_pressure=avg_pressure,
                avg_temperature=avg_temperature
            )
            
            # Store data as JSON
            data_list = df.to_dict('records')
            dataset.set_data(data_list)
            dataset.set_equipment_types(equipment_types)
            dataset.save()
            
            # Create equipment entries
            equipment_objects = []
            for _, row in df.iterrows():
                equipment_objects.append(
                    Equipment(
                        dataset=dataset,
                        equipment_name=row['Equipment Name'],
                        equipment_type=row['Type'],
                        flowrate=float(row['Flowrate']),
                        pressure=float(row['Pressure']),
                        temperature=float(row['Temperature'])
                    )
                )
            Equipment.objects.bulk_create(equipment_objects)
            
            # Maintain only last 5 datasets
            user_datasets = Dataset.objects.filter(user=request.user).order_by('-upload_date')
            if user_datasets.count() > 5:
                datasets_to_delete = user_datasets[5:]
                for ds in datasets_to_delete:
                    ds.delete()
            
            serializer = self.get_serializer(dataset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Error processing CSV: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """Get summary statistics for a dataset"""
        dataset = self.get_object()
        serializer = DatasetSummarySerializer(dataset)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='report', url_name='report')
    def report(self, request, pk=None):
        """Generate PDF report for a dataset"""
        dataset = self.get_object()
        
        # Create PDF buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(
            f"<b>Chemical Equipment Analysis Report</b>",
            styles['Title']
        )
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Dataset Info
        info = Paragraph(
            f"<b>Dataset:</b> {dataset.filename}<br/>"
            f"<b>Upload Date:</b> {dataset.upload_date.strftime('%Y-%m-%d %H:%M')}<br/>"
            f"<b>Total Equipment:</b> {dataset.total_count}",
            styles['Normal']
        )
        elements.append(info)
        elements.append(Spacer(1, 12))
        
        # Summary Statistics
        summary_title = Paragraph("<b>Summary Statistics</b>", styles['Heading2'])
        elements.append(summary_title)
        elements.append(Spacer(1, 6))
        
        stats_data = [
            ['Metric', 'Average Value'],
            ['Flowrate', f"{dataset.avg_flowrate:.2f}"],
            ['Pressure', f"{dataset.avg_pressure:.2f}"],
            ['Temperature', f"{dataset.avg_temperature:.2f}"]
        ]
        
        stats_table = Table(stats_data, colWidths=[200, 200])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(stats_table)
        elements.append(Spacer(1, 12))
        
        # Equipment Type Distribution
        type_title = Paragraph("<b>Equipment Type Distribution</b>", styles['Heading2'])
        elements.append(type_title)
        elements.append(Spacer(1, 6))
        
        equipment_types = dataset.get_equipment_types()
        type_data = [['Equipment Type', 'Count']]
        for eq_type, count in equipment_types.items():
            type_data.append([eq_type, str(count)])
        
        type_table = Table(type_data, colWidths=[200, 200])
        type_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(type_table)
        
        # Build PDF
        doc.build(elements)
        
        # Return PDF
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{dataset.filename}_report.pdf"'
        return response

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """API health check endpoint"""
    return Response({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })