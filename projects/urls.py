from django.urls import path
from .views import ProjectListView, ProjectCreateView, ProjectDetailView

urlpatterns = [
    path('list/', ProjectListView.as_view(), name='project_list'),
        path('<int:pk>/', ProjectDetailView.as_view(), name ='project_detail'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
]