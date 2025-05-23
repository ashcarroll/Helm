from django.db import models
from django.contrib.auth.models import User
from teams.models import Team

class Project(models.Model):
    STATUS_CHOICES = [
    ('NOT_STARTED', 'Not Started'),
    ('ON_TRACK', 'On Track'),
    ('AT_RISK', 'At Risk'),
    ('BLOCKED', 'Blocked'),
    ('COMPLETE', 'Complete'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='NOT_STARTED')
    start_date = models.DateField()
    end_date = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name = 'managed_projects')
    project_team = models.ManyToManyField(User, blank=True, related_name='project_team')

    def __str__(self):
        return self.title
    
    def completion_percentage(self):
        total_tasks = self.tasks.count()
        if total_tasks == 0:
            return 0
        
        completed_tasks = self.tasks.filter(status='DONE').count()
        return round((completed_tasks / total_tasks) * 100)
    
    
class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('BLOCKED', 'Blocked'), 
        ('DONE', 'Done')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    due_date = models.DateField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title