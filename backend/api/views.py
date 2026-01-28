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
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from datetime import datetime
import statistics

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
        """Generate comprehensive PDF report for a dataset"""
        dataset = self.get_object()
        equipment_list = list(dataset.equipment.all())
        
        # Create PDF buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=0.75*inch
        )
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        # Title
        title = Paragraph("Chemical Equipment Analysis Report", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Dataset Info Section
        info_data = [
            ['Dataset Information', ''],
            ['Filename:', dataset.filename],
            ['Upload Date:', dataset.upload_date.strftime('%B %d, %Y at %H:%M')],
            ['Total Equipment:', str(dataset.total_count)],
            ['Generated:', datetime.now().strftime('%B %d, %Y at %H:%M')]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4.5*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Summary Statistics Section
        summary_title = Paragraph("Summary Statistics", heading_style)
        elements.append(summary_title)
        
        # Calculate extended statistics
        flowrates = [eq.flowrate for eq in equipment_list]
        pressures = [eq.pressure for eq in equipment_list]
        temperatures = [eq.temperature for eq in equipment_list]
        
        stats_data = [
            ['Parameter', 'Average', 'Minimum', 'Maximum', 'Std Dev', 'Range'],
            [
                'Flowrate',
                f"{dataset.avg_flowrate:.2f}",
                f"{min(flowrates):.2f}",
                f"{max(flowrates):.2f}",
                f"{statistics.stdev(flowrates) if len(flowrates) > 1 else 0:.2f}",
                f"{max(flowrates) - min(flowrates):.2f}"
            ],
            [
                'Pressure',
                f"{dataset.avg_pressure:.2f}",
                f"{min(pressures):.2f}",
                f"{max(pressures):.2f}",
                f"{statistics.stdev(pressures) if len(pressures) > 1 else 0:.2f}",
                f"{max(pressures) - min(pressures):.2f}"
            ],
            [
                'Temperature',
                f"{dataset.avg_temperature:.2f}",
                f"{min(temperatures):.2f}",
                f"{max(temperatures):.2f}",
                f"{statistics.stdev(temperatures) if len(temperatures) > 1 else 0:.2f}",
                f"{max(temperatures) - min(temperatures):.2f}"
            ]
        ]
        
        stats_table = Table(stats_data, colWidths=[1.3*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#eaf2f8')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ]))
        elements.append(stats_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Equipment Type Distribution Section
        type_title = Paragraph("Equipment Type Distribution", heading_style)
        elements.append(type_title)
        
        equipment_types = dataset.get_equipment_types()
        total = sum(equipment_types.values())
        type_data = [['Equipment Type', 'Count', 'Percentage']]
        for eq_type, count in sorted(equipment_types.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100) if total > 0 else 0
            type_data.append([eq_type, str(count), f"{percentage:.1f}%"])
        
        type_table = Table(type_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        type_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fadbd8')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fcf3f2')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(type_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Top 5 Equipment by Flowrate Section
        top_title = Paragraph("Top 5 Equipment by Flowrate", heading_style)
        elements.append(top_title)
        
        sorted_equipment = sorted(equipment_list, key=lambda x: x.flowrate, reverse=True)[:5]
        top_data = [['Rank', 'Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
        for idx, eq in enumerate(sorted_equipment, 1):
            top_data.append([
                str(idx),
                eq.equipment_name,
                eq.equipment_type,
                f"{eq.flowrate:.2f}",
                f"{eq.pressure:.2f}",
                f"{eq.temperature:.2f}"
            ])
        
        top_table = Table(top_data, colWidths=[0.5*inch, 1.8*inch, 1.3*inch, 1*inch, 1*inch, 1.2*inch])
        top_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e8daef')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f4ecf7')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ]))
        elements.append(top_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Footer note
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        footer = Paragraph(
            f"Report generated on {datetime.now().strftime('%B %d, %Y at %H:%M')} | "
            f"Chemical Equipment Visualizer - IIT Bombay Screening Task",
            footer_style
        )
        elements.append(footer)
        
        # Build PDF
        doc.build(elements)
        
        # Return PDF
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Chemical Equipment Analysis Report.pdf"'
        return response
        
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