from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.views.generic import DetailView
from cart.models import Cart
from produtos.models import Produto
from .models import Pedido, ItemPedido
from django.db import transaction

class FinalizarCompraView(LoginRequiredMixin, View):
    @transaction.atomic
    def post(self, request):
        try:
            cart = get_object_or_404(Cart, user=request.user)
            
            if not cart.items.exists():
                messages.warning(request, "Seu carrinho está vazio!")
                return redirect('cart:detail')
            
            pedido = Pedido.objects.create(
                usuario=request.user,
                total=cart.total
            )
            
            products_to_lock = [item.product.id for item in cart.items.all()]
            produtos = Produto.objects.select_for_update().filter(id__in=products_to_lock)
            
            for item in cart.items.select_related('product'):
                product = next(p for p in produtos if p.id == item.product.id)
                
                if item.quantity > product.estoque:
                    messages.error(request,
                        f"Estoque insuficiente para {product.nome}. Disponível: {product.estoque}")
                    raise Exception("Estoque insuficiente")
                
                ItemPedido.objects.create(
                    pedido=pedido,
                    produto=product,
                    quantidade=item.quantity,
                    preco_unitario=product.preco
                )
                
                product.estoque -= item.quantity
                product.save()
            
            cart.items.all().delete()
            messages.success(request, "Compra finalizada com sucesso!")
            return redirect('pedidos:pedido_detalhe', pk=pedido.pk)
            
        except Exception as e:
            if 'pedido' in locals():
                pedido.delete()
            messages.error(request, f"Erro ao processar pedido: {str(e)}")
            return redirect('cart:detail')

class PedidoDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'pedidos/detalhe.html'
    context_object_name = 'pedido'

    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user)