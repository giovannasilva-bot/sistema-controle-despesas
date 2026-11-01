from src.models.orcamento_mensal import OrcamentoMensal
from docs.Semana2.modelos import Despesa
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


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
    def gerar_com_estrategia(estrategia, orcamento):
        return estrategia.gerar(orcamento)

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
    def gerar_despesas_por_forma_pagamento(orcamento: OrcamentoMensal):
        despesas_por_forma = {}

        for lancamento in orcamento.lancamentos:
            if isinstance(lancamento, Despesa):
                forma = lancamento.forma_pagamento

                if forma not in despesas_por_forma:
                    despesas_por_forma[forma] = 0

                despesas_por_forma[forma] += lancamento.valor

        return despesas_por_forma

    @staticmethod
    def exibir_relatorio_mensal(orcamento: OrcamentoMensal):
        relatorio = RelatorioService.gerar_relatorio_mensal(orcamento)

        conteudo = (
            f"[bold]Orçamento total:[/bold] R$ {relatorio['orcamento_total']:.2f}\n"
            f"[bold]Receitas:[/bold]        R$ {relatorio['receitas']:.2f}\n"
            f"[bold]Despesas:[/bold]        R$ {relatorio['despesas']:.2f}\n"
            f"[bold]Saldo:[/bold]           R$ {relatorio['saldo']:.2f}\n"
            f"[bold]Déficit:[/bold]         {'Sim' if relatorio['deficit'] else 'Não'}"
        )

        console.print(
            Panel(
                conteudo,
                title=f"Relatório financeiro - {relatorio['mes']:02d}/{relatorio['ano']}",
                border_style="blue"
            )
        )

    @staticmethod
    def exibir_despesas_por_categoria(orcamento: OrcamentoMensal):
        despesas = RelatorioService.gerar_despesas_por_categoria(orcamento)

        if not despesas:
            console.print("[yellow]Nenhuma despesa cadastrada.[/yellow]")
            return

        tabela = Table(title="Despesas por categoria")

        tabela.add_column("Categoria", style="cyan")
        tabela.add_column("Valor", justify="right", style="green")

        for categoria, valor in despesas.items():
            tabela.add_row(categoria, f"R$ {valor:.2f}")

        console.print(tabela)
        
    @staticmethod
    def exibir_despesas_por_forma_pagamento(orcamento: OrcamentoMensal):
        despesas = RelatorioService.gerar_despesas_por_forma_pagamento(
            orcamento
        )

        if not despesas:
            console.print("[yellow]Nenhuma despesa cadastrada.[/yellow]")
            return

        tabela = Table(title="Despesas por forma de pagamento")

        tabela.add_column("Forma de pagamento", style="cyan")
        tabela.add_column("Valor", justify="right", style="green")

        for forma, valor in despesas.items():
            tabela.add_row(forma, f"R$ {valor:.2f}")

        console.print(tabela)

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