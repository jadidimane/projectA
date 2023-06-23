from django.db import models
from django.db import models

class Candidature(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    cv = models.FileField(upload_to='motivation/')
    lettre_motivation=models.FileField(upload_to='motivation/')
# Create your models here.
