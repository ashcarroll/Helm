from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Team
from .forms import TeamForm
from projects.models import Project

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


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'teams/team_detail.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get.object()

        team_projects = Project.objects.filter(project_team__in=team.members.all()).distinct()

        for project in team_projects:
            total_tasks = project.tasks.count()
            if total_tasks > 0:
                completed_tasks = project.tasks.filter(status='DONE').count()
                project.completion_percentage = int((completed_tasks / total_tasks)* 100)
            else:
                project.completion_percentage = 0
        
        context['projects'] = team_projects
        return context


class TeamUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/team_update.html'
    context_object_name = 'team'
    success_url = reverse_lazy('team_list')

    def form_valid(self, form):
        messages.success(self.request, "Team updated")
        return super().form_valid(form)
    
    def test_func(self):
        # Only this team's manager can update
        team = self.get_object()
        return team.manager == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to edit this team")
        return redirect('team_list')


class TeamDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Team
    template_name = 'teams/team_delete.html'
    context_object_name = 'team'

    def get_success_url(self):
        messages.success(self.request, "Team delelted successfully")
        return reverse('team_list')
    
    def test_func(self):
        team = self.get_object()
        return team.manager == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to delete this team")
        return redirect('team_list')