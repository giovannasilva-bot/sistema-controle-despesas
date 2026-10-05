import pytest
from datetime import date
from modelos import Categoria, Receita, Despesa

def test_criar_categoria_receita_com_limite_gera_erro():
    """Valida se o sistema impede categorias de receita com limite de gastos"""
    with pytest.raises(ValueError, match="Categorias de receita não podem ter limite"):
        Categoria(nome="Salário", tipo="RECEITA", limite_mensal=5000)

def test_lancamento_com_valor_negativo_gera_erro():
    """Valida se o sistema barra lançamentos com valor <= 0"""
    cat_alimentacao = Categoria(nome="Alimentação", tipo="DESPESA")
    
    with pytest.raises(ValueError, match="valor <= 0"):
        Despesa(-50, cat_alimentacao, date.today(), "Almoço", "PIX")

def test_soma_de_lancamentos_metodo_add():
    """Testa se o método mágico __add__ consegue somar duas despesas"""
    cat_transporte = Categoria(nome="Transporte", tipo="DESPESA")
    d1 = Despesa(15.50, cat_transporte, date.today(), "Uber ida", "PIX")
    d2 = Despesa(20.00, cat_transporte, date.today(), "Uber volta", "PIX")
    
    total = d1 + d2
    assert total == 35.50

def test_igualdade_de_lancamentos_metodo_eq():
    """Testa se o método mágico __eq__ compara corretamente pela data e descrição"""
    cat_freela = Categoria("Freelance", "RECEITA")
    data_hoje = date.today()
    
    r1 = Receita(500, cat_freela, data_hoje, "Site Cliente X")
    r2 = Receita(500, cat_freela, data_hoje, "Site Cliente X")
    
    assert r1 == r2  # Devem ser iguais pois têm a mesma data e descrição

