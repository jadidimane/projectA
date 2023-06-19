from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register_view, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name='logout'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('acceuil/', views.acceuil, name='acceuil'),
    path('search/', views.search, name='search'),
    path('offres/', views.offres, name='offres'),
    path('temoignages/', views.temoignages, name='temoignages'),
    path('blog/', views.blog, name='blog'),
    path('apropos/', views.apropos, name='apropos'),
    
]
