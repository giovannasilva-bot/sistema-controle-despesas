# Sistema de Controle de Despesas Pessoais

Projeto desenvolvido para a disciplina de Programação Orientada a Objetos (POO), do curso de Bacharelado em Engenharia de Software da Universidade Federal do Cariri (UFCA).

## 1. Descrição do projeto

O Sistema de Controle de Despesas Pessoais é uma aplicação de linha de comando (CLI) desenvolvida em Python para auxiliar no gerenciamento de receitas, despesas, categorias e orçamentos mensais.

O sistema permite registrar movimentações financeiras, acompanhar receitas e despesas, calcular o saldo disponível, controlar limites de gastos por categoria e emitir alertas quando determinadas regras financeiras são atingidas.

Também oferece relatórios financeiros e analíticos, permitindo visualizar a distribuição dos gastos, identificar as categorias com maiores despesas e comparar os resultados entre períodos.

Os dados são armazenados em arquivos JSON, possibilitando salvar e recuperar as informações entre execuções.

## 2. Funcionalidades

- Cadastro de receitas e despesas;
- Organiza??o dos lan?amentos por categorias;
- Cria??o e sele??o de m?ltiplos or?amentos mensais;
- Defini??o de or?amento mensal;
- C?lculo de receitas, despesas e saldo;
- Verifica??o de d?ficit or?ament?rio;
- Controle de limites de gastos por categoria;
- Gera??o de alertas para despesas acima do valor configurado e limites de categoria excedidos;
- Relat?rio financeiro mensal;
- Relat?rios de despesas por categoria e forma de pagamento;
- C?lculo do percentual de participa??o de cada categoria nas despesas;
- Identifica??o das categorias com maiores gastos;
- C?lculo de m?dias mensais e hist?ricas;
- Identifica??o do m?s mais econ?mico;
- Compara??o de despesas entre os ?ltimos meses configurados;
- Salvamento e carregamento dos dados em JSON.

## 3. Tecnologias utilizadas

- Python 3.14.3;
- Programação Orientada a Objetos (POO);
- JSON para armazenamento dos dados;
- Pytest para testes automatizados;
- Git e GitHub para controle de versão;
- Interface de linha de comando (CLI).

## 4. Organização das classes

### Lancamento

Classe base que representa uma movimentação financeira. Reúne as informações comuns às receitas e despesas, como valor, categoria, data, descrição e forma de pagamento.

Também utiliza métodos especiais para representação, comparação e operações entre objetos.

### Receita

Classe derivada de `Lancamento`, utilizada para representar entradas de dinheiro.

### Despesa

Classe derivada de `Lancamento`, utilizada para representar saídas de dinheiro.

### Categoria

Representa as categorias utilizadas para organizar os lançamentos financeiros. Possui informações como nome, tipo e limite mensal.

### OrcamentoMensal

Representa o orçamento de determinado mês e ano. É responsável por agrupar os lançamentos, calcular receitas, despesas e saldo, além de verificar a ocorrência de déficit orçamentário.

Também realiza verificações relacionadas aos limites de gastos e gera alertas quando as regras estabelecidas são atingidas.

### Alerta

Representa notificações geradas pelo sistema. Entre os tipos previstos estão:

- `ALTO VALOR`;
- `LIMITE EXCEDIDO`;
- `DÉFICIT ORÇAMENTÁRIO`.

## 5. Relacionamento entre as classes

Os principais relacionamentos do projeto são:

- `Receita` herda de `Lancamento`;
- `Despesa` herda de `Lancamento`;
- Os lançamentos utilizam categorias para sua classificação;
- `OrcamentoMensal` agrupa vários lançamentos;
- `OrcamentoMensal` mantém os alertas gerados durante o controle do orçamento;
- `Alerta` pode estar associado a um lançamento.

As classes `Lancamento`, `Receita`, `Despesa` e `Categoria` estão implementadas em `docs/Semana2/modelos.py`. As classes `OrcamentoMensal` e `Alerta` estão organizadas em `src/models/`.

## 6. Conceitos de POO aplicados

O projeto utiliza diferentes conceitos de Programação Orientada a Objetos:

