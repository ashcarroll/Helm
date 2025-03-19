from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from .models import Team
from .forms import TeamForm

class TeamCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Team 
    form_class = TeamForm
    template_name = 'teams/team_create.html'

    def form_valid(self, form):
        team = form.save(commit=False)
        team.manager = self.request.user
        team.save()
        form.save_m2m()
        messages.success(self.request, "Team has been created successfully")
        return redirect('team_list')
    
    def test_func(self):
        # Only managers can create teams
        return self.request.user.groups.filter(name='Manager').exists()
    
    def handle_no_permission(self):
        messages.error(self.request, "Only managers can create teams")
        return redirect('team_list')


class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = 'teams/team_list.html'
    context_object_name = 'teams'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            # Managers sees the teams the manage
            return Team.objects.filter(manager=user)
        
        else:
            # IC sees the teams they are a part of
            return Team.objects.filter(members=user)
        
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        # Check if user is a manager
        context['is_manager'] = self.request.user.groups.filter(name='Manager').exists()
        return context