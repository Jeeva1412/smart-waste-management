from django.urls import path
from . import views  # Import views from Users app

urlpatterns = [
    path('',views.Home,name="home"),
    path("report_issue/", views.report_issue, name="report_issue"),
    path("schedule-pickup/", views.schedule_pickup, name="schedule_pickup"),
    path("recycling-bins/", views.recycling_bins, name="recycling_bins"),
    path("user-dashboard/", views.userDashboard, name="user-dashboard"),
]
