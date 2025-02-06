from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Work
from django.contrib.auth import logout
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone

def home(request):
    return render(request, 'accounts/home.html')

def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if email == 'admin@example.com' and password == 'admin123':
            return redirect('admin_dashboard')
        else:
            return render(request, 'accounts/admin_login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/admin_login.html')

def admin_dashboard(request):
    employees = Employee.objects.all()
    unassigned_works = Work.objects.filter(assigned=False)  # Fetch unassigned work

    return render(request, 'accounts/admin_dashboard.html', {
        'employees': employees,
        'unassigned_works': unassigned_works
    })

def add_employee(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        salary = request.POST['salary']
        category = request.POST['category']
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        Employee.objects.create(
            name=name, email=email, password=password, salary=salary,
            category=category, phone_number=phone_number, address=address
        )
        return redirect('admin_dashboard')
    return render(request, 'accounts/add_employee.html')

def employee_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            employee = Employee.objects.get(email=email, password=password)
            return redirect('employee_dashboard', employee_id=employee.id)
        except Employee.DoesNotExist:
            return render(request, 'accounts/employee_login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/employee_login.html')

def employee_dashboard(request, employee_id):
    employee = Employee.objects.get(id=employee_id)

    # Handle notifications for assigned work
    if employee.work_assigned and not employee.notification_seen:
        messages.info(request, 'New work has been assigned to you by the admin.')
        employee.notification_seen = True  # Mark notification as seen
        employee.save()

    return render(request, 'accounts/employee_dashboard.html', {'employee': employee})

def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        employee.name = request.POST['name']
        employee.email = request.POST['email']
        employee.password = request.POST['password']
        employee.salary = request.POST['salary']
        employee.category = request.POST['category']
        employee.phone_number = request.POST['phone_number']
        employee.address = request.POST['address']
        employee.work_assigned = 'work_assigned' in request.POST
        employee.save()
        return redirect('admin_dashboard')
    return render(request, 'accounts/edit_employee.html', {'employee': employee})


def assign_work(request, employee_id):
    # Fetch the employee based on the provided employee_id
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == 'POST':
        # Get the work description and file from the form
        work_description = request.POST['work_description']
        work_file = request.FILES.get('work_file')

        # Set the work_assigned flag to False when assigning new work
        employee.work_assigned = False
        employee.save()

        # Create a new Work object
        work = Work.objects.create(
            description=work_description,
            assigned=True,
            assigned_to=employee,
        )

        # Handle file upload if provided
        if work_file:
            fs = FileSystemStorage()
            filename = fs.save(work_file.name, work_file)
            work.file = fs.url(filename)

        work.save()

        # Update the employee's work description
        employee.work_description = work_description
        employee.notification_seen = False
        employee.save()

        # Display a success message
        messages.info(request, 'New work has been assigned to the employee.')

        # Redirect to the admin dashboard
        return redirect('admin_dashboard')

    # If the request method is GET, render the assign work page with the employee details
    return render(request, 'accounts/assign_work.html', {'employee': employee})

def work_details(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    work_details = Work.objects.filter(assigned_to=employee, assigned=True)

    return render(request, 'accounts/work_details.html', {
        'employee': employee,
        'work_details': work_details
    })

def update_employee_work_status(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == 'POST':
        # Process the form data
        work_assigned = request.POST.get('work_assigned') == 'True'
        work_description = request.POST.get('work_description')
        work_file = request.FILES.get('work_file')

        # Update the employee's work status and description
        employee.work_assigned = work_assigned
        employee.work_description = work_description

        if work_file:
            # Save the file if provided
            employee.work_file = work_file

        employee.save()

        # Add success message to be displayed on the page
        messages.success(request, 'Work status updated successfully!')

        return redirect('employee_dashboard', employee_id=employee.id)

    return render(request, 'employee_dashboard.html', {'employee': employee})
def update_employee_work(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    if request.method == 'POST':
        # Get the value of 'work_assigned' from the form
        work_assigned = request.POST.get('work_assigned')

        if work_assigned == 'True':
            employee.work_assigned = True
        else:
            employee.work_assigned = False

        # Optionally, update other fields like 'work_description' and 'work_file'
        employee.work_description = request.POST.get('work_description')
        if request.FILES.get('work_file'):
            employee.work_file = request.FILES['work_file']

        # Save the updated employee information
        employee.save()

        # Display success message to the employee
        messages.success(request, 'Work status updated successfully!')
        return redirect('admin_dashboard')  # Redirect to the admin dashboard or another view

    return render(request, 'admin_dashboard.html', {'employee': employee})

    return render(request, 'employee_dashboard.html', {'employee': employee})


def delete_work(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.work_assigned = False
    employee.work_description = ""
    employee.work_file = ""
    employee.notification_seen = False  # Reset notification
    employee.save()

    # Reset the assignment in Work model
    if employee.work_file:
        work = Work.objects.get(employee=employee)
        work.assigned = False
        work.employee = None
        work.save()

    return redirect('admin_dashboard')

def delete_work(request, employee_id, work_id):
    # Fetch the employee and work based on the IDs
    employee = get_object_or_404(Employee, id=employee_id)
    work = get_object_or_404(Work, id=work_id, assigned_to=employee)

    # Delete the work
    work.delete()

    # Reset the employee's work description
    employee.work_assigned = False
    employee.work_description = ""
    employee.save()

    # Display success message
    messages.success(request, 'Work has been deleted successfully.')

    return redirect('work_details', employee_id=employee.id)  # Redirect to work details page



def edit_work(request, employee_id, work_id):
    # Fetch the work object and employee based on provided IDs
    work = get_object_or_404(Work, id=work_id, assigned_to__id=employee_id)

    if request.method == 'POST':
        # Get the updated work description and file from the form
        work_description = request.POST.get('work_description')
        work_file = request.FILES.get('work_file')

        # Update work details
        work.description = work_description
        work.assigned_date = timezone.now()  # Set the assigned date to the current time

        if work_file:
            # Handle file upload if provided
            work.file = work_file

        work.save()

        # Add a success message
        messages.success(request, 'Work details updated successfully!')

        return redirect('work_details', employee_id=employee_id)  # Redirect to the work details page

    return render(request, 'accounts/edit_work.html', {
        'work': work,
        'employee': work.assigned_to,
    })
    # Fetch the work object and employee based on provided IDs
    work = get_object_or_404(Work, id=work_id, assigned_to__id=employee_id)

    if request.method == 'POST':
        # Get the updated work description and file from the form
        work_description = request.POST.get('work_description')
        work_file = request.FILES.get('work_file')

        # Update work details
        work.description = work_description

        if work_file:
            # Handle file upload if provided
            work.file = work_file

        work.save()

        # Add a success message
        messages.success(request, 'Work details updated successfully!')

        return redirect('work_details', employee_id=employee_id)  # Redirect to the work details page

    return render(request, 'accounts/edit_work.html', {
        'work': work,
        'employee': work.assigned_to,
    })


def update_work_status(request, employee_id):
    employee = Employee.objects.get(id=employee_id)

    if request.method == 'POST':
        work_assigned = request.POST.get('work_assigned') == 'True'
        work_description = request.POST.get('work_description')
        work_file = request.FILES.get('work_file')

        # Update employee's work status
        employee.work_assigned = work_assigned
        employee.work_description = work_description

        # If a work file is uploaded, handle file saving
        if work_file:
            employee.work_file = work_file

        # Save the changes
        employee.save()

        # Optionally, you can show a success message
        messages.success(request, 'Work status updated successfully.')

        return redirect('employee_dashboard')  # Redirect to employee dashboard

    return render(request, 'employee_dashboard.html', {'employee': employee})


def logout_view(request):
    logout(request)
    return redirect('home')
