from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy, reverse
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

        # Adding all projects to context
        context = ['all_projects'] = Project.objects.all()

        # Add a flag to show if it's showing all projects or filtered
        context['show_all'] = self.request.GET.get('show_all', 'false') == 'true'

        if context['show_all']:
            context['projects'] = context['all_projects']

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

        # Group tasks by status
        tasks_by_status = {
            'TODO': project.tasks.filter(status='TODO'),
            'IN_PROGRESS': project.tasks.filter(status='IN_PROGRESS'),
            'BLOCKED': project.tasks.filter(status='BLOCKED'),
            'DONE': project.tasks.filter(status='DONE')
        }

        # Calculate completion percent
        total_tasks = project.tasks.count()
        completed_tasks = project.tasks.filter(status='DONE').count()
        completion_percentage = 0
        if total_tasks >0:
            completion_percentage = int((completed_tasks / total_tasks)* 100)

        context['is_manager'] = is_manager
        context['is_in_team'] = is_in_team
        context['tasks_by_status'] = tasks_by_status
        context['completion_percentage'] = completion_percentage
        context['todo_tasks'] = tasks_by_status['TODO']
        context['in_progress_tasks'] = tasks_by_status['IN_PROGRESS']
        context['blocked_tasks'] = tasks_by_status['BLOCKED']
        context['done_tasks'] = tasks_by_status['DONE']

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
    
    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.pk})



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
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.project
        return kwargs

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
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.project
        return kwargs
    
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Task.objects.all()
        
        else:
            return Task.objects.filter(assigned_to=user)
    
    def get_success_url(self):
        project_pk = self.task.project.pk
        return reverse_lazy('project_detail', kwargs={'pk':project_pk})


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'projects/task_delete.html'

    def get_success_url(self):
        return reverse ('project_detail', kwargs={'pk': self.object.project.pk})
    
    def test_func(self):
        task = self.get_object()
        # Allow delete if cuurent user is creator of task or in the Manager group
        return (self.request.user == task.created_by) or self.request.user.groups.filter(name='Manager').exists()
    
    def handle_no_permission(self):
        task = self.get_object()
        messages.error(self.request, "You don't have permission to delete this task")
        return redirect('project_detail', pk=task.project.pk)