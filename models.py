from django.db import models

# Create your models here.
class offres(models.Model):
    id=models.BigAutoField(primary_key=True)
    datepub=models.DateField(null=True,blank=True)
    reference=models.CharField(null=True, blank=True,max_length=100)
    titre=models.CharField(null=True,blank=True,max_length=100)
    description=models.TextField(null=True,blank=True)
    localisation=models.CharField(null=True,blank=True,max_length=100)
    type_contrat=models.CharField(null=True,blank=True,max_length=100)
    experience=models.CharField(null=True,blank=True,max_length=100)
    email_recruteur=models.EmailField(null=True,blank=True)
    competences=models.CharField(null=True,blank=True,max_length=100)
    