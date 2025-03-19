from django.urls import path
from .views import TeamListView, TeamDetailView, TeamCreateView, TeamUpdateView

urlpatterns = [
    path('list/', TeamListView.as_view(), name='team_list'),
    path('<int:pk>/', TeamDetailView.as_view(), name ='team_detail'),
    path('create/', TeamCreateView.as_view(), name='team_create'),
    path('<int:pk>/update/', TeamUpdateView.as_view(), name = 'team_update'),
]