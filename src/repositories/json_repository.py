import json
from pathlib import Path


class JSONRepository:
    def __init__(self, nome_arquivo):
        self.caminho = Path(nome_arquivo)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)

    def salvar(self, dados):
        with self.caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

    def carregar(self):
        if not self.caminho.exists():
            return []

        with self.caminho.open("r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
