from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from Users.models import WastePickup, WasteReport  # Import models
from django.contrib import messages


@login_required
def worker_dashboard(request):
    worker = request.user  # Get the logged-in worker

    # Fetch assigned reports and pickups
    assigned_reports = WasteReport.objects.filter(assigned_worker=worker)
    assigned_pickups = WastePickup.objects.filter(worker=worker)  # Correct field name

    context = {
        "assigned_reports": assigned_reports,
        "assigned_pickups": assigned_pickups,
    }
    return render(request, 'Workers/worker-dashboard.html', context)


@login_required
def completed_tasks(request):
    worker = request.user  # Get the logged-in worker

    # Fetch completed reports and pickups
    completed_reports = WasteReport.objects.filter(assigned_worker=worker, status="resolved")
    completed_pickups = WastePickup.objects.filter(worker=worker, status="completed")

    context = {
        "completed_reports": completed_reports,
        "completed_pickups": completed_pickups,
    }
    return render(request, 'Workers/completed-task.html', context)



@login_required
def report_details(request, report_id):
    report = get_object_or_404(WasteReport, id=report_id)
    return render(request, 'Workers/details.html', {'task': report, 'task_type': 'report'})


@login_required
def pickup_details(request, pickup_id):
    pickup = get_object_or_404(WastePickup, id=pickup_id)
    return render(request, 'Workers/details.html', {'task': pickup, 'task_type': 'pickup'})



 # Ensure correct imports

@login_required
def update_task_status(request, task_id, task_type):
    if request.method == "POST":
        new_status = request.POST.get("status")
        
        if task_type == "report":
            task = get_object_or_404(WasteReport, id=task_id)
        elif task_type == "pickup":
            task = get_object_or_404(WastePickup, id=task_id)
        else:
            messages.error(request, "Invalid task type.")
            return redirect("workers:worker-dashboard")

        # Update the task status
        task.status = new_status
        task.save()

        messages.success(request, f"Task status updated to {new_status.capitalize()}.")
        return redirect("workers:worker-dashboard")

    else:
        messages.error(request, "Invalid request.")
        return redirect("workers:worker-dashboard")