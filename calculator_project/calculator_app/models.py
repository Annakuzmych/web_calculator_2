from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager
from .managers import ProUserManager


class ProUser(AbstractUser): 
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    objects = ProUserManager()
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 


class Message(models.Model):
    user = models.ForeignKey(ProUser, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    room_name = models.CharField(max_length=100, default='general')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} at {self.timestamp}'
    
class CalculationHistory(models.Model):
    user = models.ForeignKey(ProUser, on_delete=models.CASCADE, default=1)
    expression = models.CharField(max_length=100)
    result = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

class ConversionHistory(models.Model):
    user = models.ForeignKey(ProUser, on_delete=models.CASCADE, default=1)
    number = models.CharField(max_length=100)
    from_base = models.IntegerField()
    to_base = models.IntegerField()
    result = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)



