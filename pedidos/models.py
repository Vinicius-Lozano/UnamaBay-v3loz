from django.db import models
from accounts.models import CustomUser
from produtos.models import Produto

class Pedido(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pagamento Pendente'),
        ('E', 'Em separação'),
        ('T', 'Em transporte'),
        ('C', 'Concluído'),
        ('X', 'Cancelado'),
    )
    
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')  
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
    
    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def get_subtotal(self):
        return self.quantidade * self.preco_unitario

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens dos Pedidos"

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"