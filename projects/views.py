from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Project, Task
from .forms import ProjectForm, TaskForm


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
            return Project.objects.filter(project_team=user)
        
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
        form.save_m2m()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        project = self.get_object()

        is_manager = user.groups.filter(name='Manager').exists()
        is_in_team = project.project_team.filter(pk=user.pk).exists()

        context['is_manager'] = is_manager
        context['is_in_team'] = is_in_team
        return context


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_update.html'
    context_object_name = 'project'

    def form_valid(self, form):
        messages.success(self.request, "Project updated successfully")
        return super().form_valid(form)
    
    def test_func(self):
        # Only the manager of the project can update
        project = self.get_object()
        return project.manager == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to edit this project")
        return redirect('project_list')


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'projects/project_delete.html'
    success_url = reverse_lazy('project_list')

    def test_func(self):
        # Only the manager of the project can delete it
        project = self.get_object()
        return project.manager == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to delete this project")
        return redirect('project_list')


class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'projects/task_create.html'

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=kwargs['project_id'])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        task = form.save(commit=False)
        task.project = self.project
        task.created_by = self.request.user
        task.save()
        messages.success(self.request, "Task created successfully")
        return redirect('project_detail', pk=self.project.pk)
    
    def test_func(self):
        user = self.request.user

        # Check if user is a Manager
        if user.groups.filter(name='Manager').exists():
            return True
        
        # Or if user is assigned the project team
        if self.project.project_team.filter(pk=user.pk).exists():
            return True
        
        # Otherwise deny 
        return False
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to create a task for this project")
        return redirect('project_list')
    

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'projects/task_update.html'

    def dispatch(self, request, *args, **kwargs):
        self.task = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Task.objects.all()
        
        else:
            return Task.objects.filter(assigned_to=user)
    
    def get_success_url(self):
        project_pk = self.task.project.pk
        return reverse_lazy('project_detail', kwargs={'pk':project_pk})

