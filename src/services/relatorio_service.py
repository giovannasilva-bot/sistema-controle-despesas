from src.models.orcamento_mensal import OrcamentoMensal


class RelatorioService:
    @staticmethod
    def gerar_relatorio_mensal(orcamento: OrcamentoMensal):
        receitas = orcamento.calcularReceitas()
        despesas = orcamento.calcularDespesas()
        saldo = orcamento.calcularSaldo()

        return {
            "mes": orcamento.mes,
            "ano": orcamento.ano,
            "orcamento_total": orcamento.orcamento_total,
            "receitas": receitas,
            "despesas": despesas,
            "saldo": saldo,
            "deficit": orcamento.verificarDeficit()
        }

    @staticmethod
    def gerar_despesas_por_categoria(orcamento: OrcamentoMensal):
        despesas_por_categoria = {}

        for lancamento in orcamento.lancamentos:
            if lancamento.categoria.tipo == "DESPESA":
                categoria = lancamento.categoria.nome

                if categoria not in despesas_por_categoria:
                    despesas_por_categoria[categoria] = 0

                despesas_por_categoria[categoria] += lancamento.valor

        return despesas_por_categoria

    @staticmethod
    def exibir_relatorio_mensal(orcamento: OrcamentoMensal):
        relatorio = RelatorioService.gerar_relatorio_mensal(orcamento)

        print(f"\nRELATÓRIO FINANCEIRO - {relatorio['mes']:02d}/{relatorio['ano']}")
        print("-" * 40)
        print(f"Orçamento total: R$ {relatorio['orcamento_total']:.2f}")
        print(f"Receitas:        R$ {relatorio['receitas']:.2f}")
        print(f"Despesas:        R$ {relatorio['despesas']:.2f}")
        print(f"Saldo:           R$ {relatorio['saldo']:.2f}")
        print(f"Déficit:         {'Sim' if relatorio['deficit'] else 'Não'}")

    @staticmethod
    def exibir_despesas_por_categoria(orcamento: OrcamentoMensal):
        despesas = RelatorioService.gerar_despesas_por_categoria(orcamento)

        print("\nDESPESAS POR CATEGORIA")
        print("-" * 40)

        if not despesas:
            print("Nenhuma despesa cadastrada.")
            return

        for categoria, valor in despesas.items():
            print(f"{categoria}: R$ {valor:.2f}")
