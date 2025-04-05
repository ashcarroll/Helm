from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import Profile
from .forms import UserRegisterForm, ProfileUpdateForm


# PROFILE MODEL TESTS

class ProfileModelTests(TestCase):
    def setUp(self):
        # Create a user to check profile creation is triggered by signals
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            email="testuser@example.com"
        )
    
    def test_profile_created_on_user_creation(self):
        # Test a profile is automatically created when a new user is created
        self.assertTrue(hasattr(self.user, 'profile'))
        # Check default image is used
        self.assertEqual(self.user.profile.image.name, 'default.jpg')

    def test_profile_str(self):
        # Test that the __str__ method of Profile returns expected string
        expected_str = f"{self.user.username} Profile"
        self.assertEqual(str(self.user.profile), expected_str)


#  USER FORMS TESTS

class UserFormsTests(TestCase):
    def test_valid_registration_form(self):
        # Test UserRegisterForm validates correctly
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'role': 'IC',
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid(), "UserRegisterForm should be valid with correct data")
    
    def test_invalid_registration_form_password_mismatch(self):
        # Test that the form is invalid if passwords do not match
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'DifferentPass456!',
            'role': 'IC',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid(), "UserRegisterForm should be invalid if passwords do not match")
        self.assertIn('password2', form.errors)

    def test_role_field_choices(self):
        # Test that the role field in registration form contains the expected choices
        form = UserRegisterForm()
        expected_choices = [('Manager', 'Manager'), ('IC', 'IC')]
        self.assertEqual(form.fields['role'].choices, expected_choices, "The role field should have the expected choices")

    def test_invalid_profile_update_form(self):
        # Test that the ProfileUpdateForm is invalid with a non-image file
        invalid_file =SimpleUploadedFile("test.txt", b"Not an image", content_type="image/gif")
        form = ProfileUpdateForm(data={}, files={'image': invalid_file})
        self.assertFalse(form.is_valid(), "ProfileUpdateForm should be invalid with a non-image file")


#  USER VIEWS TESTS

class UserViewTests(TestCase):
    def setUp(self):
        # Create groups needed for registration and role assignment
        self.manager_group = Group.objects.create(name='Manager')
        self.ic_group = Group.objects.create(name='IC')

        # Create a test user in the manager group
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            email="testuser@example.com"
        )
        self.manager_group.user_set.add(self.user)
        self.client = Client()

    
    def test_registration_view_creates_user_and_profile(self):
        # Test that the registration view creates a new user with a profile and assigns to the correct group
        registration_url = reverse("register")
        form_data ={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'role': 'IC',
        }
        response = self.client.post(registration_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard"))

        # Check the user was created
        self.assertTrue(User.objects.filter(username="newuser").exists())
        new_user = User.objects.get(username="newuser")
        self.assertTrue(hasattr(new_user, 'profile'))
        self.assertTrue(new_user.groups.filter(name="IC").exists())


    def test_profile_update_view(self):
        # Test profile update view correctly updates teh profile picture
        self.client.login(username="testuser", password="testpass")
        update_url = reverse("profile_update")

        # Create fake image to upload
        image_content = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00'
            b'\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x00\x00\x00\x00\x00'
            b'\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4C\x01\x00'
            b'\x3B'
        )
        uploaded_image = SimpleUploadedFile("test.gif", image_content, content_type="image/gif")
        response = self.client.post(update_url, {'image': uploaded_image})
        self.assertRedirects(response, reverse("profile"))
        self.user.profile.refresh_from_db()
        self.assertNotEqual(self.user.profile.image.name, "default.jpg")
