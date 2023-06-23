from django import forms
from .models import offres
class OfferForm(forms.ModelForm):
    class Meta:
        model=offres
        fields=['datepub','reference','titre','description','localisation','type_contrat','experience','email_recruteur','competences']
          
    
    
    
    
    
    
    
    

