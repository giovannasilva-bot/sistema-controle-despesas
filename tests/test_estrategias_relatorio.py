
from datetime import date

from docs.Semana2.modelos import Categoria, Receita, Despesa
from src.models.orcamento_mensal import OrcamentoMensal
from src.services.relatorio_service import RelatorioService
from src.services.estrategias_relatorio import (
    RelatorioMensalStrategy,
    DespesasPorCategoriaStrategy,
    PercentuaisPorCategoriaStrategy,
    TopCategoriasStrategy
)


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


def test_strategy_relatorio_mensal():
    orcamento = criar_orcamento_outubro()

    resultado = RelatorioService.gerar_com_estrategia(
        RelatorioMensalStrategy(), orcamento
    )

    assert resultado["receitas"] == 3000
    assert resultado["despesas"] == 800


def test_strategy_despesas_por_categoria():
    orcamento = criar_orcamento_outubro()

    resultado = RelatorioService.gerar_com_estrategia(
        DespesasPorCategoriaStrategy(), orcamento
    )

    assert resultado["Alimentação"] == 500
    assert resultado["Transporte"] == 300


def test_strategy_percentuais():
    orcamento = criar_orcamento_outubro()

    resultado = RelatorioService.gerar_com_estrategia(
        PercentuaisPorCategoriaStrategy(), orcamento
    )

    assert resultado["Alimentação"] == 62.5
    assert resultado["Transporte"] == 37.5


def test_strategy_top_categorias():
    orcamento = criar_orcamento_outubro()

    resultado = RelatorioService.gerar_com_estrategia(
        TopCategoriasStrategy(), orcamento
    )

    assert resultado[0] == ("Alimentação", 500)
    assert resultado[1] == ("Transporte", 300)
