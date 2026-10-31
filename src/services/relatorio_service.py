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

    @staticmethod
    def gerar_percentuais_por_categoria(orcamento: OrcamentoMensal):
        despesas = RelatorioService.gerar_despesas_por_categoria(orcamento)
        total_despesas = orcamento.calcularDespesas()

        if total_despesas == 0:
            return {categoria: 0 for categoria in despesas}

        return {
            categoria: (valor / total_despesas) * 100
            for categoria, valor in despesas.items()
        }

    @staticmethod
    def gerar_top_categorias(orcamento: OrcamentoMensal, quantidade=5):
        despesas = RelatorioService.gerar_despesas_por_categoria(orcamento)

        return sorted(
            despesas.items(),
            key=lambda item: item[1],
            reverse=True
        )[:quantidade]

    @staticmethod
    def gerar_media_mensal(orcamentos: list[OrcamentoMensal]):
        if not orcamentos:
            raise ValueError("É necessário informar pelo menos um orçamento.")

        total_receitas = sum(
            orcamento.calcularReceitas() for orcamento in orcamentos
        )

        total_despesas = sum(
            orcamento.calcularDespesas() for orcamento in orcamentos
        )

        total_saldo = sum(
            orcamento.calcularSaldo() for orcamento in orcamentos
        )

        quantidade = len(orcamentos)

        return {
            "quantidade_meses": quantidade,
            "media_receitas": total_receitas / quantidade,
            "media_despesas": total_despesas / quantidade,
            "media_saldo": total_saldo / quantidade
        }

    @staticmethod
    def comparar_despesas(orcamento_atual: OrcamentoMensal,
                          orcamento_anterior: OrcamentoMensal):
        despesas_atuais = RelatorioService.gerar_despesas_por_categoria(
            orcamento_atual
        )

        despesas_anteriores = RelatorioService.gerar_despesas_por_categoria(
            orcamento_anterior
        )

        categorias = set(despesas_atuais) | set(despesas_anteriores)
        comparativo = {}

        for categoria in categorias:
            atual = despesas_atuais.get(categoria, 0)
            anterior = despesas_anteriores.get(categoria, 0)

            diferenca = atual - anterior

            if anterior == 0:
                percentual = 0 if atual == 0 else None
            else:
                percentual = (diferenca / anterior) * 100

            comparativo[categoria] = {
                "mes_anterior": anterior,
                "mes_atual": atual,
                "diferenca": diferenca,
                "variacao_percentual": percentual
            }

        return comparativo