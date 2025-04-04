from django.db import models
from django.contrib.auth.models import User

# Helper function to define upload path for profile pics
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Using an upload_to function to organize uploads in folders by user ID
    image = models.ImageField(upload_to=user_directory_path, default='default.jpg')

    def __str__(self):
        return f"{self.user.username} Profile"