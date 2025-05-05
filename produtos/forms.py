from django import forms
from .models import Produto, Categoria

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'estoque', 'categoria', 'imagem']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)

    def clean_preco(self):
        preco = self.cleaned_data.get('preco')
        if preco <= 0:
            raise forms.ValidationError("O preço deve ser maior que zero")
        return preco
    
    def clean_estoque(self):
        estoque = self.cleaned_data.get('estoque')
        if estoque < 0:
            raise forms.ValidationError("O estoque não pode ser negativo")
        return estoque