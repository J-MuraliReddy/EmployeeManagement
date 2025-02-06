"""EmployeeManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('employee-login/', views.employee_login, name='employee_login'),
    path('employee-dashboard/<int:employee_id>/', views.employee_dashboard, name='employee_dashboard'),
    path('edit-employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('assign-work/<int:employee_id>/', views.assign_work, name='assign_work'),
    path('logout/', views.logout_view, name='logout'),
    path('delete-work/<int:employee_id>/', views.delete_work, name='delete_work'),
    path('update_employee_work/<int:employee_id>/', views.update_employee_work, name='update_employee_work'),
    path('update_work_status/<int:employee_id>/', views.update_work_status, name='update_work_status'),
    path('work-details/<int:employee_id>/', views.work_details, name='work_details'),
    path('employee/<int:employee_id>/update_work_status/', views.update_employee_work_status, name='update_employee_work_status'),
    path('employee/update_work_status/<int:employee_id>/', views.update_employee_work_status, name='update_employee_work_status'),
    path('edit-work/<int:employee_id>/<int:work_id>/', views.edit_work, name='edit_work'),
    path('delete-work/<int:employee_id>/<int:work_id>/', views.delete_work, name='delete_work'),
    
]
