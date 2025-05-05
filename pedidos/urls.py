from django.urls import path
from .views import FinalizarCompraView, PedidoDetailView

app_name = 'pedidos'

urlpatterns = [
    path('finalizar/', FinalizarCompraView.as_view(), name='finalizar_compra'),
    path('<int:pk>/', PedidoDetailView.as_view(), name='pedido_detalhe'),
]