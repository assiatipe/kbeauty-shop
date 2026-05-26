from django.urls import path
from . import views

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('login/', views.connexion, name='login'),
    path('logout/', views.deconnexion, name='logout'),
    path('profil/', views.profil, name='profil'),
]
