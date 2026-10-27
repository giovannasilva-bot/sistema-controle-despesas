
from datetime import date


class Alerta:
    def __init__(self, tipo, mensagem, data=None, lancamento=None):
        tipos_validos = (
            "ALTO VALOR",
            "LIMITE EXCEDIDO",
            "DÉFICIT ORÇAMENTÁRIO"
        )

        if tipo not in tipos_validos:
            raise ValueError("Tipo de alerta inválido.")

        if not mensagem or not mensagem.strip():
            raise ValueError("A mensagem do alerta não pode ser vazia.")

        self.tipo = tipo
        self.mensagem = mensagem
        self.data = data if data is not None else date.today()
        self.lancamento = lancamento

    def __str__(self):
        return f"[{self.tipo}] {self.mensagem}"

    def __repr__(self):
        return (
            f"Alerta(tipo={self.tipo!r}, "
            f"mensagem={self.mensagem!r}, "
            f"data={self.data!r})"
        )
