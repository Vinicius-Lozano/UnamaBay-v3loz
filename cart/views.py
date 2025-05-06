from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Cart, CartItem
from .forms import CartAddForm, CartUpdateForm
from produtos.models import Produto
from django.db.models import Sum
from django.db import transaction


class CartDetailView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = 'cart/detail.html'
    context_object_name = 'cart'

    def get_object(self):
        return get_object_or_404(Cart, user=self.request.user)

class CartAddView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = Cart.objects.get_or_create(user=request.user)[0]
        product = get_object_or_404(Produto, id=product_id)
        form = CartAddForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            quantity = cd['quantity']
            
            
            existing_quantity = cart.items.filter(product=product).aggregate(
                Sum('quantity'))['quantity__sum'] or 0
            
            if (existing_quantity + quantity) > product.estoque:
                messages.error(request, 
                    f"Estoque insuficiente. Disponível: {product.estoque - existing_quantity}")
                return redirect('produtos:detalhe_produto', pk=product_id)

            item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                if (item.quantity + quantity) > product.estoque:
                    messages.error(request,
                        f"Estoque insuficiente após atualização. Disponível: {product.estoque - item.quantity}")
                    return redirect('cart:detail')
                
                item.quantity += quantity
                item.save()
                msg = f"Quantidade de {product.nome} atualizada!"
            else:
                msg = f"{product.nome} adicionado ao carrinho!"
                
            messages.success(request, msg)

        return redirect('cart:detail')

class CartUpdateView(LoginRequiredMixin, UpdateView):
    model = CartItem  
    form_class = CartUpdateForm
    template_name = 'cart/update.html'
    success_url = reverse_lazy('cart:detail')

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'quantity': self.object.quantity}
        kwargs.pop('instance', None)
        return kwargs

    def form_valid(self, form):
        new_quantity = form.cleaned_data['quantity']
        product = self.object.product
        
        with transaction.atomic():
            product = Produto.objects.select_for_update().get(pk=product.id)
            
            if new_quantity > product.estoque:
                messages.error(self.request,
                    f"Estoque insuficiente. Disponível: {product.estoque}")
                return redirect('cart:detail')
            
            self.object.quantity = new_quantity
            self.object.save()
        
        messages.success(self.request, "Quantidade atualizada com sucesso!")
        return redirect(self.success_url)

class CartRemoveView(LoginRequiredMixin, DeleteView):
    model = CartItem
    success_url = reverse_lazy('cart:detail')
    template_name = 'cart/confirm_remove.html'

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Item removido do carrinho!")
        return super().delete(request, *args, **kwargs)