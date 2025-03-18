from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from projects.models import Task

@login_required
def dashboard_view(request):
    user = request.user
    assigned_tasks = Task.objects.filter(assigned_to=user)

    context = {
        'username': request.user.username,
        'assigned_tasks': assigned_tasks,
    }
    return render(request, 'dashboard/dashboard.html', context)