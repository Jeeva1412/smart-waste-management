from django.urls import path
from . import views


app_name = 'Admins' 

urlpatterns = [
    path('admin-dashboard', views.admin_dashboard, name='admin-dashboard'),
    path('manage-report/', views.manage_report, name='manage-report'),


    path('view-pickups/', views.view_pickups, name='view-pickups'),
    path('assign-worker/<uuid:pickup_id>/', views.assign_worker, name="assign_worker"),


    path('create-worker/', views.create_worker, name='create-worker'),


    path("update-report/<uuid:report_id>/", views.update_waste_report, name="update_report"),
    path("view-details/<uuid:report_id>/", views.view_details, name="view-details"),
]
