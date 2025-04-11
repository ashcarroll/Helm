from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from projects.models import Task, Project
from django.http import JsonResponse
import json

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


@login_required
def project_status_data(request):
    user = request.user

    # Filter projects based on role
    if user.groups.filter(name='Manager').exists():
        projects_query = Project.objects.filter(manager=user)
    else:
        projects_query = Project.objects.filter(project_team=user)

    # Count projects by status
    status_counts = {
        'NOT_STARTED': 0,
        'ON_TRACK': 0,
        'AT_RISK': 0,
        'BLOCKED': 0,
        'COMPLETE': 0
    }

    # Populate counts
    for status, _ in Project.STATUS_CHOICES:
        status_counts[status] = projects_query.filter(status=status).count()

    # Format data for Chart.js
    data = {
        'counts': [
            status_counts['NOT_STARTED'],
            status_counts['ON_TRACK'],
            status_counts['AT_RISK'],
            status_counts['BLOCKED'],
            status_counts['COMPLETE']
        ]
    }

    return JsonResponse(data)


@login_required
def task_completion_data(request):
    user = request.user

    # Get date range for the last 7 days
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)

    # Get tasks completed by day
    date_list = []
    completion_counts = []

    for i in range(7):
        current_date = start_date + timedelta(days=i)
        date_list.append(current_date.strftime('%b %d'))

        # Count tasks completed on this date
        if user.groups.filter(name='Manager').exists():
            # Managers see completion stats for the projects they manage
            count = Task.objects.filter(
                project__manager=user,
                status='DONE',
                date_updated__date=current_date
            ).count()
        else:
            # ICs see completion data for tasks assigned to them
            count = Task.objects.filter(
                assigned_to=user,
                status='DONE',
                date_updated__date=current_date
            ).count()

        completion_counts.append(count)

    data = {
        'dates': date_list,
        'completedCounts': completion_counts
    }

    return JsonResponse(data)





