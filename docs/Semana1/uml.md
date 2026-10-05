# UML Textual — Sistema de Controle de Despesas Pessoais

## 1. Classe Lancamento

**Responsabilidade:** representar uma movimentação financeira genérica do sistema.

### Atributos

* `id`
* `valor`
* `categoria`
* `data`
* `descricao`
* `forma_pagamento`

### Métodos principais

* `__str__()` — retorna um resumo do lançamento.
* `__repr__()` — apresenta os detalhes do lançamento.
* `__eq__()` — compara dois lançamentos.
* `__lt__()` — permite comparar lançamentos para ordenação.
* `__add__()` — permite realizar operações de soma entre lançamentos.

### Relacionamentos

* É a classe base de `Receita` e `Despesa`.
* Está associada a uma `Categoria`.
* Um `Lancamento` pode gerar zero ou mais Alerta.
* Pode fazer parte de um `OrcamentoMensal`.

---

## 2. Classe Receita

**Herda de:** `Lancamento`

**Responsabilidade:** representar uma entrada de dinheiro.

### Atributos

* Herda os atributos de `Lancamento`.

### Métodos principais

* Herda os métodos de `Lancamento`.

---

## 3. Classe Despesa

**Herda de:** `Lancamento`

**Responsabilidade:** representar uma saída de dinheiro.

### Atributos

* Herda os atributos de `Lancamento`.

### Métodos principais

* Herda os métodos de `Lancamento`.
* `verificarLimite()` — verifica se o gasto ultrapassa o limite definido para a categoria.

---

## 4. Classe Categoria

**Responsabilidade:** representar uma categoria de receita ou despesa.

### Atributos

* `id`
* `nome`
* `tipo`
* `limite_mensal`
* `descricao`

### Métodos principais

* `verificarLimite()` — verifica o limite mensal de gastos da categoria.

### Relacionamentos

Receita --------|> Lancamento
Despesa --------|> Lancamento

Categoria "1" -------- "0..*" Lancamento

OrcamentoMensal "1" -------- "0..*" Lancamento

Lancamento "1" -------- "0..*" Alerta

## 5. Classe OrcamentoMensal

**Responsabilidade:** controlar as movimentações financeiras de um determinado mês.

### Atributos

* `mes`
* `ano`
* `orcamento_total`
* `lancamentos`

### Métodos principais

* `adicionarLancamento()` — adiciona um lançamento ao orçamento mensal.
* `calcularReceitas()` — calcula o total de receitas do mês.
* `calcularDespesas()` — calcula o total de despesas do mês.
* `calcularSaldo()` — calcula o saldo disponível.
* `verificarDeficit()` — verifica se o saldo mensal está negativo.

### Relacionamentos

* Um `OrcamentoMensal` pode possuir vários `Lancamentos`.

---

## 6. Classe Alerta

**Responsabilidade:** representar uma notificação gerada a partir de uma regra financeira.

### Atributos

* `tipo`
* `mensagem`
* `data`
* `lancamento`

### Métodos principais

* `gerarAlerta()` — gera um alerta quando uma regra financeira é atingida.
* `exibirAlerta()` — apresenta o alerta ao usuário.

### Relacionamentos

* Um `Alerta` pode estar associado a um `Lancamento`.

---

# 7. Relacionamentos gerais

```text
                    ┌─────────────────┐
                    │    Lancamento   │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                    ▼                 ▼
              ┌──────────┐      ┌──────────┐
              │  Receita │      │  Despesa │
              └──────────┘      └──────────┘


┌──────────────┐          1       ┌─────────────────┐
│   Categoria  │──────────────────│    Lancamento   │
└──────────────┘                  └─────────────────┘


┌──────────────────┐      1      ┌─────────────────┐
│ OrcamentoMensal  │──────────────│    Lancamento   │
└──────────────────┘             └─────────────────┘


┌─────────────────┐       1       ┌──────────────┐
│   Lancamento    │────────────────│    Alerta    │
└─────────────────┘                └──────────────┘
```

## 8. Resumo dos relacionamentos

* `Receita` herda de `Lancamento`.
* `Despesa` herda de `Lancamento`.
* Uma `Categoria` pode possuir vários `Lancamentos`.
* Um `OrcamentoMensal` pode agrupar vários `Lancamentos`.
* Um `Lancamento` pode gerar vários `Alertas`.
