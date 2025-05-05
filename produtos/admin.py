from django.contrib import admin
from .models import Categoria, Produto

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nome', 'descricao')
    readonly_fields = ('criado_em', 'atualizado_em')
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Categoria)
admin.site.register(Produto, ProdutoAdmin)
