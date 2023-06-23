from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
class candidat(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    is_candidate=True
    
    
class agent(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    is_agent=True
    