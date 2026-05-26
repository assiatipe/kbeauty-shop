from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from products.views import home


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('recommendations/', include('recommendation.urls')),
    path('reviews/', include('reviews.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'kbeauty_shop.views.handler404'
handler500 = 'kbeauty_shop.views.handler500'