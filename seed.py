import json
from pathlib import Path


RAIZ_PROJETO = Path(__file__).resolve().parent
CAMINHO_SETTINGS = RAIZ_PROJETO / "settings.json"
CAMINHO_DADOS = RAIZ_PROJETO / "data" / "orcamento.json"


CONFIGURACOES_PADRAO = {
    "limite_alto_valor": 500.00,
    "meses_comparacao": 3,
    "meta_economia_percentual": 10
}


DADOS_DEMO = [
    {
        "mes": 10,
        "ano": 2026,
        "orcamento_total": 2500.0,
        "lancamentos": [
            {
                "tipo": "RECEITA",
                "valor": 3000.0,
                "data": "2026-10-05",
                "descricao": "Salário",
                "forma_pagamento": "Pix",
                "categoria": {
                    "nome": "Salário",
                    "tipo": "RECEITA",
                    "limite_mensal": None,
                    "descricao": ""
                }
            },
            {
                "tipo": "DESPESA",
                "valor": 350.0,
                "data": "2026-10-08",
                "descricao": "Compras do mês",
                "forma_pagamento": "Cartão",
                "categoria": {
                    "nome": "Alimentação",
                    "tipo": "DESPESA",
                    "limite_mensal": 600.0,
                    "descricao": "Despesas com alimentação"
                }
            },
            {
                "tipo": "DESPESA",
                "valor": 180.0,
                "data": "2026-10-12",
                "descricao": "Transporte",
                "forma_pagamento": "Pix",
                "categoria": {
                    "nome": "Transporte",
                    "tipo": "DESPESA",
                    "limite_mensal": 300.0,
                    "descricao": "Despesas com transporte"
                }
            },
            {
                "tipo": "DESPESA",
                "valor": 550.0,
                "data": "2026-10-20",
                "descricao": "Compra de equipamento",
                "forma_pagamento": "Cartão",
                "categoria": {
                    "nome": "Eletrônicos",
                    "tipo": "DESPESA",
                    "limite_mensal": 1000.0,
                    "descricao": "Equipamentos e acessórios"
                }
            }
        ]
    },
    {
        "mes": 11,
        "ano": 2026,
        "orcamento_total": 2500.0,
        "lancamentos": [
            {
                "tipo": "RECEITA",
                "valor": 3000.0,
                "data": "2026-11-05",
                "descricao": "Salário",
                "forma_pagamento": "Pix",
                "categoria": {
                    "nome": "Salário",
                    "tipo": "RECEITA",
                    "limite_mensal": None,
                    "descricao": ""
                }
            },
            {
                "tipo": "DESPESA",
                "valor": 420.0,
                "data": "2026-11-08",
                "descricao": "Compras do mês",
                "forma_pagamento": "Cartão",
                "categoria": {
                    "nome": "Alimentação",
                    "tipo": "DESPESA",
                    "limite_mensal": 600.0,
                    "descricao": "Despesas com alimentação"
                }
            },
            {
                "tipo": "DESPESA",
                "valor": 200.0,
                "data": "2026-11-15",
                "descricao": "Transporte",
                "forma_pagamento": "Pix",
                "categoria": {
                    "nome": "Transporte",
                    "tipo": "DESPESA",
                    "limite_mensal": 300.0,
                    "descricao": "Despesas com transporte"
                }
            },
            {
                "tipo": "DESPESA",
                "valor": 120.0,
                "data": "2026-11-22",
                "descricao": "Lazer",
                "forma_pagamento": "Dinheiro",
                "categoria": {
                    "nome": "Lazer",
                    "tipo": "DESPESA",
                    "limite_mensal": 300.0,
                    "descricao": "Despesas de lazer"
                }
            }
        ]
    },
    {
        "mes": 12,
        "ano": 2026,
        "orcamento_total": 2500.0,
        "lancamentos": [
            {
                "tipo": "RECEITA",
                "valor": 3000.0,
                "data": "2026-12-05",
                "descricao": "Salário",
                "forma_pagamento": "Pix",
                "categoria": {
                    "nome": "Salário",
                    "tipo": "RECEITA",
                    "limite_mensal": None,
                    "descricao": ""
                }
            },
            {
                "tipo": "DESPESA",
                "valor": 500.0,
                "data": "2026-12-08",
                "descricao": "Compras do mês",
                "forma_pagamento": "Cartão",
                "categoria": {
                    "nome": "Alimentação",
                    "tipo": "DESPESA",
                    "limite_mensal": 600.0,
                    "descricao": "Despesas com alimentação"
                }
            },
            {
                "tipo": "DESPESA",
                "valor": 250.0,
                "data": "2026-12-15",
                "descricao": "Transporte",
                "forma_pagamento": "Pix",
                "categoria": {
                    "nome": "Transporte",
                    "tipo": "DESPESA",
                    "limite_mensal": 300.0,
                    "descricao": "Despesas com transporte"
                }
            },
            {
                "tipo": "DESPESA",
                "valor": 700.0,
                "data": "2026-12-20",
                "descricao": "Compra de equipamento",
                "forma_pagamento": "Cartão",
                "categoria": {
                    "nome": "Eletrônicos",
                    "tipo": "DESPESA",
                    "limite_mensal": 1000.0,
                    "descricao": "Equipamentos e acessórios"
                }
            }
        ]
    }
]


def criar_settings():
    if CAMINHO_SETTINGS.exists():
        print("settings.json já existe. Mantido.")
        return

    with CAMINHO_SETTINGS.open("w", encoding="utf-8") as arquivo:
        json.dump(
            CONFIGURACOES_PADRAO,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

    print("settings.json criado.")


def criar_dados_demo():
    CAMINHO_DADOS.parent.mkdir(parents=True, exist_ok=True)

    if CAMINHO_DADOS.exists():
        print("data/orcamento.json já existe. Mantido.")
        return

    with CAMINHO_DADOS.open("w", encoding="utf-8") as arquivo:
        json.dump(
            DADOS_DEMO,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

    print("data/orcamento.json criado com dados de demonstração.")


def main():
    print("=== SEED DO SISTEMA ===")
    criar_settings()
    criar_dados_demo()
    print("Seed finalizado.")


if __name__ == "__main__":
    main()