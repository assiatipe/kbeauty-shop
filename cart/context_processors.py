from .models import Panier

def cart_count(request):
    if request.user.is_authenticated:
        try:
            panier = Panier.objects.get(client=request.user)
            return {'cart_count': panier.nombre_articles}
        except Panier.DoesNotExist:
            pass
    return {'cart_count': 0}
