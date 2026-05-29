from django.urls import path
from . import views

urlpatterns = [
    path('valider/', views.valider_commande, name='valider_commande'),
    path('confirmation/<int:commande_id>/', views.confirmation_commande, name='confirmation_commande'),
    path('historique/', views.historique_commandes, name='historique_commandes'),
    path('api/recent/', views.recent_purchases_api, name='recent_purchases_api'),
    path('<int:commande_id>/', views.detail_commande, name='detail_commande'),
    path('<int:commande_id>/action/<str:action>/', views.client_action_commande, name='client_action_commande'),
]
