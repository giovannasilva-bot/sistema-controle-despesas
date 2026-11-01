from docs.Semana2.modelos import Receita, Despesa
from src.models.alerta import Alerta
from src.services.configuracao_service import ConfiguracaoService


class OrcamentoMensal:
    def __init__(self, mes, ano, orcamento_total, configuracao=None):
        if mes < 1 or mes > 12:
            raise ValueError("O mês deve estar entre 1 e 12.")

        if ano < 1:
            raise ValueError("O ano deve ser válido.")

        if orcamento_total < 0:
            raise ValueError("O orçamento total não pode ser negativo.")

        self.mes = mes
        self.ano = ano
        self.orcamento_total = orcamento_total
        self.lancamentos = []
        self.alertas = []
        self.configuracao = (
    configuracao if configuracao is not None else ConfiguracaoService()
)


    def adicionarLancamento(self, lancamento):
        if not isinstance(lancamento, (Receita, Despesa)):
            raise ValueError("O lançamento deve ser uma Receita ou Despesa.")

        if lancamento.data.month != self.mes or lancamento.data.year != self.ano:
            raise ValueError("O lançamento deve pertencer ao mês e ano do orçamento.")

        self.lancamentos.append(lancamento)
        self.atualizarAlertaDeficit()

        if isinstance(lancamento, Despesa):
            limite_alto_valor = self.configuracao.obter("limite_alto_valor")
            if lancamento.valor > limite_alto_valor:
                self.alertas.append(
                    Alerta(
                        "ALTO VALOR",
                       f"Despesa acima de R$ {limite_alto_valor:.2f}: R$ {lancamento.valor:.2f}", 
                        lancamento.data,
                        lancamento
                    )
                )

            limite = lancamento.categoria.limite_mensal

            if limite is not None:
                total_categoria = sum(
                    item.valor
                    for item in self.lancamentos
                    if isinstance(item, Despesa)
                    and item.categoria.nome == lancamento.categoria.nome
                    and item.categoria.tipo == lancamento.categoria.tipo
                )

                if total_categoria > limite:
                    self.alertas.append(
                        Alerta(
                            "LIMITE EXCEDIDO",
                            f"Limite da categoria {lancamento.categoria.nome} excedido: "
                            f"R$ {total_categoria:.2f} de R$ {limite:.2f}",
                            lancamento.data,
                            lancamento
                        )
                    )


    def calcularReceitas(self):
        return sum(
            lancamento.valor
            for lancamento in self.lancamentos
            if isinstance(lancamento, Receita)
        )

    def calcularDespesas(self):
        return sum(
            lancamento.valor
            for lancamento in self.lancamentos
            if isinstance(lancamento, Despesa)
        )

    def calcularSaldo(self):
        return self.calcularReceitas() - self.calcularDespesas()

    def verificarDeficit(self):
        return self.calcularSaldo() < 0
    def atualizarAlertaDeficit(self):
        alerta_deficit = next(
            (
                alerta for alerta in self.alertas
                if alerta.tipo == "DÉFICIT ORÇAMENTÁRIO"
            ),
            None
        )

        if self.verificarDeficit():
            if alerta_deficit is None:
                self.alertas.append(
                    Alerta(
                        "DÉFICIT ORÇAMENTÁRIO",
                        f"Saldo mensal negativo: R$ {self.calcularSaldo():.2f}"
                    )
                )
            else:
                alerta_deficit.mensagem = (
                    f"Saldo mensal negativo: R$ {self.calcularSaldo():.2f}"
                )
        elif alerta_deficit is not None:
            self.alertas.remove(alerta_deficit)
    def __str__(self):
        return (
            f"Orçamento {self.mes:02d}/{self.ano} | "
            f"Receitas: R$ {self.calcularReceitas():.2f} | "
            f"Despesas: R$ {self.calcularDespesas():.2f} | "
            f"Saldo: R$ {self.calcularSaldo():.2f}"
        )
