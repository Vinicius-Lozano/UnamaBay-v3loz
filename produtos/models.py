from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    imagem = models.ImageField(upload_to='produtos/', null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.nome} (R${self.preco})"

    def diminuir_estoque(self, quantidade):
        if self.estoque >= quantidade:
            self.estoque -= quantidade
            self.save()
            return True
        return False   
    
    class Meta:
        permissions = [
            ("pode_adicionar_produto", "Pode adicionar novos produtos"),
        ]