- Encapsulamento: organização dos atributos e métodos dentro das classes;
- Herança: utilização de `Lancamento` como classe base para `Receita` e `Despesa`;
- Abstração: representação das entidades e regras do domínio financeiro por meio de classes;
- Polimorfismo: utilização de uma interface comum para diferentes estratégias de geração de relatórios;
- Métodos especiais: implementação de métodos como `__str__`, `__repr__`, `__eq__`, `__lt__` e `__add__`;
- Decorator: utilização de `log_operacao` para registrar operações relacionadas à criação de lançamentos.

## 7. Padrão de projeto Strategy

O projeto utiliza o padrão de projeto Strategy para organizar diferentes formas de geração de relatórios.

A classe abstrata `EstrategiaRelatorio` define o método `gerar()`, que é implementado pelas estratégias concretas.

Foram implementadas as seguintes estratégias:

- `RelatorioMensalStrategy`: gera o relatório financeiro mensal;
- `DespesasPorCategoriaStrategy`: apresenta as despesas agrupadas por categoria;
- `PercentuaisPorCategoriaStrategy`: calcula a participação percentual das categorias nas despesas;
- `TopCategoriasStrategy`: identifica as categorias com maiores gastos.

A classe `RelatorioService` disponibiliza os métodos de geração dos relatórios e permite utilizar as estratégias por meio do método `gerar_com_estrategia()`.

## 8. Relatórios analíticos

Além do relatório financeiro mensal, o sistema possui funcionalidades para análise dos dados:

- Percentuais por categoria: apresenta quanto cada categoria representa do total de despesas;
- Top categorias: organiza as categorias de acordo com os valores gastos;
- Média mensal: calcula as médias de receitas, despesas e saldo considerando os orçamentos informados;
- Comparação de despesas: compara os gastos de dois meses, apresentando valores anteriores, atuais, diferenças e variações percentuais.

Esses recursos permitem acompanhar melhor a distribuição dos gastos e observar mudanças entre períodos.

## 9. Persistência dos dados

O armazenamento é realizado em arquivos JSON por meio da classe `JSONRepository`, localizada em `src/repositories/json_repository.py`.

A classe disponibiliza dois métodos principais:

- `salvar()`: grava os dados no arquivo JSON;
- `carregar()`: recupera os dados armazenados.

A conversão dos objetos financeiros para dados que podem ser armazenados e a reconstrução desses objetos são realizadas na aplicação principal, em `src/main.py`.

O arquivo utilizado para armazenar os dados é `data/orcamento.json`. A pasta e o arquivo são criados conforme a necessidade de armazenamento.

As configurações gerais do sistema são armazenadas em `settings.json` e gerenciadas pela classe `ConfiguracaoService`, localizada em `src/services/configuracao_service.py`. Entre os parâmetros configuráveis estão o valor para alertas de despesas elevadas, a quantidade de meses utilizada nas comparações e a meta percentual de economia.


## 10. Estrutura do projeto

```text
sistema-controle-despesas/
|
|-- README.md
|-- settings.json
|
|-- data/                         (criada localmente)
|   |-- orcamento.json            (ignorado pelo Git)
|
|-- src/
|   |-- __init__.py
|   |-- main.py
|   |
|   |-- models/
|   |   |-- __init__.py
|   |   |-- alerta.py
|   |   |-- orcamento_mensal.py
|   |
|   |-- repositories/
|   |   |-- __init__.py
|   |   |-- json_repository.py
|   |
|   |-- services/
|       |-- __init__.py
|       |-- configuracao_service.py
|       |-- relatorio_service.py
|       |-- estrategias_relatorio.py
|
|-- docs/
|   |-- Semana1/
|   |   |-- uml.md
|   |   |-- uml.txt
|   |   |-- uml.png
|   |
|   |-- Semana2/
|   |   |-- modelos.py
|   |   |-- teste_modelos.py
|   |
|   |-- Semana4/
|       |-- README.md
|
|-- tests/
    |-- test_alertas.py
    |-- test_estrategias_relatorio.py
    |-- test_relatorios_analiticos.py
    |-- test_semana3.py
    |-- test_semana4.py
```

## 11. Como executar o projeto

É necessário ter o Python instalado.

### Clonar o repositório

```bash
git clone https://github.com/giovannasilva-bot/sistema-controle-despesas.git
```

