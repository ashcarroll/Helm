from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    context = {
        'username': request.user.username
    }
    return render(request, 'dashboard/dashboard.html', context)