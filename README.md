# Sistema de Controle de Despesas Pessoais

Projeto desenvolvido para a disciplina de Programação Orientada a Objetos (POO) do curso de Bacharelado em Engenharia de Software da Universidade Federal do Cariri (UFCA).

## 1. Descrição do projeto

O Sistema de Controle de Despesas Pessoais tem como objetivo auxiliar o usuário no gerenciamento de suas receitas, despesas, categorias e orçamentos mensais.

O sistema permitirá registrar movimentações financeiras, acompanhar o saldo disponível, controlar limites de gastos por categoria, gerar relatórios e emitir alertas de acordo com regras financeiras definidas.

O projeto será desenvolvido inicialmente como uma aplicação de linha de comando (CLI), utilizando Python e armazenamento persistente em arquivos JSON.

## 2. Objetivos

O projeto tem como principais objetivos:

* Registrar receitas e despesas;
* Organizar lançamentos por categorias;
* Controlar o orçamento mensal;
* Calcular receitas, despesas e saldo disponível;
* Controlar limites de gastos por categoria;
* Gerar alertas financeiros;
* Gerar relatórios e estatísticas;
* Aplicar conceitos de Programação Orientada a Objetos;
* Utilizar testes automatizados para validar as funcionalidades.

## 3. Tecnologias

* Python
* Programação Orientada a Objetos (POO)
* JSON
* Pytest
* Git
* GitHub
* Interface de linha de comando (CLI)

## 4. Estrutura planejada de classes

O sistema será organizado utilizando as seguintes classes principais:

### Lancamento

Classe base responsável por representar uma movimentação financeira.

Principais informações:

* ID;
* Valor;
* Categoria;
* Data;
* Descrição;
* Forma de pagamento.

### Receita

Classe derivada de `Lancamento`, responsável por representar entradas de dinheiro.

### Despesa

Classe derivada de `Lancamento`, responsável por representar saídas de dinheiro.

### Categoria

Representa uma categoria de receita ou despesa.

Possui informações como:

* ID;
* Nome;
* Tipo;
* Limite mensal;
* Descrição.

### OrcamentoMensal

Representa o orçamento de determinado mês.

Será responsável por organizar os lançamentos do período e auxiliar no cálculo do saldo mensal.

### Alerta

Representa notificações geradas quando alguma regra financeira é atingida, como gastos elevados, ultrapassagem de limites ou saldo mensal negativo.

## 5. Relacionamento entre as classes

O sistema terá os seguintes relacionamentos principais:

* `Receita` herda de `Lancamento`;
* `Despesa` herda de `Lancamento`;
* `Lancamento` está associado a uma `Categoria`;
* `OrcamentoMensal` agrupa vários `Lancamentos`;
* `Alerta` pode estar associado a um `Lancamento`;
* `Categoria` pode possuir vários `Lancamentos`.

## 6. Estrutura planejada do projeto

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
    └── uml.md
```

## 7. Desenvolvimento por etapas

### Semana 1 — Modelagem e definição do projeto

* Definição das classes;
* Definição dos atributos e métodos;
* Definição dos relacionamentos;
* UML textual;
* Estrutura inicial do projeto;
* Criação das classes vazias com docstrings;
* README inicial.

### Semana 2 — Classes base e encapsulamento

* Implementação de `Lancamento`;
* Implementação de `Receita`;
* Implementação de `Despesa`;
* Implementação de `Categoria`;
* Uso de `@property`;
* Validações básicas;
* Métodos especiais.

### Semana 3 — Relacionamentos e persistência

* Relacionamento entre lançamentos, categorias e orçamento;
* Persistência em JSON;
* Cálculos financeiros;
* Primeiro relatório.

### Semana 4 — Regras e alertas

* Limites de categoria;
* Alertas;
* Validações;
* Saldo mensal;
* Interface CLI;
* Testes dos principais fluxos.

### Semana 5 — Relatórios e finalização

* Relatórios analíticos;
* Comparação entre meses;
* Possível aplicação de padrão de projeto;
* Finalização do README;
* Testes finais;
* Versão `v1.0`.

## 8. Status atual

O projeto encontra-se na etapa inicial de modelagem e estruturação, correspondente à Semana 1 do projeto de POO.

Nesta etapa, o foco é definir a arquitetura do sistema e criar a estrutura inicial das classes antes da implementação das regras de negócio.
