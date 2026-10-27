
from datetime import date

from docs.Semana2.modelos import Categoria, Despesa
from src.models.orcamento_mensal import OrcamentoMensal


def test_alerta_despesa_acima_de_500():
    categoria = Categoria(nome="Eletrônicos", tipo="DESPESA")

    despesa = Despesa(
        valor=600,
        categoria=categoria,
        data=date(2026, 10, 10),
        descricao="Compra de celular",
        forma_pagamento="Cartão"
    )

    orcamento = OrcamentoMensal(10, 2026, 2000)
    orcamento.adicionarLancamento(despesa)

    assert any(
        alerta.tipo == "ALTO VALOR"
        for alerta in orcamento.alertas
    )


def test_alerta_limite_mensal_excedido():
    categoria = Categoria(
        nome="Alimentação",
        tipo="DESPESA",
        limite_mensal=300
    )

    despesa = Despesa(
        valor=350,
        categoria=categoria,
        data=date(2026, 10, 15),
        descricao="Compras do mês",
        forma_pagamento="Pix"
    )

    orcamento = OrcamentoMensal(10, 2026, 2000)
    orcamento.adicionarLancamento(despesa)

    assert any(
        alerta.tipo == "LIMITE EXCEDIDO"
        for alerta in orcamento.alertas
    )
