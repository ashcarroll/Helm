from django.urls import path
from .views import ProjectListView, ProjectCreateView, ProjectDetailView, TaskCreateView

urlpatterns = [
    path('list/', ProjectListView.as_view(), name='project_list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name ='project_detail'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:project_id>/tasks/create/', TaskCreateView.as_view(), name='task_create'),
]