from django.db import models
from django.contrib.auth.models import User
from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary.utils import cloudinary_url
from django.templatetags.static import static


# Helper function to define upload path for profile pics
def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Using Cloudinary storage with custom upload path 
    image = models.ImageField(
        upload_to=user_directory_path,
        storage=MediaCloudinaryStorage(),
        null=True,
        blank=True,
        default='default.jpg'
    )

    def __str__(self):
        return f"{self.user.username} Profile"
    

    def get_image_url(self):
        if self.image and hasattr(self.image, 'name'): 
            # Generate a Cloudinary thumbnail URL
            return cloudinary_url(
                self.image.name, width=300, height=300, crop="lfill"
            )[0]
        else: 
            # Fallback to default image
            return cloudinary_url(
                "default.jpg", width=300, height=300, crop="lfill"
            )[0]