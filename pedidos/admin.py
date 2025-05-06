from django.contrib import admin
from .models import Pedido, ItemPedido

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0  
    readonly_fields = ('produto', 'quantidade', 'preco_unitario')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'total', 'status', 'criado_em')
    list_filter = ('status', 'criado_em')
    search_fields = ('usuario__username', 'id')
    inlines = [ItemPedidoInline]
    readonly_fields = ('criado_em', 'atualizado_em')

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'produto', 'quantidade', 'preco_unitario')
    search_fields = ('pedido__id', 'produto__nome')