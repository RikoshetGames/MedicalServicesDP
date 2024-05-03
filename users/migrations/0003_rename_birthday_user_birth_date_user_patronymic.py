# Generated by Django 5.0.4 on 2024-04-30 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_country_user_birthday_user_verify_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='birthday',
            new_name='birth_date',
        ),
        migrations.AddField(
            model_name='user',
            name='patronymic',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Отчество'),
        ),
    ]