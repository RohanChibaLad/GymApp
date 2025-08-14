from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    firstName = models.CharField(max_length=30, blank=True)
    lastName = models.CharField(max_length=30, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    dateOfBirth = models.DateField(null=True, blank=True)
    phoneNumber = models.CharField(max_length=15, null=True, blank=True)    

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["username"]
        indexes = [models.Index(fields=["email"])]