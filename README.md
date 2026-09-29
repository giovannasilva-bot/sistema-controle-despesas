# Sistema de Controle de Despesas Pessoais

Projeto desenvolvido para a disciplina de Programação Orientada a Objetos (POO) do curso de Bacharelado em Engenharia de Software da Universidade Federal do Cariri(UFCA).

## 1. Descrição do projeto

O Sistema de Controle de Despesas Pessoais tem como objetivo auxiliar o usuário no gerenciamento de suas receitas, despesas, categorias e orçamentos mensais.

O sistema permitirá registrar movimentações financeiras, acompanhar o saldo disponível, controlar limites de gastos por categoria, gerar relatórios e emitir alertas de acordo com regras financeiras definidas.

O projeto será desenvolvido inicialmente como uma aplicação de linha de comando (CLI), utilizando Python e armazenamento persistente em arquivos JSON.

## 2. Objetivos

O projeto tem como principais objetivos:

- Registrar receitas e despesas;
- Organizar lançamentos por categorias;
- Controlar o orçamento mensal;
- Calcular receitas, despesas e saldo disponível;
- Controlar limites de gastos por categoria;
- Gerar alertas financeiros;
- Gerar relatórios e estatísticas;
- Aplicar conceitos de Programação Orientada a Objetos;
- Utilizar testes automatizados para validar as funcionalidades.

## 3. Tecnologias

- Python
- Programação Orientada a Objetos (POO)
- JSON
- Pytest
- Git
- GitHub
- Interface de linha de comando (CLI)

## 4. Estrutura planejada de classes

O sistema será organizado utilizando as seguintes classes principais:

### Lancamento

Classe base responsável por representar uma movimentação financeira.

Principais atributos:

- ID;
- Valor;
- Categoria;
- Data;
- Descrição;
- Forma de pagamento.

Principais métodos especiais:

- `__str__()`;
- `__repr__()`;
- `__eq__()`;
- `__lt__()`;
- `__add__()`.

### Receita

Classe derivada de `Lancamento`, responsável por representar entradas de dinheiro.

Herda os atributos e comportamentos básicos de `Lancamento`.

### Despesa

Classe derivada de `Lancamento`, responsável por representar saídas de dinheiro.

Além dos comportamentos herdados, poderá verificar se o gasto ultrapassa o limite definido para sua categoria.

### Categoria

Representa uma categoria de receita ou despesa.

Principais atributos:

- ID;
- Nome;
- Tipo;
- Limite mensal;
- Descrição.

A categoria poderá verificar o limite mensal de gastos quando for do tipo `DESPESA`.

### OrcamentoMensal

Representa o orçamento de determinado mês.

Será responsável por organizar os lançamentos do período e auxiliar nos cálculos de receitas, despesas, saldo disponível e déficit orçamentário.

### Alerta

Representa notificações geradas quando alguma regra financeira é atingida, como gastos elevados, ultrapassagem de limites ou saldo mensal negativo.

## 5. Relacionamento entre as classes

O sistema terá os seguintes relacionamentos principais:

- `Receita` herda de `Lancamento`;
- `Despesa` herda de `Lancamento`;
- Uma `Categoria` pode possuir vários `Lancamentos`;
- Um `OrcamentoMensal` pode agrupar vários `Lancamentos`;
- Um `Lancamento` pode gerar vários `Alertas`.

A documentação do modelo UML está disponível nos seguintes arquivos:

- `docs/uml.md` — documentação detalhada das classes, atributos, métodos e relacionamentos.
- `docs/uml.txt` — representação textual do UML para consulta e entrega.
- `docs/uml.png` — representação visual do diagrama UML.

## 6. Conceitos de POO

- Encapsulamento por meio da organização dos atributos e métodos nas classes.
- Herança entre `Lancamento`, `Receita` e `Despesa`.
- Polimorfismo nos comportamentos específicos das classes derivadas, conforme a implementação do projeto.
- Abstração na representação das entidades financeiras.
- Métodos especiais para representação, comparação e operações entre objetos.

## 7. Estrutura planejada do projeto

```text
sistema-controle-despesas/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── __init__.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── lancamento.py
│   │   ├── receita.py
│   │   ├── despesa.py
│   │   ├── categoria.py
│   │   ├── orcamento_mensal.py
│   │   └── alerta.py
│   │
│   ├── services/
│   │   └── __init__.py
│   │
│   ├── repositories/
│   │   └── __init__.py
│   │
│   └── cli/
│       ├── __init__.py
│       └── main.py
│
├── tests/
│   └── __init__.py
│
├── data/
│   ├── categorias.json
│   ├── lancamentos.json
│   ├── orcamentos.json
│   ├── alertas.json
│   └── settings.json
│
└── docs/
    ├── uml.md
    ├── uml.txt
    └── uml.png
