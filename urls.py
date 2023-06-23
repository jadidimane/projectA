from django.urls import path
from .views import new_offer,job_offer_list,delete_offer,update_offer,detail_offre,detail_offre2,job_offer_list1
urlpatterns = [
    path('new_offer/', new_offer, name="new_offer"),
    path('job_offer_list/', job_offer_list, name="job_offers"),
    path('delete_offer/<int:id>', delete_offer, name="delete_offer"),
    path('update_offer/<int:id>', update_offer, name="edit_offer"),
    path('offre/<int:id>', detail_offre , name="offer"),
    path('offre2/<int:id>', detail_offre2 , name="postuler_offre"),
    path('job_offer_list1/', job_offer_list1 , name="liste_pour_visiteurs"),


]