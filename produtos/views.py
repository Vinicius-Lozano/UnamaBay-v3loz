from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Produto, Categoria
from .forms import ProdutoForm
from django.contrib import messages

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = Produto.objects.all().order_by('criado_em')[:6]  
        print(context['produtos'])  
        return context

class ListaProdutosView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'produtos/lista.html'
    context_object_name = 'produtos'
    paginate_by = 12
    ordering = ['-criado_em']  
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        
        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(categoria__id=categoria_id)
            
        
        busca = self.request.GET.get('q')
        if busca:
            queryset = queryset.filter(nome__icontains=busca)
            
        return queryset.select_related('categoria')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context

class AdicionarProdutoView(PermissionRequiredMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'produtos/adicionar.html'
    success_url = reverse_lazy('produtos:lista_produtos')
    permission_required = 'produtos.pode_adicionar_produto'
    
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        messages.success(self.request, 'Produto adicionado com sucesso!')
        return super().form_valid(form)
    

class DetalheProdutoView(LoginRequiredMixin, DetailView):
    model = Produto
    template_name = 'produtos/detalhe.html'
    context_object_name = 'produto'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        
        produto = self.get_object()
        context['disponivel'] = produto.estoque > 0
        context['estoque_baixo'] = produto.estoque < 10
        
        
        context['pode_editar'] = (
            self.request.user.has_perm('produtos.pode_adicionar_produto') or
            self.request.user == produto.criado_por
        )
        
        return context

class EditarProdutoView(PermissionRequiredMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'produtos/editar.html'
    success_url = reverse_lazy('produtos:lista_produtos')
    permission_required = 'produtos.pode_adicionar_produto'
    
    def form_valid(self, form):
        messages.success(self.request, 'Produto atualizado com sucesso!')
        return super().form_valid(form)

class ExcluirProdutoView(PermissionRequiredMixin, DeleteView):
    model = Produto
    success_url = reverse_lazy('produtos:lista_produtos')
    permission_required = 'produtos.pode_adicionar_produto'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Produto excluído com sucesso!')
        return super().delete(request, *args, **kwargs)