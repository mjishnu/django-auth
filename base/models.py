from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class UserTypes(models.TextChoices):
        PATIENT = "patient", "Patient"
        DOCTOR = "doctor", "Doctor"

    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)

    email = models.EmailField(unique=True)
    user_type = models.CharField(
        max_length=20,
        choices=UserTypes.choices,
        default=UserTypes.PATIENT,
    )
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"{self.username} ({self.get_user_type_display()})"
