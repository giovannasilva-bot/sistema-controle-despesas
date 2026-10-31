from abc import ABC, abstractmethod

from src.services.relatorio_service import RelatorioService


class EstrategiaRelatorio(ABC):

    @abstractmethod
    def gerar(self, orcamento):
        pass


class RelatorioMensalStrategy(EstrategiaRelatorio):

    def gerar(self, orcamento):
        return RelatorioService.gerar_relatorio_mensal(orcamento)


class DespesasPorCategoriaStrategy(EstrategiaRelatorio):

    def gerar(self, orcamento):
        return RelatorioService.gerar_despesas_por_categoria(orcamento)


class PercentuaisPorCategoriaStrategy(EstrategiaRelatorio):

    def gerar(self, orcamento):
        return RelatorioService.gerar_percentuais_por_categoria(orcamento)


class TopCategoriasStrategy(EstrategiaRelatorio):

    def gerar(self, orcamento):
        return RelatorioService.gerar_top_categorias(orcamento)