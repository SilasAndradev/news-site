from django.db import models
from django.contrib.auth.models import User


class ReaderProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE
        )

    bio = models.TextField(blank=True, null=True)
    
    ProfilePicture = models.ImageField(
        upload_to="uploads/perfis",
        blank=True
        )
    
    CommentPermission = models.BooleanField(
        default=True
        )
    
    PermissionChangeProfile = models.BooleanField(
        default=True
        )
    

    def __str__(self):
        return self.user.username



    