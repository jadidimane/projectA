
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from app.tokens import generatorToken
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from offres import *
from offres.views import *
from temoignage import *
from temoignage.views import *
from .models import candidat,agent
@csrf_protect
def home(request):
    return render(request, 'index.html')

@csrf_protect
def Candidate_register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        email = request.POST['email']
        mot_de_passe = request.POST['mot_de_passe']
        mot_de_passe1 = request.POST['mot_de_passe1']
        if mot_de_passe != mot_de_passe1:
            messages.error(request, 'Les mots de passe ne correspondent pas')
            return redirect(Candidate_register_view)
        candidat.user=User.objects.create_user(email=email,password=mot_de_passe,username=username)
        candidat.user.first_name=prenom
        candidat.user.last_name=nom
        candidat.user.save()
        candidat.is_candidate=True
        messages.success(request, 'Votre compte a été créé avec succès!')

        # Envoi d'un mail de bienvenu
        subject = "Bienvenu sur TechWork"
        message = "Bonjour " + candidat.user.first_name + "\n \n Bienvenue sur TechWork, votre plateforme de recrutement spécialisée dans les métiers de la technologie ! \n \n Trouvez votre prochaine opportunité professionnelle parmi nos offres d'emploi de premier plan. \n \n Explorez, postulez et faites avancer votre carrière dès aujourd'hui."
        from_email = settings.EMAIL_HOST_USER
        to_list = [candidat.user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)


        # Envoi d'un mail de confirmation
        current_site = get_current_site(request)
        email_subject = "Confirmation de compte"
        message_confirm = render_to_string("email_confirm.html", {
            "name": candidat.user.first_name,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(candidat.user.pk)),
            "token": generatorToken.make_token(candidat.user),
        })
        email = EmailMessage(
            email_subject,
            message_confirm,
            from_email,
            to_list,
        )
        email.send()
        messages.info(request, "Un email de confirmation a été envoyé à votre adresse. Veuillez vérifier votre boîte de réception.")
        return redirect(candidat_login)

    return render(request, 'candidate_register.html')

def Agent_register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        email = request.POST['email']
        mot_de_passe = request.POST['mot_de_passe']
        mot_de_passe1 = request.POST['mot_de_passe1']
        if mot_de_passe != mot_de_passe1:
            messages.error(request, 'Les mots de passe ne correspondent pas')
            return redirect(Agent_register_view)
            
        
        agent.user=User.objects.create_user(email=email,password=mot_de_passe,username=username)
        agent.user.first_name=prenom
        agent.user.last_name=nom
        agent.save()
        messages.success(request, 'Votre compte a été créé avec succès!')

        # Envoi d'un mail de bienvenu
        subject = "Bienvenu sur TechWork"
        message = "Bonjour " + agent.user.first_name + "\n \n Bienvenue sur TechWork, votre plateforme de recrutement spécialisée dans les métiers de la technologie ! \n \n Trouvez votre prochaine opportunité professionnelle parmi nos offres d'emploi de premier plan. \n \n Explorez, postulez et faites avancer votre carrière dès aujourd'hui."
        from_email = settings.EMAIL_HOST_USER
        to_list = [agent.user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)


        # Envoi d'un mail de confirmation
        current_site = get_current_site(request)
        email_subject = "Confirmation de compte"
        message_confirm = render_to_string("email_confirm.html", {
            "name": agent.user.first_name,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(agent.user.pk)),
            "token": generatorToken.make_token(agent.user),
        })
        email = EmailMessage(
            email_subject,
            message_confirm,
            from_email,
            to_list,
        )
        email.send()
        messages.info(request, "Un email de confirmation a été envoyé à votre adresse. Veuillez vérifier votre boîte de réception.")
        return redirect(agent_login)

    return render(request, 'agent_register.html')

        
@csrf_protect

def candidat_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        mot_de_passe = request.POST.get('mot_de_passe')
        candidat.user = authenticate(request, username=username, password=mot_de_passe)
        my_user=User.objects.get(username=username)
        if candidat.user is not None:
            login(request, candidat.user)
            candidat.is_candidate=True
            return redirect(job_offer_list)
        elif my_user.is_active == False:
            return render(request,'reponse1.html')

        else:
            return redirect(candidat_login)

    return render(request, 'candidate_login.html')

def agent_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        mot_de_passe = request.POST.get('mot_de_passe')
        user = authenticate(request, username=username, password=mot_de_passe)
        my_user=User.objects.get(username=username)
        if user is not None:
            login(request, agent.user)
            redirect(gestion_offres)
        elif my_user.is_active == False:
            messages.error(request, "Vous n'avez pas comfirmer votre email") 

        else:
            messages.error(request, 'Votre login est incorrect')
            return redirect('agent_login')

    return render(request, 'agent_login.html')


@csrf_protect
def user_logout(request):
    logout(request)
    messages.success(request, 'Votre compte a été déconnécté!')
    return redirect(home)

@csrf_protect
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        if user is not None and generatorToken.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Votre Compte a été activé")
            if candidat.is_candidate==True:
              return redirect(candidat_login)
            elif agent.is_agent==True:
              return redirect(agent_login)
        else:
            messages.error(request, "Votre Compte n'a pas été activé!")
            return redirect('home')
            
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None:
        messages.error(request, "Votre Compte n'a pas été activé!")
        return redirect('home')

@csrf_protect
def acceuil(request):
    return render(request, 'acceuil.html')
@csrf_protect
def offres(request):
    return redirect(job_offer_list1)
@csrf_protect
def temoignages(request):
    return redirect(temoignages_list)
@csrf_protect
def apropos(request):
    return render(request, 'apropos.html')


