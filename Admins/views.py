from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.contrib.auth import login
from .forms import WorkerRegistrationForm
from Users.models import CustomUser,User,WastePickup,WasteReport
from django.contrib.auth import get_user_model
from Users.models import WasteReport, WastePickup


CustomUser = get_user_model()


def is_admin(user):
    return user.is_authenticated and user.role == "administrator"
@login_required
def admin_dashboard(request):
    # Check if models exist in the database
    total_reports = WasteReport.objects.count() if WasteReport.objects.exists() else 0
    resolved_reports = WasteReport.objects.filter(status="resolved").count() if WasteReport.objects.exists() else 0
    pending_reports = WasteReport.objects.filter(status="pending").count() if WasteReport.objects.exists() else 0
    assigned_reports = WasteReport.objects.filter(status="assigned").count() if WasteReport.objects.exists() else 0

    total_pickups = WastePickup.objects.count() if WastePickup.objects.exists() else 0
    completed_pickups = WastePickup.objects.filter(status="completed").count() if WastePickup.objects.exists() else 0
    pending_pickups = WastePickup.objects.filter(status="scheduled").count() if WastePickup.objects.exists() else 0
    assigned_pickups = WastePickup.objects.filter(status="assigned").count() if WastePickup.objects.exists() else 0

    # Get recent activities safely
    recent_reports = WasteReport.objects.order_by('-created_at')[:3] if WasteReport.objects.exists() else []
    recent_pickups = WastePickup.objects.order_by('-date', '-time')[:3] if WastePickup.objects.exists() else []

    context = {
        "total_reports": total_reports,
        "resolved_reports": resolved_reports,
        "pending_reports": pending_reports,
        "assigned_reports": assigned_reports,
        "total_pickups": total_pickups,
        "completed_pickups": completed_pickups,
        "pending_pickups": pending_pickups,
        "assigned_pickups": assigned_pickups,
        "recent_reports": recent_reports,
        "recent_pickups": recent_pickups,
    }

    return render(request, "Admins/adminDashboard.html", context)




@login_required
def manage_report(request):
     # Get all waste reports
    reports = WasteReport.objects.all()
    context={
        "reports":reports
    }
    return render(request, 'Admins/manage-reports.html',context)



@login_required
def create_worker(request):
    if request.method == "POST":
        form = WorkerRegistrationForm(request.POST)
        if form.is_valid():
            worker = form.save(commit=False)
            worker.role = 'worker'  # Ensuring the role is always 'worker'
            worker.save()
            messages.success(request, "Worker created successfully!")  # Success message
            return redirect('Admins:create-worker')  # Redirect to clear form
        else:
            messages.error(request, "Failed to create worker. Please correct the errors below.")  # Error message
    else:
        form = WorkerRegistrationForm()

    workers = CustomUser.objects.filter(role='worker')  # Fetch all workers
    
    return render(request, 'Admins/create-worker.html', {'form': form, 'workers': workers})





# Check if user is an admin


@login_required
@user_passes_test(is_admin)
def update_waste_report(request, report_id):
    report = get_object_or_404(WasteReport, id=report_id)
    workers = CustomUser.objects.filter(role="worker")

    if request.method == "POST":
        worker_id = request.POST.get("assigned_worker")
        
        if worker_id:
            assigned_worker = CustomUser.objects.get(id=worker_id)
            report.assigned_worker = assigned_worker
            report.status = "assigned"
            report.save()
            messages.success(request, "Worker assigned successfully!")
            return redirect("Admins:manage-report")

    return render(request, "Admins/update_report.html", {"report": report, "workers": workers})


def view_details(request,report_id):
    report = get_object_or_404(WasteReport, id=report_id)
    context={
        "report":report
    }
    return render(request,"Admins/view-details.html",context)



@login_required
def view_pickups(request):
    return render(request, 'Admins/view-pickup.html')



# Get the CustomUser model


@login_required
@user_passes_test(is_admin)
def view_pickups(request):
    pickups = WastePickup.objects.all()
    workers = CustomUser.objects.filter(role="worker")

    return render(request, "Admins/view-pickup.html", {"pickups": pickups, "workers": workers})




@login_required
@user_passes_test(is_admin)
def assign_worker(request, pickup_id):
    pickup = get_object_or_404(WastePickup, id=pickup_id)  # Ensure pickup ID is an integer

    if request.method == "POST":
        worker_id = request.POST.get("assigned_worker")

        # Debugging: Check if worker_id is received correctly
        print(f"Received worker ID: {worker_id}")

        if worker_id and worker_id.isdigit():  # Ensure it's a valid integer
            assigned_worker = get_object_or_404(CustomUser, id=worker_id)  # Convert to integer
            print(f"Assigning Worker: {assigned_worker.username}")

            pickup.worker = assigned_worker
            pickup.status = "assigned"
            pickup.save()

            messages.success(request, "Worker assigned successfully!")
            return redirect("Admins:view-pickups")

    messages.error(request, "Failed to assign worker. Please try again.")
    return redirect("Admins:view-pickups")
