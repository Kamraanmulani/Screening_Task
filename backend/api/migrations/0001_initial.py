# Generated migration

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=255)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('data', models.TextField()),
                ('total_count', models.IntegerField(default=0)),
                ('avg_flowrate', models.FloatField(default=0.0)),
                ('avg_pressure', models.FloatField(default=0.0)),
                ('avg_temperature', models.FloatField(default=0.0)),
                ('equipment_types', models.TextField(default='{}')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datasets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-upload_date'],
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment_name', models.CharField(max_length=255)),
                ('equipment_type', models.CharField(max_length=100)),
                ('flowrate', models.FloatField()),
                ('pressure', models.FloatField()),
                ('temperature', models.FloatField()),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipment', to='api.dataset')),
            ],
        ),
    ]
