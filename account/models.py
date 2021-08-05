from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


USER_CHOICES=(
    ("PATIENT", "PATIENT"),
    ("DOCTOR", "DOCTOR"),
)


class User(AbstractUser):
    user_type=models.CharField(max_length=20, choices=USER_CHOICES)
    username = models.CharField(max_length=34,  db_index=True)
    profilepicture=models.ImageField(upload_to="media/photo")
    email=models.CharField(max_length=30, unique=True)
    address=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    state=models.CharField(max_length=30)
    pincode=models.CharField(max_length=40)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

