# Generated by Django 5.2 on 2025-04-26 20:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estoque', models.PositiveIntegerField()),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='produtos/')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='produtos.categoria')),
                ('criado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('pode_adicionar_produto', 'Pode adicionar novos produtos')],
            },
        ),
    ]
