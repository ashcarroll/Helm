from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Project, Task
from .forms import ProjectForm, TaskForm
from datetime import date

# ---------------------------------------------------------------------------------------
#  PROJECT TESTS
# ---------------------------------------------------------------------------------------


#  PROJECT MODEL TESTS

class ProjectModelTests(TestCase):
    def setUp(self):
        # Create manager user for testing
        self.manager = User.objects.create_user(
            username='manager1',
            password='testpass',
            email='manager1@example.com'
        )
        self.project = Project.objects.create(
            title = 'Test Project',
            description = 'A test project',
            status = 'NOT_STARTED',
            start_date=date.today(),
            end_date=date.today(),
            manager=self.manager
        )

    def test_project_str(self):
        # Test that the __str__ method returns the project title
        self.assertEqual(str(self.project), "Test Project")



#  PROJECT FORM TESTS

class ProjectFormTests(TestCase):
    def setUp(self):
        # Create a couple of users for the members of project team field
        self.user1 = User.objects.create_user(
            username='user1', 
            password='pass1',
            email='user1@example.com'
        )
        self.user2 = User.objects.create_user(
            username='user2', 
            password='pass2',
            email='user2@example.com'
        )

    def test_valid_project_form(self):
        # Test that the ProjectForm is valid with proper data
        form_data = {
            'title': 'Marketing Project',
            'description': 'Project for marketing',
            'status': 'ON_TRACK',
            'start_date': date.today(),
            'end_date': date.today(),
            'project_team': [str(self.user1.id), str(self.user2.id)]
        }
        form = ProjectForm(data=form_data)
        form.fields['project_team'].queryset = User.objects.all()
        self.assertTrue(form.is_valid())

    def test_invalid_project_form(self):
        # Test that the form is invalid if field is missing
        form_data = {
            'title': '',
            'description': 'Project for marketing.',
            'status': 'ON_TRACK',
            'start_date': date.today(),
            'end_date': date.today(),
            'project_team': [str(self.user1.id), str(self.user2.id)]
        }
        form = ProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)


#  PROJECT VIEWS TESTS

class ProjectViewsTests(TestCase):
    def setUp(self):
        # Create groups
        self.manager_group = Group.objects.create(name='Manager')
        self.ic_group = Group.objects.create(name='IC')

        # Create a manager and add to Mnager group
        self.manager = User.objects.create_user(
            username='manager1', 
            password='testpass',
            email='manager1@example.com'
        )
        self.manager_group.user_set.add(self.manager)

        # Create an IC and add to the IC group
        self.ic_user = User.objects.create_user(
            username='ic1', 
            password='testpass',
            email='ic1@example.com'
        )
        self.ic_group.user_set.add(self.ic_user)

        # Create a project managed by the manager and assign the IC to it
        self.project = Project.objects.create(
            title='View Test Project',
            description='Testing project views',
            status='ON_TRACK',
            start_date=date.today(),
            end_date=date.today(),
            manager=self.manager
        )
        self.project.project_team.add(self.ic_user)

        self.client = Client()

    def test_project_list_view_as_manager(self):
        # Test that a manager sees projects they manage
        self.client.login(username='manager1', password='testpass')
        list_url = reverse('project_list')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.title)

    def test_project_list_view_as_ic(self):
        # Test that an IC sees the projects they are assigned to 
        self.client.login(username='ic1', password='testpass')
        list_url = reverse('project_list')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.title)

    def test_project_detail_view(self):
        # Test that the project detail view shows project information
        self.client.login(username='manager1', password='testpass')
        detail_url = reverse('project_detail', kwargs={'pk': self.project.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)

    def test_project_create_view_as_manager(self):
        # Test that a manager can create a project
        self.client.login(username='manager1', password='testpass')
        create_url = reverse('project_create')
        form_data = {
            'title': 'New Project',
            'description': 'Project created by manager',
            'status': 'NOT_STARTED',
            'start_date': date.today(),
            'end_date': date.today(),
            'project_team': [str(self.ic_user.id)]
        }
        response = self.client.post(create_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(title='New Project').exists())

    def test_project_create_view_as_ic(self):
        # Tets that an IC can't access the project creation view
        self.client.login(username='ic1', password='testpass')
        create_url = reverse('project_create')
        response = self.client.post(create_url)
        self.assertNotEqual(response.status_code, 200)

    def test_prject_update_view_as_manager(self):
        # Test that a manager can upfate a porject
        self.client.login(username='manager1', password='testpass')
        update_url = reverse('project_update', kwargs={'pk': self.project.pk})
        form_data = {
            'title': 'Update Project Title',
            'description': self.project.description,
            'status': self.project.status,
            'start_date': self.project.start_date,
            'end_date': self.project.end_date,
            'project_team': [str(self.ic_user.id)]
        }
        response = self.client.post(update_url, form_data)
        self.assertRedirects(response, reverse('project_detail', kwargs={'pk': self.project.pk}))
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, 'Update Project Title')

    def test_project_delete_view_as_manager(self):
        # Test that a manager can delete a project
        self.client.login(username='manager1', password='testpass')
        delete_url = reverse('project_delete', kwargs={'pk': self.project.pk})
        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse('project_list'))
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_project_delete_view_as_ic(self):
        # Test that an IC cannot delete a project
        self.client.login(username='ic1', password='testpass')
        delete_url = reverse('project_delete', kwargs={'pk': self.project.pk})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())



