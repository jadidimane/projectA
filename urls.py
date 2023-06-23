from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name="home"),
    path('Candidate_register/', views.Candidate_register_view, name="register_candidate"),
    path('Candidate_login/', views.candidat_login, name="login_candidate"),
    path('Agent_register/', views.Agent_register_view, name="register_agent"),
    path('Agent_login/', views.agent_login, name="login_agent"),

    path('logout/', views.user_logout, name='logout'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('acceuil/', views.acceuil, name='acceuil'),
    path('offres/', views.offres, name='offres'),
    path('temoignages/', views.temoignages, name='temoignages'),
    
    path('apropos/', views.apropos, name='apropos'),
    
]