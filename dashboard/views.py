from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from projects.models import Task, Project

@login_required
def dashboard_view(request):
    user = request.user
    is_manager = user.groups.filter(name='Manager').exists()

    # Get relevant project detail depending on role
    if is_manager:
        projects = Project.objects.filter(manager=user)
    else:
        projects = Project.objects.filter(project_team=user)

    # Get active uncomplete projects
    active_projects = projects.exclude(status='COMPLETE')

    # Get tasks assigned to the user
    assigned_tasks = Task.objects.filter(assigned_to=user).order_by('-due_date')

    # Count stats
    active_projects_count = active_projects.count()
    open_tasks_count = assigned_tasks.exclude(status='DONE').count()
    completed_tasks_count = assigned_tasks.filter(status='DONE').count()

    # Tasks due this week
    today = timezone.now().date()
    week_later = today + timedelta(days=7)
    upcoming_due_count = assigned_tasks.exclude(status='DONE').filter(
        due_date__gte=today,
        due_date__lte=week_later
    ).count()

    # Task stats
    all_tasks = Task.objects.filter(project__in=projects)
    todo_count = all_tasks.filter(status='TODO').count()
    in_progress_count = all_tasks.filter(status='IN_PROGRESS').count()
    blocked_count = all_tasks.filter(status='BLOCKED').count()
    done_count = all_tasks.filter(status='DONE').count()
    

    context = {
        'username': request.user.username,
        'assigned_tasks': assigned_tasks,
        'active_projects': active_projects,
        'active_projects_count': active_projects_count,
        'open_tasks_count': open_tasks_count,
        'completed_tasks_count': completed_tasks_count,
        'upcoming_due_count': upcoming_due_count,
        'todo_count': todo_count,
        'in_progress_count': in_progress_count,
        'blocked_count': blocked_count,
        'done_count': done_count,
    }
    
    return render(request, 'dashboard/dashboard.html', context)




