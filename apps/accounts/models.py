from django.contrib.auth.models import AbstractUser
from django.db import models

class CaptainUser(AbstractUser):
    """Custom User Model with user type, phone, and avatar."""

    class UserType(models.TextChoices):
        CLIENT = 'client', 'Client'
        EMPLOYEE = 'employee', 'Employee'
        GUEST = 'guest', 'Guest'

    user_type = models.CharField(max_length=10,choices=UserType.choices,default=UserType.EMPLOYEE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.get_user_type_display()}"
