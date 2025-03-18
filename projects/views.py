from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, DetailView
from .models import Project
from .forms import ProjectForm

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            # Managers see the projects they manage
            return Project.objects.filter(manager=user)
        
        else:
            # IC sees their team's projects
            return Project.objects.filter(team__in=user.teams.all())
        
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        # Adding a boolean to see if user is a manager
        context['is_manager'] = self.request.user.groups.filter(name='Manager').exists()
        return context


class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create_project.html'

    def form_valid(self, form):
        project = form.save(commit=False)
        project.manager = self.request.user
        project.save()
        messages.success(self.request, "Project has been created successfully")

        return redirect('project_list')
    
    def test_func(self):
        # Only managers can access this view
        return self.request.user.groups.filter(name='Manager').exists()
    
    def handle_no_permission(self):
        # Error handling to protect view on the backend, incase URL is guessed and UI constraints are bypassed
        messages.error(self.request, "Only managers can create projects")
        return redirect('project_list')
    

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

