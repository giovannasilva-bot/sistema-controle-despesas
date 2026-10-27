
from src.main import exibir_menu, ler_valor


def test_exibir_menu(capsys):
    exibir_menu()

    resultado = capsys.readouterr().out

    assert "CONTROLE DE DESPESAS" in resultado
    assert "Adicionar receita" in resultado
    assert "Adicionar despesa" in resultado
    assert "Listar lançamentos" in resultado
    assert "Salvar dados" in resultado
    assert "Sair sem salvar" in resultado


def test_ler_valor_positivo(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "150,50")

    assert ler_valor("Valor: R$ ") == 150.50


def test_ler_valor_rejeita_zero(monkeypatch, capsys):
    entradas = iter(["0", "50"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = ler_valor("Valor: R$ ")

    assert resultado == 50
    assert "maior que zero" in capsys.readouterr().out
