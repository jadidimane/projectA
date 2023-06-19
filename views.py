from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
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

@csrf_protect
def home(request):
    return render(request, 'app/index.html')

@csrf_protect
def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        telephone = request.POST['telephone']
        email = request.POST['email']
        mot_de_passe = request.POST['mot_de_passe']
        mot_de_passe1 = request.POST['mot_de_passe1']
        if User.objects.filter(username=username):
            messages.error(request, "Ce nom d'utilisateur est déjà utilisé.")
            return redirect('register')
        if User.objects.filter(email=email):
            messages.error(request, "Cette adresse email est déjà utilisée.")
            return redirect('register')
            
        if mot_de_passe != mot_de_passe1:
            messages.error(request, 'Les mots de passe ne correspondent pas')
            return redirect('register')
        if not username.isalnum():
            messages.error(request, 'Le nom d\'utilisateur doit être alphanumérique')
            return redirect('register')
            
        user = User.objects.create_user(username=username, email=email, password=mot_de_passe)

        user.first_name = prenom
        user.last_name = nom
        user.is_active = False
        user.save()
        messages.success(request, 'Votre compte a été créé avec succès!')

        # Envoi d'un mail de bienvenu
        subject = "Bienvenu sur TechWork"
        message = "Bonjour " + user.first_name + "\n \n Bienvenue sur TechWork, votre plateforme de recrutement spécialisée dans les métiers de la technologie ! \n \n Trouvez votre prochaine opportunité professionnelle parmi nos offres d'emploi de premier plan. \n \n Explorez, postulez et faites avancer votre carrière dès aujourd'hui."
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)


        # Envoi d'un mail de confirmation
        current_site = get_current_site(request)
        email_subject = "Confirmation de compte"
        message_confirm = render_to_string("emailConfirm.html", {
            "name": user.first_name,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": generatorToken.make_token(user),
        })
        email = EmailMessage(
            email_subject,
            message_confirm,
            from_email,
            to_list,
        )
        email.send()
        messages.info(request, "Un email de confirmation a été envoyé à votre adresse. Veuillez vérifier votre boîte de réception.")
        return redirect('login')

    return render(request, 'app/register.html')

@csrf_protect
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        mot_de_passe = request.POST.get('mot_de_passe')
        user = authenticate(request, username=username, password=mot_de_passe)
        my_user=User.objects.get(username=username)
        if user is not None:
            login(request, user)
            prenom = user.first_name
            return render(request, 'app/index.html', {'prenom': prenom}) 
        elif my_user.is_active == False:
            messages.error(request, "Vous n'avez pas comfirmer votre email") 

        else:
            messages.error(request, 'Votre login est incorrect')
            return redirect('login')

    return render(request, 'app/login.html')

@csrf_protect
def user_logout(request):
    logout(request)
    messages.success(request, 'Votre compte a été déconnécté!')
    return redirect('home')

@csrf_protect
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        if user is not None and generatorToken.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Votre Compte a été activé")
            return redirect('login')
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
    return render(request, 'offres.html')
@csrf_protect
def temoignages(request):
    return render(request, 'temoignages.html')
@csrf_protect
def blog(request):
    return render(request, 'blog.html')
@csrf_protect
def apropos(request):
    return render(request, 'apropos.html')
@csrf_protect
def search(request):
    query = request.GET.get('query', '')
    # Perform search logic based on the query
    # Return the search results to a template
    return render(request, 'search_results.html', {'query': query})

