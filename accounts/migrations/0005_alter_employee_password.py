# Generated by Django 4.0 on 2025-01-21 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_employee_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
