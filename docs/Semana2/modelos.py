
import uuid
from datetime import date

# ---------------------------------------------------------
# 1. DECORATOR CUSTOMIZADO 
# ---------------------------------------------------------
def log_operacao(funcao_original):
    """Decorator para registrar (log) a criação de lançamentos financeiros."""
    def embrulho(*args, **kwargs):
        print("\n" + "-"*50)
        print("[Log] 📝 Validando e registrando nova operação...")
        resultado = funcao_original(*args, **kwargs)
        print("[Log] ✅ Operação registrada com sucesso.")
        print("-"*50)
        return resultado
    return embrulho

# ---------------------------------------------------------
# 2. CLASSES DO SISTEMA (Com Encapsulamento)
# ---------------------------------------------------------

class Categoria:
    def __init__(self, nome, tipo, limite_mensal=None, descricao=""):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.tipo = tipo.upper()  # Força 'RECEITA' ou 'DESPESA'
        self.descricao = descricao
        
        self._limite_mensal = None
        # O '=' aciona o setter abaixo para validar a regra de negócio
        self.limite_mensal = limite_mensal

    @property
    def limite_mensal(self):
        return self._limite_mensal

    @limite_mensal.setter
    def limite_mensal(self, valor):
        """Regra: Categorias de receita não podem ter limite de gastos."""
        if self.tipo == "RECEITA" and valor is not None:
            raise ValueError("Categorias de receita não podem ter limite de gastos.")
        if valor is not None and valor < 0:
            raise ValueError("O limite mensal não pode ser negativo!")
        self._limite_mensal = valor

    def __str__(self):
        return f"{self.nome} ({self.tipo})"


class Lancamento:
    def __init__(self, valor, categoria, data, descricao, forma_pagamento):
        if not isinstance(categoria, Categoria):
            raise ValueError("Todo lançamento deve estar associado a uma Categoria válida.")
            
        self.id = str(uuid.uuid4())
        self.categoria = categoria
        self.data = data
        self.descricao = descricao
        self.forma_pagamento = forma_pagamento
        
        self._valor = 0
        # Aciona o setter para validar se o valor é maior que zero
        self.valor = valor

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, novo_valor):
        """Regra: Não é permitido cadastrar despesas/receitas com valor <= 0."""
        if novo_valor <= 0:
            raise ValueError("Não é permitido cadastrar lançamentos com valor <= 0.")
        self._valor = novo_valor

    # --- MÉTODOS ESPECIAIS OBRIGATÓRIOS ---
    
    def __str__(self):
        """Resumo legível para o usuário final"""
        return f"[{self.data}] {self.descricao}: R$ {self.valor:.2f} | Cat: {self.categoria.nome}"

    def __repr__(self):
        """Resumo técnico para debug"""
        return f"<{self.__class__.__name__} id={self.id[:8]} valor={self.valor}>"

    def __eq__(self, outro):
        """Compara dois lançamentos. São iguais se tiverem mesma data e descrição."""
        if not isinstance(outro, Lancamento):
            return False
        return self.data == outro.data and self.descricao == outro.descricao

    def __lt__(self, outro):
        """Permite ordenar listas por data usando '<'"""
        if self.data == outro.data:
            return self.valor < outro.valor
        return self.data < outro.data

    def __add__(self, outro):
        """Permite somar lançamentos do mesmo tipo usando '+'"""
        if type(self) == type(outro):
            return self.valor + outro.valor
        raise TypeError("Só é possível somar lançamentos do mesmo tipo.")


# ---------------------------------------------------------
# 3. HERANÇA
# ---------------------------------------------------------

class Receita(Lancamento):
    @log_operacao
    def __init__(self, valor, categoria, data, descricao, forma_pagamento="Dinheiro"):
        if categoria.tipo != "RECEITA":
            raise ValueError("Receitas exigem uma categoria do tipo RECEITA.")
        super().__init__(valor, categoria, data, descricao, forma_pagamento)


class Despesa(Lancamento):
    @log_operacao
    def __init__(self, valor, categoria, data, descricao, forma_pagamento):
        if categoria.tipo != "DESPESA":
            raise ValueError("Despesas exigem uma categoria do tipo DESPESA.")
        super().__init__(valor, categoria, data, descricao, forma_pagamento)








