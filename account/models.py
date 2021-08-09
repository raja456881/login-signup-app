from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
# Create your models here.


USER_CHOICES=(
    ("PATIENT", "PATIENT"),
    ("DOCTOR", "DOCTOR"),
)
Catergory_Choices=(
    ( "Mental Health", "Mental Heart"),
    ("Heart Disease", "Heart Disease"),
    ("Covid 19", "Covid 19"),
    ("Immunization", "Immunization")
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

class Blog(models.Model):
    title=models.CharField(max_length=100)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog")
    image=models.ImageField(upload_to="media/blog")
    category=models.CharField(max_length=30, choices=Catergory_Choices)
    summary=models.TextField(max_length=200)
    content=models.TextField(max_length=100)

class Draft(models.Model):
    title=models.CharField(max_length=100)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="draft")
    image=models.ImageField(upload_to="media/blog")
    category=models.CharField(max_length=30, choices=Catergory_Choices)
    summary=models.TextField(max_length=200)
    content=models.TextField(max_length=100)


@receiver(pre_save, sender=Blog)
def CreateDraft(sender, instance, **kwargs):
        Draft.objects.create(user=instance.user, title=instance.title, image=instance.image,
                              category=instance.category, summary=instance.summary, content=instance.content)