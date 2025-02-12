from django.urls import path
from . import views

app_name = 'workers'

urlpatterns = [
    path('worker-dashboard/', views.worker_dashboard, name='worker-dashboard'),
    path('completed-tasks/', views.completed_tasks, name='completed-tasks'),

    path('report/<uuid:report_id>/', views.report_details, name='report-details'),  # Report Details
    path('pickup/<uuid:pickup_id>/', views.pickup_details, name='pickup-details'),  # Pickup Details

    path("update-status/<uuid:task_id>/<str:task_type>/", views.update_task_status, name="update_status"),
]
