from django.db import models # Importing Django models
from django.contrib.auth.models import AbstractUser # Importing AbstractUser to create a custom user model
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator # Importing validators for model fields

phone_validator = RegexValidator(r"^\+?[1-9]\d{1,14}$", "Enter a valid phone number.") # Regex for phone number validation

class User(AbstractUser): # Custom User model inheriting from AbstractUser
    email = models.EmailField(unique=True) #Email field with unique constraint
    date_of_birth = models.DateField(null=True, blank=True) #Date of birth field that can be null or blank
    
    #Phone number field with regex validation
    phone_number = models.CharField(
        unique=True, 
        max_length=15, 
        null=True, 
        blank=True, 
        validators=[phone_validator]
    )

    # Weight field with decimal validation
    weight = models.DecimalField(
        null=True, 
        blank=True, 
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0)])
    
    #Height field with positive integer validation
    height = models.PositiveIntegerField( 
        null=True, 
        blank=True,
        validators=[MinValueValidator(40), MaxValueValidator(300)]
    )
    def __str__(self): # String representation of the User model
        return self.username

    class Meta: # Meta class for User model
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["username"]