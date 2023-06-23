

from django.shortcuts import render, redirect
from .forms import CandidatureForm

def candidature(request):
    if request.method == 'POST':
        form = CandidatureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(candidature_success)
    else:
        form = CandidatureForm()
    return render(request, 'candidatures/candidature.html', {'form': form})

def candidature_success(request):
    return render(request, 'candidatures/candidature_success.html')
