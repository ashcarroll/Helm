from django.urls import path
from .views import dashboard_view, project_status_data, task_completion_data

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('api/project-status-data/', project_status_data, name='project_status_data'),
    path('api/task-completion-data/', task_completion_data, name='task_completion_data'), 
]