from django import path
from .views import TeamListView, TeamDetailView, TeamCreateView

urlpatterns = [
    path('list/', TeamListView.as_view(), name='team_list'),
    path('<int:pk>/', TeamDetailView.as_view(), name ='team_detail'),
    path('create/', TeamCreateView.as_view(), name='team_create'),
]