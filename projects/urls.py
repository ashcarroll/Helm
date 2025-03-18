from django.urls import path
from .views import ProjectListView, ProjectCreateView, ProjectDetailView, TaskCreateView, TaskUpdateView

urlpatterns = [
    path('list/', ProjectListView.as_view(), name='project_list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name ='project_detail'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:project_id>/tasks/create/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/update', TaskUpdateView.as_view(), name='task_update'),
]