### Entrar na pasta do projeto

```bash
cd sistema-controle-despesas
```

### Criar e ativar o ambiente virtual

No PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Executar a aplicação

Na raiz do projeto, execute:

```bash
python -m src.main
```

A aplicação apresentará o menu interativo para utilização das funcionalidades do sistema.

## 12. Testes automatizados

O projeto utiliza Pytest para executar os testes automatizados e verificar o funcionamento das funcionalidades implementadas.

Para instalar as dependências necessárias:

```bash
python -m pip install typer rich pytest
```

Para executar todos os testes, utilize:

```bash
python -m pytest
```

Os testes automatizados estão organizados na pasta `tests/`, abrangendo os modelos, as regras de negócio, os alertas e os relatórios.

## 13. Documentação UML

Os arquivos referentes à modelagem UML estão disponíveis em `docs/Semana1/`:

- `uml.md`: documentação textual do modelo;
- `uml.txt`: representação textual do diagrama;
- `uml.png`: representação visual do diagrama.

---

Projeto acadêmico desenvolvido para a disciplina de Programação Orientada a Objetos (POO) — Engenharia de Software, UFCA.

## 14. Versionamento

A tag `v1.0` no GitHub representa a versão final e completa do projeto para a entrega da disciplina.

Essa versão deve conter todas as funcionalidades implementadas e testadas no sistema.

As demais tags presentes no repositório representam versões anteriores do desenvolvimento do projeto.

## 15. Como utilizar o sistema

Após instalar as dependências e ativar o ambiente virtual, os comandos devem ser executados no terminal, a partir da pasta raiz do projeto.

### Consultar os comandos disponíveis

Para visualizar todas as funcionalidades disponíveis:

```powershell
python -m src.main --help
```

Para consultar as opções de um comando específico:

```powershell
python -m src.main iniciar --help
```

### Criar um orçamento mensal

Para cadastrar um novo orçamento, informe o mês, o ano e o valor total disponível:

```powershell
python -m src.main iniciar --mes 11 --ano 2027 --orcamento 1500
```

O parâmetro `--sobrescrever` permite substituir um orçamento já existente. Deve ser utilizado com cuidado, pois altera os dados daquele período.

### Cadastrar receitas

Para adicionar uma receita, informe o valor, a categoria e a descrição:

```powershell
python -m src.main adicionar-receita --valor 2500 --categoria Salario --descricao "Salario mensal"
```

Também podem ser informados:

- `--data`: data no formato AAAA-MM-DD;
- `--forma-pagamento`: forma de recebimento. O padrão é Dinheiro.

### Cadastrar despesas

Para adicionar uma despesa:

```powershell
python -m src.main adicionar-despesa --valor 150 --categoria Alimentacao --descricao "Compra no supermercado"
```

Também podem ser informados:

- `--data`: data no formato AAAA-MM-DD;
- `--forma-pagamento`: forma de pagamento. O padrão é Dinheiro;
- `--limite-mensal`: limite mensal da categoria.

### Consultar informações do orçamento

**Resumo financeiro:**

```powershell
python -m src.main status
```

**Listagem de receitas e despesas:**

```powershell
python -m src.main listar-lancamentos
```

**Consultar alertas registrados:**

```powershell
python -m src.main consultar-alertas
```

### Consultar relatórios

**Relatório financeiro mensal:**

```powershell
python -m src.main relatorio-mensal
```

**Despesas agrupadas por categoria:**

```powershell
python -m src.main despesas-por-categoria
```

**Despesas agrupadas por forma de pagamento:**

```powershell
python -m src.main despesas-por-forma-pagamento
```

### Análises históricas

**Média financeira dos orçamentos cadastrados:**

```powershell
python -m src.main media-mensal
```

**Identificar o mês mais econômico:**

```powershell
python -m src.main mes-mais-economico
```

**Comparar as despesas dos últimos meses cadastrados:**

```powershell
python -m src.main comparar-despesas
```

### Observação

Os comandos que trabalham com um orçamento específico podem solicitar a seleção do período desejado. Já as análises históricas consideram os orçamentos cadastrados.

Os exemplos de cadastro são ilustrativos. Antes de executar, verifique os dados para evitar registros duplicados ou alterações indesejadas.
