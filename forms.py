from django import forms
from .models import Candidats,Agent
from django.contrib.auth.forms import UserCreationForm
class CandidateAuthentificationForm(UserCreationForm):
    class Meta:
        model=Candidats
        fields=['nom','prenom','email','telephone']
class AgentAuthentificationForm(UserCreationForm):
    class Meta:
        model=Agent
        fields=['nom','prenom','email','telephone']