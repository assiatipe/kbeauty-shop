from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogue, name='catalogue'),
    path('<slug:slug>/', views.detail_produit, name='detail_produit'),
]
