from datetime import date

from docs.Semana2.modelos import Categoria, Receita, Despesa
from src.models.orcamento_mensal import OrcamentoMensal
from src.services.relatorio_service import RelatorioService



def criar_orcamento_outubro():
    orcamento = OrcamentoMensal(10, 2026, 2000)

    salario = Categoria("Salário", "RECEITA")
    alimentacao = Categoria("Alimentação", "DESPESA")
    transporte = Categoria("Transporte", "DESPESA")

    orcamento.adicionarLancamento(
        Receita(3000, salario, date(2026, 10, 5), "Salário", "Pix")
    )

    orcamento.adicionarLancamento(
        Despesa(500, alimentacao, date(2026, 10, 10), "Compras", "Cartão")
    )

    orcamento.adicionarLancamento(
        Despesa(300, transporte, date(2026, 10, 15), "Ônibus", "Dinheiro")
    )

    return orcamento


def criar_orcamento_novembro():
    orcamento = OrcamentoMensal(11, 2026, 2000)

    salario = Categoria("Salário", "RECEITA")
    alimentacao = Categoria("Alimentação", "DESPESA")
    lazer = Categoria("Lazer", "DESPESA")

    orcamento.adicionarLancamento(
        Receita(3500, salario, date(2026, 11, 5), "Salário", "Pix")
    )

    orcamento.adicionarLancamento(
        Despesa(600, alimentacao, date(2026, 11, 10), "Compras", "Cartão")
    )

    orcamento.adicionarLancamento(
        Despesa(200, lazer, date(2026, 11, 15), "Passeio", "Pix")
    )

    return orcamento


def test_gerar_percentuais_por_categoria():
    orcamento = criar_orcamento_outubro()

    resultado = RelatorioService.gerar_percentuais_por_categoria(orcamento)

    assert resultado["Alimentação"] == 62.5
    assert resultado["Transporte"] == 37.5


def test_gerar_top_categorias():
    orcamento = criar_orcamento_outubro()

    resultado = RelatorioService.gerar_top_categorias(orcamento, 2)

    assert resultado == [
        ("Alimentação", 500),
        ("Transporte", 300)
    ]


def test_gerar_media_mensal():
    outubro = criar_orcamento_outubro()
    novembro = criar_orcamento_novembro()

    resultado = RelatorioService.gerar_media_mensal(
        [outubro, novembro]
    )

    assert resultado["quantidade_meses"] == 2
    assert resultado["media_receitas"] == 3250
    assert resultado["media_despesas"] == 800
    assert resultado["media_saldo"] == 2450


def test_comparar_despesas():
    outubro = criar_orcamento_outubro()
    novembro = criar_orcamento_novembro()

    resultado = RelatorioService.comparar_despesas(
        novembro, outubro
    )

    assert resultado["Alimentação"]["mes_anterior"] == 500
    assert resultado["Alimentação"]["mes_atual"] == 600
    assert resultado["Alimentação"]["diferenca"] == 100
    assert resultado["Alimentação"]["variacao_percentual"] == 20

    assert resultado["Transporte"]["variacao_percentual"] == -100
    assert resultado["Lazer"]["variacao_percentual"] is None


def test_media_mensal_sem_orcamentos():
    try:
        RelatorioService.gerar_media_mensal([])
        assert False, "Deveria gerar um erro."
    except ValueError:
        assert True


