from pathlib import Path
from src.repositories.json_repository import JSONRepository


class ConfiguracaoService:
    def __init__(self, caminho=None):
        if caminho is None:
            caminho = Path(__file__).resolve().parents[2] / "settings.json"

        self.repositorio = JSONRepository(caminho)
        self.configuracoes = self.repositorio.carregar()

        self._validar_configuracoes()

    def _validar_configuracoes(self):
        campos_obrigatorios = (
            "limite_alto_valor",
            "meses_comparacao",
            "meta_economia_percentual"
        )

        if not isinstance(self.configuracoes, dict):
            raise ValueError("O arquivo de configurações deve conter um objeto JSON.")

        for campo in campos_obrigatorios:
            if campo not in self.configuracoes:
                raise ValueError(f"Configuração obrigatória ausente: {campo}.")

        limite = self.configuracoes["limite_alto_valor"]
        meses = self.configuracoes["meses_comparacao"]
        meta = self.configuracoes["meta_economia_percentual"]

        if isinstance(limite, bool) or not isinstance(limite, (int, float)) or limite <= 0:
            raise ValueError("O limite de alto valor deve ser um número positivo.")

        if isinstance(meses, bool) or not isinstance(meses, int) or meses < 1:
            raise ValueError("A quantidade de meses deve ser um inteiro positivo.")

        if isinstance(meta, bool) or not isinstance(meta, (int, float)) or not 0 <= meta <= 100:
            raise ValueError("A meta de economia deve estar entre 0 e 100.")

    def obter(self, chave):
        if chave not in self.configuracoes:
            raise KeyError(f"Configuração não encontrada: {chave}.")

        return self.configuracoes[chave]