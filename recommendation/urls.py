from django.urls import path
from . import views

urlpatterns = [
    path('<int:produit_id>/', views.recommandations_produit, name='recommandations_produit'),
    path('chatbot/', views.chatbot_page, name='chatbot'),
    path('chatbot/api/', views.chatbot_api, name='chatbot_api'),
]
