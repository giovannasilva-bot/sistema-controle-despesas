from datetime import date

import pytest

from src.models.orcamento_mensal import OrcamentoMensal
from docs.Semana2.modelos import Categoria, Receita, Despesa
from src.repositories.json_repository import JSONRepository
from src.services.relatorio_service import RelatorioService


def criar_lancamentos():
    categoria_receita = Categoria(nome="Salário", tipo="RECEITA")
    categoria_despesa = Categoria(
        nome="Alimentação",
        tipo="DESPESA",
        limite_mensal=800
    )

    receita = Receita(
        valor=3000,
        categoria=categoria_receita,
        data=date(2026, 10, 5),
        descricao="Salário",
        forma_pagamento="Pix"
    )

    despesa = Despesa(
        valor=500,
        categoria=categoria_despesa,
        data=date(2026, 10, 10),
        descricao="Compras do mês",
        forma_pagamento="Cartão"
    )

    return receita, despesa


def test_adicionar_lancamento_ao_orcamento():
    receita, despesa = criar_lancamentos()
    orcamento = OrcamentoMensal(10, 2026, 2000)

    orcamento.adicionarLancamento(receita)
    orcamento.adicionarLancamento(despesa)

    assert len(orcamento.lancamentos) == 2


def test_calcular_receitas():
    receita, despesa = criar_lancamentos()
    orcamento = OrcamentoMensal(10, 2026, 2000)

    orcamento.adicionarLancamento(receita)
    orcamento.adicionarLancamento(despesa)

    assert orcamento.calcularReceitas() == 3000


def test_calcular_despesas():
    receita, despesa = criar_lancamentos()
    orcamento = OrcamentoMensal(10, 2026, 2000)

    orcamento.adicionarLancamento(receita)
    orcamento.adicionarLancamento(despesa)

    assert orcamento.calcularDespesas() == 500


def test_calcular_saldo():
    receita, despesa = criar_lancamentos()
    orcamento = OrcamentoMensal(10, 2026, 2000)

    orcamento.adicionarLancamento(receita)
    orcamento.adicionarLancamento(despesa)

    assert orcamento.calcularSaldo() == 2500


def test_verificar_deficit():
    receita, despesa = criar_lancamentos()
    orcamento = OrcamentoMensal(10, 2026, 400)

    orcamento.adicionarLancamento(receita)
    orcamento.adicionarLancamento(despesa)

    assert orcamento.verificarDeficit() is True


def test_rejeitar_lancamento_de_outro_mes():
    categoria = Categoria(nome="Alimentação", tipo="DESPESA")

    despesa = Despesa(
        valor=100,
        categoria=categoria,
        data=date(2026, 9, 10),
        descricao="Compra",
        forma_pagamento="Pix"
    )

    orcamento = OrcamentoMensal(10, 2026, 2000)

    with pytest.raises(ValueError, match="mês e ano"):
        orcamento.adicionarLancamento(despesa)
#------------------------------------------------------------------------------------------------------------------



def test_gerar_relatorio_mensal():
    receita, despesa = criar_lancamentos()
    orcamento = OrcamentoMensal(10, 2026, 2000)

    orcamento.adicionarLancamento(receita)
    orcamento.adicionarLancamento(despesa)

    relatorio = RelatorioService.gerar_relatorio_mensal(orcamento)

    assert relatorio["receitas"] == 3000
    assert relatorio["despesas"] == 500
    assert relatorio["saldo"] == 2500
    assert relatorio["deficit"] is False


def test_gerar_despesas_por_categoria():
    receita, despesa = criar_lancamentos()
    orcamento = OrcamentoMensal(10, 2026, 2000)
    orcamento.adicionarLancamento(receita)
    orcamento.adicionarLancamento(despesa)

    resultado = RelatorioService.gerar_despesas_por_categoria(orcamento)

    assert resultado == {"Alimentação": 500}


def test_salvar_e_carregar_json(tmp_path):
    caminho = tmp_path / "orcamentos.json"
    repositorio = JSONRepository(caminho)

    dados = {
        "mes": 10,
        "ano": 2026,
        "receitas": 3000,
        "despesas": 500
    }

    repositorio.salvar(dados)
    resultado = repositorio.carregar()

    assert resultado == dados


def test_carregar_json_inexistente(tmp_path):
    caminho = tmp_path / "inexistente.json"
    repositorio = JSONRepository(caminho)

    assert repositorio.carregar() == []
