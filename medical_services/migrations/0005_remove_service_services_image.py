# Generated by Django 5.0.4 on 2024-05-01 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medical_services', '0004_alter_service_deadline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='services_image',
        ),
    ]