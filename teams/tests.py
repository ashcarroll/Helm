from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Team
from .forms import TeamForm


#  TEAM MODEL TESTS

class TeamModelTests(TestCase):
    def setUp(self):
        # Create manager user for testing
        self.manager = User.objects.create_user(
            username='manager1',
            password='testpass',
            email='manager1@example.com'
        )

        # Create a team with this manager
        self.team = Team.objects.create(name='Design Team', manager=self.manager)

    def test_team_str(self):
        # Test that the __str__ method returns the team name
        self.assertEqual(str(self.team), 'Design Team')



#  TEAM FORM TESTS

class TeamFormTests(TestCase):
    def setUp(self):
        # Create a couple of users to use in member field
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

    def test_valid_team_form(self):
        # Test that TeamForm is valid with proper data
        form_data = {
            'name': 'Marketing Team',
            'members': [self.user1.id, self.user2.id]
            }
        form = TeamForm(data=form_data)
        form.fields['members'].queryset = User.objects.all()
        self.assertTrue(form.is_valid())
    
    def test_invalid_team_form(self):
        # Test that the form is invalid if a required field is missing
        form_data = {'name':''}
        form = TeamForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)



#  TEAM VIEWS TESTS

class TeamViewsTests(TestCase):
    def setUp(self):
        # Create groups for role testing
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

        # Create a team managed by manager and include the IC as a team member
        self.team = Team.objects.create(name='Design Team', manager=self.manager)
        self.team.members.add(self.ic_user)

        self.client = Client()

    def test_team_create_view_as_manager(self):
        # Test manager can create a new team
        self.client.login(username='manager1', password='testpass')
        create_url = reverse('team_create')
        form_data = {'name':'New Team', 'members':[self.ic_user.id]}
        response = self.client.post(create_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Team.objects.filter(name='New Team').exists())

    def test_team_create_view_as_ic(self):
        # Test to ensure an IC cannot access the team creation functionality
        self.client.login(username='ic1', password='testpass')
        create_url = reverse('team_create')
        response = self.client.get(create_url)
        self.assertNotEqual(response.status_code, 200)

    def test_team_list_view_as_manager(self):
        # Test that a manager can see the teams tehey manage
        self.client.login(username='manager1', password='testpass')
        list_url = reverse('team_list')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.team.name)

    def test_team_list_view_as_ic(self):
        # Test that an IC can see the teams they belong to
        self.client.login(username='ic1', password='testpass')
        list_url = reverse('team_list')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.team.name)

    def test_team_detail_view(self):
        # Test that the team detail view displays team information
        self.client.login(username='manager1', password='testpass')
        detail_url = reverse('team_detail', kwargs={'pk': self.team.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.team.name)
        self.assertContains(response, self.manager.username)

    def test_team_update_view_as_manager(self):
        # Test that the team update view works for the team's manager
        self.client.login(username='manager1', password='testpass')
        update_url = reverse('team_update', kwargs={'pk': self.team.pk})
        form_data = {'name': 'Updated Team Name', 'members': [self.ic_user.id]}
        response = self.client.post(update_url, form_data)
        self.assertRedirects(response, reverse('team_list'))
        self.team.refresh_from_db()
        self.assertEqual(self.team.name, 'Updated Team Name')

    def test_team_updadte_view_as_ic(self):
        # Test that an IC cannot update a team
        self.client.login(username='ic1', password='testpass')
        update_url = reverse('team_update', kwargs={'pk': self.team.pk})
        response = self.client.post(update_url)
        self.assertNotEqual(response.status_code, 200)

    def test_team_delete_view_as_manager(self):
        # Test that the team's manager can delete the team
        self.client.login(username='manager1', password='testpass')
        delete_url = reverse('team_delete', kwargs={'pk': self.team.pk})
        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse('team_list'))
        self.assertFalse(Team.objects.filter(pk=self.team.pk).exists())

    def test_team_delete_view_as_ic(self):
        # Test that an IC cannot delete a team
        self.client.login(username='ic1', password='testpass')
        delete_url = reverse('team_delete', kwargs={'pk': self.team.pk})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Team.objects.filter(pk=self.team.pk).exists())