# ---------------------------------------------------------------------------------------
#  TASKS TESTS
# ---------------------------------------------------------------------------------------


#  TASK MODEL TESTS

class TaskModelTests(TestCase):
    def setUp(self):
        # Create users
        self.manager = User.objects.create_user(
            username='manager1', 
            password='testpass',
            email='manager1@example.com'
        )
        self.user = User.objects.create_user(
            username='ic1', 
            password='testpass',
            email='ic1@example.com'
        )

        # Create project for tasks
        self.project = Project.objects.create(
            title='Task Project',
            description='Project for tasks',
            status='ON_TRACK',
            start_date=date.today(),
            end_date=date.today(),
            manager=self.manager
        )

        # Create a task
        self.task = Task.objects.create(
            title='Test Task',
            description='A test task',
            project=self.project,
            assigned_to=self.user,
            created_by=self.manager,
            status='TODO',
            due_date=date.today()
        )

    def test_task_str(self):
        # Test that the __str__ method returns the task title
        self.assertEqual(str(self.task), "Test Task")


#  TASK FORM TESTS

class TaskFormTests(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(
            username='user1', 
            password='pass1',
            email='user1@example.com'
        )
        self.user2 = User.objects.create_user(
            username='user2', 
            password='pass2',
            email='user2@example.com'
        )
        self.manager = User.objects.create_user(
            username='manager1', 
            password='testpass',
            email='manager1@example.com'
        )

        # Create a project
        self.project = Project.objects.create(
            title='Test Project',
            description='Project for task testing',
            status='NOT_STARTED',
            start_date=date.today(),
            end_date=date.today(),
            manager=self.manager
        )

    def test_valid_task_form(self):
        # Test that TaskForm is valid with proper data
        form_data = {
            'title': 'New Task',
            'description': 'A task description',
            'assigned_to': self.user1.id,
            'status': 'TODO',
            'due_date': date.today(),
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_task_form(self):
        # Test that the task form is invalid when data is missing
        form_data = {
            'title': '',
            'description': 'A task without a title',
            'assigned_to': self.user1.id,
            'status': 'TODO',
            'due_date': date.today(),
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)


#  TASK VIEWS TESTS

class TaskViewsTests(TestCase):
    def setUp(self):
        # Create groups
        self.manager_group = Group.objects.create(name='Manager')
        self.ic_group = Group.objects.create(name='IC')

        # Create Manager
        self.manager = User.objects.create_user(
            username='manager1', 
            password='testpass',
            email='manager1@example.com'
        )
        self.manager_group.user_set.add(self.manager)

        # Create IC
        self.ic_user = User.objects.create_user(
            username='ic1', 
            password='testpass',
            email='ic1@example.com'
        )
        self.ic_group.user_set.add(self.ic_user)

        # Create project that is managed by the manager and has the IC as a member
        self.project = Project.objects.create(
            title='Test Project',
            description='Project for task testing',
            status='ON_TRACK',
            start_date=date.today(),
            end_date=date.today(),
            manager=self.manager
        )
        self.project.project_team.add(self.ic_user)

        # Create a task
        self.task = Task.objects.create(
            title="Test Task",
            description="A task for testing",
            project=self.project,
            assigned_to=self.ic_user,
            created_by=self.manager,
            status="TODO",
            due_date=date.today()
        )
        self.client = Client()

    def test_task_create_view_as_manager(self):
        # Test that a manager can create a task for the project
        self.client.login(username='manager1', password='testpass')
        create_url = reverse('task_create', kwargs={'project_id': self.project.pk})
        form_data = {
            'title': 'New Task',
            'description': 'A task created by the manager',
            'assigned_to': self.ic_user.id,
            'status': 'TODO',
            'due_date': date.today(),
        }
        response = self.client.post(create_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.project.tasks.filter(title="New Task").exists())

    def test_task_create_view_as_ic(self):
        # Test to ensure an IC can create a task if they are part of the project team
        self.client.login(username='ic1', password='testpass')
        create_url = reverse('task_create', kwargs={'project_id':self.project.pk})
        form_data = {
            'title': 'IC Task',
            'description': 'A task created by an IC',
            'assigned_to': self.ic_user.id,
            'status': 'TODO',
            'due_date': date.today(),
        }
        response = self.client.post(create_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.project.tasks.filter(title="IC Task").exists())

    def test_task_update_view(self):
        # Test that a task can be updated
        self.client.login(username='manager1', password='testpass')
        update_url = reverse('task_update', kwargs={'pk':self.task.pk})
        form_data = {
            'title': 'Updated Task',
            'description': self.task.description,
            'assigned_to': self.ic_user.id,
            'status': 'IN_PROGRESS',
            'due_date': self.task.due_date,
        }
        response = self.client.post(update_url, form_data)
        self.assertRedirects(response, reverse('project_detail', kwargs={'pk': self.project.pk}))
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_task_delete_view_as_manager(self):
        # Test that a manager can delete a task
        self.client.login(username='manager1', password='testpass')
        delete_url = reverse('task_delete', kwargs={'pk':self.task.pk})
        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse('project_detail', kwargs={'pk':self.project.pk}))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_delete_view_as_ic(self):
        # Test that an IC can't delete a task, if they do not meet the permission requirements (arent the task creator)
        self.client.login(username='ic1', password='testpass')
        delete_url = reverse('task_delete', kwargs={'pk': self.task.pk})
        response = self.client.post(delete_url)

        self.assertEqual(response.status_code, 302)
        # Check the task still exists after the attempted deletion
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())