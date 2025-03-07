# Generated by Django 4.0 on 2025-01-21 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_employee_notification_seen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='points',
        ),
        migrations.AddField(
            model_name='employee',
            name='work_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='notification_seen',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='employee',
            name='password',
            field=models.CharField(default='123', max_length=100),
        ),
        migrations.AlterField(
            model_name='employee',
            name='work_file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
