# Generated by Django 5.0.4 on 2024-04-30 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medical_services', '0002_rename_description_category_category_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='category_image',
            new_name='services_image',
        ),
    ]