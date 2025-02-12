from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import WasteReport,WastePickup
from django.contrib import messages

# Create your views here.

def Home(request):
    if not request.user.is_authenticated:
        return render(request, "Users/userHome.html")


    if request.user.role == "administrator":
         return redirect("Admins:admin-dashboard")
    

    if request.user.role == "worker":
         return redirect("workers:worker-dashboard")
    
    return render(request, "Users/userHome.html")
    
    

@login_required(login_url='login')
def report_issue(request):
    if request.method == "POST":
        description = request.POST.get("description")
        location = request.POST.get("location")
        image = request.FILES.get("image")


        User = get_user_model()
        admin_user = User.objects.filter(role="administrator").first()  # Modify according to your user model

        if not admin_user:
            messages.error(request, "No admin available to assign.")
            return redirect("schedule-pickup")

        # Save report in the database
        WasteReport.objects.create(
            user=request.user,  # Logged-in user
            admin=admin_user,
            description=description,
            location=location,
            image=image
        )

        messages.success(request, "Waste issue reported successfully!")
        return redirect("report_issue")
    return render(request, "Users/report_issues.html")



@login_required(login_url='login')
def schedule_pickup(request):
    if request.method == "POST":
        date = request.POST.get("date")
        time = request.POST.get("time")
        location = request.POST.get("location")

        # Get an admin user (you can customize this logic)
        User = get_user_model()
        admin_user = User.objects.filter(role="administrator").first()  # Modify according to your user model

        if not admin_user:
            messages.error(request, "No admin available to assign.")
            return redirect("schedule_pickup")

        # Create a pickup request
        WastePickup.objects.create(
            user=request.user,
            admin=admin_user,  # Assign an admin
            date=date,
            time=time,
            location=location,
            status="scheduled"
        )

        messages.success(request, "Waste pickup scheduled successfully!")
        return redirect("schedule_pickup")
    return render(request, "Users/schedule_pickup.html")




@login_required(login_url='login')
def recycling_bins(request):
    return render(request, "Users/recycling_bins.html")


@login_required(login_url='login')
def userDashboard(request):
    user = request.user  # Get the logged-in user

    # Get all reported waste issues by the user
    reported_issues = WasteReport.objects.filter(user=user)

    # Get all scheduled pickups for the user
    pickup_history = WastePickup.objects.filter(user=user)

    return render(request, "Users/user_Dashboard.html", {
        "reported_issues": reported_issues,
        "pickup_history": pickup_history,
    })
