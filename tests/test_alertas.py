from datetime import date

from docs.Semana2.modelos import Categoria, Despesa, Receita
from src.models.orcamento_mensal import OrcamentoMensal
from src.services.configuracao_service import ConfiguracaoService


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
def test_alerta_deficit_orcamentario():
    categoria_receita = Categoria(nome="Salário", tipo="RECEITA")
    categoria_despesa = Categoria(nome="Alimentação", tipo="DESPESA")

    receita = Receita(
        valor=1000,
        categoria=categoria_receita,
        data=date(2026, 10, 5),
        descricao="Salário",
        forma_pagamento="Pix"
    )

    despesa = Despesa(
        valor=1500,
        categoria=categoria_despesa,
        data=date(2026, 10, 10),
        descricao="Compras",
        forma_pagamento="Cartão"
    )

    orcamento = OrcamentoMensal(10, 2026, 2000)
    orcamento.adicionarLancamento(receita)
    orcamento.adicionarLancamento(despesa)

    assert any(
        alerta.tipo == "DÉFICIT ORÇAMENTÁRIO"
        for alerta in orcamento.alertas
    )


def test_nao_duplicar_alerta_deficit():
    categoria_receita = Categoria(nome="Salário", tipo="RECEITA")
    categoria_despesa = Categoria(nome="Alimentação", tipo="DESPESA")

    receita = Receita(
        valor=1000,
        categoria=categoria_receita,
        data=date(2026, 10, 5),
        descricao="Salário",
        forma_pagamento="Pix"
    )

    despesa1 = Despesa(
        valor=1200,
        categoria=categoria_despesa,
        data=date(2026, 10, 10),
        descricao="Compra 1",
        forma_pagamento="Pix"
    )

    despesa2 = Despesa(
        valor=500,
        categoria=categoria_despesa,
        data=date(2026, 10, 15),
        descricao="Compra 2",
        forma_pagamento="Cartão"
    )

    orcamento = OrcamentoMensal(10, 2026, 2000)
    orcamento.adicionarLancamento(receita)
    orcamento.adicionarLancamento(despesa1)
    orcamento.adicionarLancamento(despesa2)

    quantidade = sum(
        alerta.tipo == "DÉFICIT ORÇAMENTÁRIO"
        for alerta in orcamento.alertas
    )

    assert quantidade == 1


def test_atualizar_alerta_deficit():
    categoria_receita = Categoria(nome="Salário", tipo="RECEITA")
    categoria_despesa = Categoria(nome="Alimentação", tipo="DESPESA")

    receita = Receita(
        valor=1000,
        categoria=categoria_receita,
        data=date(2026, 10, 5),
        descricao="Salário",
        forma_pagamento="Pix"
    )

    despesa1 = Despesa(
        valor=1200,
        categoria=categoria_despesa,
        data=date(2026, 10, 10),
        descricao="Compra 1",
        forma_pagamento="Pix"
    )

    despesa2 = Despesa(
        valor=500,
        categoria=categoria_despesa,
        data=date(2026, 10, 15),
        descricao="Compra 2",
        forma_pagamento="Cartão"
    )

    orcamento = OrcamentoMensal(10, 2026, 2000)
    orcamento.adicionarLancamento(receita)
    orcamento.adicionarLancamento(despesa1)

    alerta = next(
        alerta for alerta in orcamento.alertas
        if alerta.tipo == "DÉFICIT ORÇAMENTÁRIO"
    )

    orcamento.adicionarLancamento(despesa2)

    assert alerta.mensagem == "Saldo mensal negativo: R$ -700.00"


def test_remover_alerta_deficit_quando_saldo_positivo():
    categoria = Categoria(nome="Geral", tipo="DESPESA")
    categoria_receita = Categoria(nome="Salário", tipo="RECEITA")

    orcamento = OrcamentoMensal(10, 2026, 2000)

    receita_inicial = Receita(
        valor=1000,
        categoria=categoria_receita,
        data=date(2026, 10, 1),
        descricao="Salário inicial",
        forma_pagamento="Pix"
    )

    despesa = Despesa(
        valor=1500,
        categoria=categoria,
        data=date(2026, 10, 10),
        descricao="Compra",
        forma_pagamento="Pix"
    )

    receita_extra = Receita(
        valor=1000,
        categoria=categoria_receita,
        data=date(2026, 10, 20),
        descricao="Renda extra",
        forma_pagamento="Pix"
    )

    orcamento.adicionarLancamento(receita_inicial)
    orcamento.adicionarLancamento(despesa)

    assert any(
        alerta.tipo == "DÉFICIT ORÇAMENTÁRIO"
        for alerta in orcamento.alertas
    )

    orcamento.adicionarLancamento(receita_extra)

    assert not any(
        alerta.tipo == "DÉFICIT ORÇAMENTÁRIO"
        for alerta in orcamento.alertas
    )

def test_alerta_usa_limite_definido_na_configuracao():
    configuracao = ConfiguracaoService(caminho="settings.json")

    categoria = Categoria(nome="Eletrônicos", tipo="DESPESA")

    despesa = Despesa(
        valor=600,
        categoria=categoria,
        data=date(2026, 10, 10),
        descricao="Compra de celular",
        forma_pagamento="Cartão"
    )

    orcamento = OrcamentoMensal(
        10, 2026, 2000, configuracao=configuracao
    )

    orcamento.adicionarLancamento(despesa)

    assert any(
        alerta.tipo == "ALTO VALOR"
        for alerta in orcamento.alertas
    )


def test_despesa_abaixo_do_limite_configurado_nao_gera_alerta():
    configuracao = ConfiguracaoService(caminho="settings.json")

    categoria = Categoria(nome="Eletrônicos", tipo="DESPESA")

    despesa = Despesa(
        valor=400,
        categoria=categoria,
        data=date(2026, 10, 10),
        descricao="Compra de acessório",
        forma_pagamento="Pix"
    )

    orcamento = OrcamentoMensal(
        10, 2026, 2000, configuracao=configuracao
    )

    orcamento.adicionarLancamento(despesa)

    assert not any(
        alerta.tipo == "ALTO VALOR"
        for alerta in orcamento.alertas
    )