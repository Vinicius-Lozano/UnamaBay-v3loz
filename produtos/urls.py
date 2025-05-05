from django.urls import path
from .views import ListaProdutosView, AdicionarProdutoView, DetalheProdutoView, ExcluirProdutoView, EditarProdutoView

app_name = 'produtos'

urlpatterns = [
    path('', ListaProdutosView.as_view(), name='lista_produtos'),
    path('adicionar/', AdicionarProdutoView.as_view(), name='adicionar_produto'),
    path('<int:pk>/', DetalheProdutoView.as_view(), name='detalhe_produto'),
    path('<int:pk>/editar/', EditarProdutoView.as_view(), name='editar_produto'),
    path('<int:pk>/excluir/', ExcluirProdutoView.as_view(), name='excluir_produto'),
]