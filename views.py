from django.shortcuts import render,redirect,HttpResponse
from .forms import OfferForm
from django.contrib import messages
from .models import offres 
def new_offer(request):
    if request.method != 'POST':
        form = OfferForm()
    else:
        form = OfferForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(job_offer_list)
    context = {'of': form}
    return render(request,"offres/new_job_offer.html",context)
def job_offer_list(request):
    offers= offres.objects.all()
    
    return render(request,'offres/job_offer_list.html', {'offres': offers})
def job_offer_list1(request):
    offers= offres.objects.all()
    
    return render(request,'offres/job_offer_list1.html', {'offres': offers})


def delete_offer(request,id):
     offre = offres.objects.get(pk=id)
     if request.method == 'POST':
        offre.delete()
        return redirect(job_offer_list)
    
     context = {'offre':offre}
     return render(request, 'offres/delete_offer.html', context )

def update_offer(request,id):
     offre = offres.objects.get(pk=id)
     if request.method != 'POST':
        form = OfferForm(instance = offre)
     else:
        form = OfferForm(instance = offre, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return render(request,'offres/reponse.html')
        else:
            HttpResponse('la modification a echoue reessayer')
     context = {'uf': form, 'offer':offre }
     return render(request, 'offres/update_job_offer.html', context )
def detail_offre(request, id):
    offre = offres.objects.get(pk=id)
    return render(request, 'offres/offre.html', {'offre': offre})

def detail_offre2(request, id):
    offre = offres.objects.get(pk=id)
    return render(request, 'offres/offer_postula.html', {'offre': offre})
def gestion_offres(request):
    return render(request,'offres/gestion_offres.html')
# Create your views here. 
