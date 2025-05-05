from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from produtos.views import HomeView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),  
    path('accounts/', include('accounts.urls')),
    path('produtos/', include('produtos.urls')),
    path('carrinho/', include('cart.urls')),
    path('pedidos/', include('pedidos.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)