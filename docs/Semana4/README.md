# Etapa 4 — Sistema de Controle de Despesas Pessoais

## Descrição

Nesta etapa, foi iniciada a implementação da interface de linha de comando (CLI) do Sistema de Controle de Despesas Pessoais. O objetivo é permitir que o usuário interaja com as funcionalidades do sistema pelo terminal.

## Objetivos

- Implementar um menu interativo.
- Permitir o cadastro de receitas e despesas.
- Consultar os lançamentos financeiros.
- Visualizar o saldo e os relatórios mensais.
- Permitir o salvamento dos dados em arquivo JSON.

## Tecnologias

- Python
- JSON
- Pytest
- Git e GitHub

## Funcionalidades implementadas

- Menu principal com opções de navegação.
- Cadastro de receitas e despesas.
- Listagem dos lançamentos cadastrados.
- Consulta do saldo financeiro.
- Exibição do relatório mensal.
- Consulta de despesas por categoria.
- Salvamento e carregamento dos dados em JSON.

## Status

A interface inicial foi implementada e os testes automatizados foram executados. A documentação será complementada com os detalhes das validações e dos testes realizados.

## Regras de negócio e validações

O sistema possui validações para evitar o cadastro de informações inválidas:

- O valor de uma receita ou despesa deve ser maior que zero.
- O mês do orçamento deve estar entre 1 e 12.
- O ano deve ser maior ou igual a 1.
- O valor total do orçamento não pode ser negativo.
- A categoria precisa ser compatível com o tipo de lançamento, receita ou despesa.
- A data do lançamento deve pertencer ao mês e ao ano do orçamento selecionado.
- O sistema permite salvar os dados em um arquivo JSON e carregá-los posteriormente.

## Como executar o projeto

1. Abra o terminal na pasta principal do projeto.
2. Ative o ambiente virtual:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Execute o sistema:

   ```powershell
   python -m src.main
   ```

4. Para executar os testes automatizados:

   ```powershell
   python -m pytest -v
   ```

## Testes

Foram criados testes automatizados para verificar as funcionalidades do sistema, incluindo o cadastro de lançamentos, o cálculo do saldo, a geração de relatórios, a persistência dos dados em JSON e as validações da interface.

A execução dos testes permite identificar possíveis erros e verificar se as funcionalidades implementadas estão funcionando como esperado.

## Status da etapa

A interface de linha de comando foi implementada com opções para cadastrar receitas e despesas, consultar informações financeiras, gerar relatórios e salvar os dados. A documentação registra as funcionalidades, as regras de negócio e as instruções para executar o projeto e seus testes.