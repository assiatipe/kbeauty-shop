from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import InscriptionForm, ConnexionForm, ProfilForm, UserUpdateForm
from .models import ProfilClient
from orders.models import Commande


def inscription(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = InscriptionForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f'Bienvenue {user.first_name} ! Votre compte a été créé.'
            )
            return redirect('home')
    else:
        form = InscriptionForm()

    return render(request, 'accounts/inscription.html', {
        'form': form,
    })


def connexion(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(
                request,
                f'Bon retour, {user.first_name or user.username} !'
            )

            next_url = request.GET.get('next') or 'home'
            return redirect(next_url)

        messages.error(request, 'Identifiants incorrects.')
    else:
        form = ConnexionForm()

    return render(request, 'accounts/connexion.html', {
        'form': form,
    })


@require_POST
def deconnexion(request):
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('home')


@login_required
def profil(request):
    profil_client, created = ProfilClient.objects.get_or_create(
        user=request.user
    )

    commandes = Commande.objects.filter(
        client=request.user
    ).order_by('-date_commande')[:5]

    if request.method == 'POST':
        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        profil_form = ProfilForm(
            request.POST,
            request.FILES,
            instance=profil_client
        )

        if user_form.is_valid() and profil_form.is_valid():
            user_form.save()
            profil_form.save()
            messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('profil')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profil_form = ProfilForm(instance=profil_client)

    return render(request, 'accounts/profil.html', {
        'user_form': user_form,
        'profil_form': profil_form,
        'commandes': commandes,
    })