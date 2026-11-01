from datetime import date
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from docs.Semana2.modelos import Categoria, Receita, Despesa
from src.models.orcamento_mensal import OrcamentoMensal
from src.repositories.json_repository import JSONRepository
from src.services.relatorio_service import RelatorioService


# Arquivo onde os dados serão guardados
CAMINHO_DADOS = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "orcamento.json"
)

repositorio = JSONRepository(CAMINHO_DADOS)

# Aplicação da nova interface de linha de comando
app = typer.Typer(
    help="Sistema de Controle de Despesas Pessoais",
    no_args_is_help=True
)

console = Console()


def ler_inteiro(mensagem, minimo=None, maximo=None):
    """Lê um número inteiro e valida os limites, quando informados."""
    while True:
        try:
            valor = int(input(mensagem))

            if minimo is not None and valor < minimo:
                print(f"Digite um número maior ou igual a {minimo}.")
                continue

            if maximo is not None and valor > maximo:
                print(f"Digite um número menor ou igual a {maximo}.")
                continue

            return valor

        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def ler_valor(mensagem):
    """Lê um valor financeiro positivo."""
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))

            if valor <= 0:
                print("O valor deve ser maior que zero.")
                continue

            return valor

        except ValueError:
            print("Valor inválido. Exemplo: 150,50.")


def criar_orcamento():
    print("\nCONFIGURAÇÃO DO ORÇAMENTO")

    mes = ler_inteiro("Mês (1 a 12): ", 1, 12)
    ano = ler_inteiro("Ano: ", 1)
    total = ler_valor("Orçamento mensal disponível: R$ ")

    return OrcamentoMensal(mes, ano, total)


def salvar_dados(orcamento):
    """Converte os lançamentos em dados que podem ser salvos em JSON."""
    dados = {
        "mes": orcamento.mes,
        "ano": orcamento.ano,
        "orcamento_total": orcamento.orcamento_total,
        "lancamentos": []
    }

    for lancamento in orcamento.lancamentos:
        dados["lancamentos"].append({
            "tipo": (
                "RECEITA"
                if isinstance(lancamento, Receita)
                else "DESPESA"
            ),
            "valor": lancamento.valor,
            "data": lancamento.data.isoformat(),
            "descricao": lancamento.descricao,
            "forma_pagamento": lancamento.forma_pagamento,
            "categoria": {
                "nome": lancamento.categoria.nome,
                "tipo": lancamento.categoria.tipo,
                "limite_mensal": lancamento.categoria.limite_mensal,
                "descricao": lancamento.categoria.descricao
            }
        })

    repositorio.salvar(dados)
    print("\nDados salvos com sucesso!")


def carregar_dados():
    """Reconstrói os objetos Python a partir do JSON salvo."""
    dados = repositorio.carregar()

    if not isinstance(dados, dict) or "lancamentos" not in dados:
        return None

    try:
        orcamento = OrcamentoMensal(
            dados["mes"],
            dados["ano"],
            dados["orcamento_total"]
        )

        for item in dados["lancamentos"]:
            info_categoria = item["categoria"]

            categoria = Categoria(
                nome=info_categoria["nome"],
                tipo=info_categoria["tipo"],
                limite_mensal=info_categoria["limite_mensal"],
                descricao=info_categoria.get("descricao", "")
            )

            data_lancamento = date.fromisoformat(item["data"])

            if item["tipo"] == "RECEITA":
                lancamento = Receita(
                    valor=item["valor"],
                    categoria=categoria,
                    data=data_lancamento,
                    descricao=item["descricao"],
                    forma_pagamento=item["forma_pagamento"],
                    _silencioso=True
                )
            elif item["tipo"] == "DESPESA":
                lancamento = Despesa(
                    valor=item["valor"],
                    categoria=categoria,
                    data=data_lancamento,
                    descricao=item["descricao"],
                    forma_pagamento=item["forma_pagamento"],
                    _silencioso=True
                )
            else:
                raise ValueError("Tipo de lançamento inválido no arquivo.")

            orcamento.adicionarLancamento(lancamento)

        return orcamento

    except (KeyError, TypeError, ValueError) as erro:
        print(f"\nNão foi possível carregar os dados: {erro}")
        return None



def adicionar_lancamento(orcamento, tipo):
    print("\n=== CADASTRO DE LANCAMENTO ===")

    # Recupera as categorias existentes para o tipo escolhido.
    categorias = {}

    for lancamento_existente in orcamento.lancamentos:
        categoria_existente = lancamento_existente.categoria

        if categoria_existente.tipo == tipo:
            chave = categoria_existente.nome.casefold()
            categorias[chave] = categoria_existente

    lista_categorias = list(categorias.values())

    if lista_categorias:
        for indice, categoria_item in enumerate(lista_categorias, start=1):
            print(f"  {indice}. {categoria_item.nome}")

        print(f"  {len(lista_categorias) + 1}. Cadastrar nova categoria")
    else:
        print("Nenhuma categoria cadastrada para esse tipo.")

    print("  0. Voltar ao menu")

    limite_escolha = len(lista_categorias) + 1

    escolha = ler_inteiro(
        "\nSelecione uma categoria: ",
        0,
        limite_escolha
    )

    if escolha == 0:
        print("Cadastro cancelado.")
        return

    if escolha <= len(lista_categorias):
        categoria = lista_categorias[escolha - 1]

    else:
        nome_categoria = input("Nome da nova categoria: ").strip()

        if not nome_categoria:
            print("O nome da categoria não pode ficar vazio.")
            return

        if nome_categoria.casefold() in categorias:
            print("Essa categoria já existe para esse tipo.")
            return

        limite = None

        if tipo == "DESPESA":
            limite_texto = input(
                "Limite mensal (Enter para não definir): "
            ).strip()

            if limite_texto:
                try:
                    limite = float(limite_texto.replace(",", "."))

                    if limite < 0:
                        print("O limite não pode ser negativo.")
                        return

                except ValueError:
                    print("Limite inválido.")
                    return

        categoria = Categoria(
            nome=nome_categoria,
            tipo=tipo,
            limite_mensal=limite
        )

    valor = ler_valor("Valor: R$ ")

    if valor is None:
        return

    data_texto = input(
        "Data (AAAA-MM-DD; Enter para hoje): "
    ).strip()

    try:
        data_lancamento = (
            date.fromisoformat(data_texto)
            if data_texto
            else date.today()
        )
    except ValueError:
        print("Data inválida. Use o formato AAAA-MM-DD.")
        return

    descricao = input("Descrição: ").strip()

    if not descricao:
        print("A descrição não pode ficar vazia.")
        return

    forma_pagamento = input("Forma de pagamento: ").strip()

    if not forma_pagamento:
        print("A forma de pagamento não pode ficar vazia.")
        return

    try:
        if tipo == "RECEITA":
            lancamento = Receita(
                valor=valor,
                categoria=categoria,
                data=data_lancamento,
                descricao=descricao,
                forma_pagamento=forma_pagamento
            )
        else:
            lancamento = Despesa(
                valor=valor,
                categoria=categoria,
                data=data_lancamento,
                descricao=descricao,
                forma_pagamento=forma_pagamento
            )

        orcamento.adicionarLancamento(lancamento)

        print("\nLançamento cadastrado com sucesso!")

    except ValueError as erro:
        print(f"\nNão foi possível cadastrar: {erro}")


def listar_lancamentos(orcamento):
    print("\nLANÇAMENTOS CADASTRADOS")
    print("-" * 45)

    if not orcamento.lancamentos:
        print("Nenhum lançamento cadastrado.")
        return

    for numero, lancamento in enumerate(
        sorted(orcamento.lancamentos), start=1
    ):
        tipo = (
            "Receita"
            if isinstance(lancamento, Receita)
            else "Despesa"
        )

        print(f"{numero}. {tipo} | {lancamento}")
        print(f"   Pagamento: {lancamento.forma_pagamento}")


def exibir_saldo(orcamento):
    print("\nRESUMO FINANCEIRO")
    print("-" * 35)
    print(f"Orçamento: R$ {orcamento.orcamento_total:.2f}")
    print(f"Receitas:  R$ {orcamento.calcularReceitas():.2f}")
    print(f"Despesas:  R$ {orcamento.calcularDespesas():.2f}")
    print(f"Saldo:     R$ {orcamento.calcularSaldo():.2f}")


    if orcamento.verificarDeficit():
        print("Atenção: as despesas ultrapassaram o orçamento.")

def exibir_alertas(orcamento):
    print("\n=== ALERTAS DO ORÇAMENTO ===")

    if not orcamento.alertas:
        print("Nenhum alerta registrado.")
        return

    for alerta in orcamento.alertas:
        print(f"- {alerta}")

@app.command()
def iniciar(
    mes: int = typer.Option(..., "--mes", help="Mês do orçamento."),
    ano: int = typer.Option(..., "--ano", help="Ano do orçamento."),
    orcamento: float = typer.Option(
        ...,
        "--orcamento",
        help="Valor total disponível no mês."
    ),
    sobrescrever: bool = typer.Option(
        False,
        "--sobrescrever",
        help="Substitui um orçamento já existente."
    )
):
    """Cria um novo orçamento mensal."""

    if mes < 1 or mes > 12:
        raise typer.BadParameter("O mês deve estar entre 1 e 12.")

    if ano < 1:
        raise typer.BadParameter("O ano deve ser válido.")

    if orcamento < 0:
        raise typer.BadParameter("O orçamento não pode ser negativo.")

    if repositorio.caminho.exists() and not sobrescrever:
        console.print(
            "[yellow]Já existe um orçamento cadastrado.[/yellow]"
        )
        console.print(
            "Use --sobrescrever se realmente deseja substituí-lo."
        )
        raise typer.Exit(code=1)

    novo_orcamento = OrcamentoMensal(mes, ano, orcamento)

    salvar_dados(novo_orcamento)

    console.print(
        Panel(
            f"Orçamento de [bold green]R$ {orcamento:.2f}[/bold green] "
            f"configurado para {mes:02d}/{ano}.",
            title="Configuração concluída",
            border_style="green"
        )
    )

@app.command()
def status():
    """Exibe um resumo do orçamento cadastrado."""

    orcamento = carregar_dados()

    if orcamento is None:
        console.print(
            "[yellow]Nenhum orçamento cadastrado. "
            "Execute o comando iniciar.[/yellow]"
        )
        raise typer.Exit(code=1)

    tabela = Table(title="Resumo financeiro")

    tabela.add_column("Informação", style="cyan")
    tabela.add_column("Valor", justify="right")

    tabela.add_row("Período", f"{orcamento.mes:02d}/{orcamento.ano}")
    tabela.add_row("Orçamento", f"R$ {orcamento.orcamento_total:.2f}")
    tabela.add_row("Receitas", f"R$ {orcamento.calcularReceitas():.2f}")
    tabela.add_row("Despesas", f"R$ {orcamento.calcularDespesas():.2f}")
    tabela.add_row("Saldo", f"R$ {orcamento.calcularSaldo():.2f}")

    console.print(tabela)

    if orcamento.verificarDeficit():
        console.print(
            "[bold red]Atenção: o orçamento está em déficit![/bold red]"
        )

@app.command()
def adicionar_receita(
    valor: float = typer.Option(..., "--valor", help="Valor da receita."),
    categoria: str = typer.Option(..., "--categoria", help="Categoria da receita."),
    descricao: str = typer.Option(..., "--descricao", help="Descrição da receita."),
    data_lancamento: str | None = typer.Option(
        None, "--data", help="Data no formato AAAA-MM-DD."
    ),
    forma_pagamento: str = typer.Option(
        "Dinheiro", "--forma-pagamento", help="Forma de recebimento."
    )
):
    """Cadastra uma nova receita."""

    orcamento = carregar_dados()

    if orcamento is None:
        console.print("[red]Nenhum orçamento cadastrado.[/red]")
        raise typer.Exit(code=1)

    if valor <= 0:
        raise typer.BadParameter("O valor deve ser maior que zero.")

    if not categoria.strip() or not descricao.strip():
        raise typer.BadParameter("Categoria e descrição são obrigatórias.")

    try:
        data = (
            date.fromisoformat(data_lancamento)
            if data_lancamento
            else date.today()
        )
    except ValueError:
        raise typer.BadParameter("Data inválida. Use AAAA-MM-DD.")

    categoria_existente = next(
        (
            lancamento.categoria
            for lancamento in orcamento.lancamentos
            if lancamento.categoria.tipo == "RECEITA"
            and lancamento.categoria.nome.casefold() == categoria.casefold()
        ),
        None
    )

    if categoria_existente is None:
        categoria_existente = Categoria(
            nome=categoria.strip(),
            tipo="RECEITA"
        )

    try:
        receita = Receita(
            valor=valor,
            categoria=categoria_existente,
            data=data,
            descricao=descricao.strip(),
            forma_pagamento=forma_pagamento.strip()
        )

        orcamento.adicionarLancamento(receita)
        salvar_dados(orcamento)

        console.print(
            Panel(
                f"Receita de [green]R$ {valor:.2f}[/green] cadastrada!",
                title="Cadastro concluído",
                border_style="green"
            )
        )

    except ValueError as erro:
        raise typer.BadParameter(str(erro))

@app.command()
def adicionar_despesa(
    valor: float = typer.Option(..., "--valor", help="Valor da despesa."),
    categoria: str = typer.Option(..., "--categoria", help="Categoria da despesa."),
    descricao: str = typer.Option(..., "--descricao", help="Descrição da despesa."),
    data_lancamento: str | None = typer.Option(
        None, "--data", help="Data no formato AAAA-MM-DD."
    ),
    forma_pagamento: str = typer.Option(
        "Dinheiro", "--forma-pagamento", help="Forma de pagamento."
    ),
    limite_mensal: float | None = typer.Option(
        None, "--limite-mensal", help="Limite mensal da categoria."
    )
):
    """Cadastra uma nova despesa."""

    orcamento = carregar_dados()

    if orcamento is None:
        console.print("[red]Nenhum orçamento cadastrado.[/red]")
        raise typer.Exit(code=1)

    if valor <= 0:
        raise typer.BadParameter("O valor deve ser maior que zero.")

    if not categoria.strip() or not descricao.strip():
        raise typer.BadParameter("Categoria e descrição são obrigatórias.")

    if limite_mensal is not None and limite_mensal < 0:
        raise typer.BadParameter("O limite mensal não pode ser negativo.")

    try:
        data = (
            date.fromisoformat(data_lancamento)
            if data_lancamento
            else date.today()
        )
    except ValueError:
        raise typer.BadParameter("Data inválida. Use AAAA-MM-DD.")

    categoria_existente = next(
        (
            lancamento.categoria
            for lancamento in orcamento.lancamentos
            if lancamento.categoria.tipo == "DESPESA"
            and lancamento.categoria.nome.casefold() == categoria.casefold()
        ),
        None
    )

    if categoria_existente is not None:
        if limite_mensal is not None:
            raise typer.BadParameter(
                "A categoria já existe. O limite deve ser definido na criação."
            )
    else:
        categoria_existente = Categoria(
            nome=categoria.strip(),
            tipo="DESPESA",
            limite_mensal=limite_mensal
        )

    try:
        despesa = Despesa(
            valor=valor,
            categoria=categoria_existente,
            data=data,
            descricao=descricao.strip(),
            forma_pagamento=forma_pagamento.strip()
        )

        orcamento.adicionarLancamento(despesa)
        salvar_dados(orcamento)

        console.print(
            Panel(
                f"Despesa de [red]R$ {valor:.2f}[/red] cadastrada!",
                title="Cadastro concluído",
                border_style="green"
            )
        )

        if orcamento.alertas:
            console.print("[yellow]Verifique os alertas do orçamento.[/yellow]")

    except ValueError as erro:
        raise typer.BadParameter(str(erro))

@app.command()
def listar_lancamentos():
    """Lista todas as receitas e despesas cadastradas."""

    orcamento = carregar_dados()

    if orcamento is None:
        console.print("[yellow]Nenhum orçamento cadastrado.[/yellow]")
        raise typer.Exit(code=1)

    if not orcamento.lancamentos:
        console.print("[yellow]Nenhum lançamento cadastrado.[/yellow]")
        return

    tabela = Table(title="Lançamentos cadastrados")

    tabela.add_column("Data", style="cyan")
    tabela.add_column("Tipo")
    tabela.add_column("Categoria")
    tabela.add_column("Descrição")
    tabela.add_column("Valor", justify="right")
    tabela.add_column("Forma de pagamento")

    for lancamento in sorted(orcamento.lancamentos):
        tipo = (
            "[green]Receita[/green]"
            if isinstance(lancamento, Receita)
            else "[red]Despesa[/red]"
        )

        tabela.add_row(
            lancamento.data.strftime("%d/%m/%Y"),
            tipo,
            lancamento.categoria.nome,
            lancamento.descricao,
            f"R$ {lancamento.valor:.2f}",
            lancamento.forma_pagamento
        )

    console.print(tabela)

@app.command()
def consultar_alertas():
    """Exibe os alertas registrados no orçamento."""

    orcamento = carregar_dados()

    if orcamento is None:
        console.print("[yellow]Nenhum orçamento cadastrado.[/yellow]")
        raise typer.Exit(code=1)

    if not orcamento.alertas:
        console.print("[green]Nenhum alerta registrado.[/green]")
        return

    tabela = Table(title="Alertas do orçamento")

    tabela.add_column("Nº", style="cyan", justify="center")
    tabela.add_column("Alerta", style="yellow")

    for numero, alerta in enumerate(orcamento.alertas, start=1):
        tabela.add_row(str(numero), str(alerta))

    console.print(tabela)


@app.command()
def relatorio_mensal():
    """Exibe o relatório financeiro mensal."""

    orcamento = carregar_dados()

    if orcamento is None:
        console.print("[yellow]Nenhum orçamento cadastrado.[/yellow]")
        raise typer.Exit(code=1)

    RelatorioService.exibir_relatorio_mensal(orcamento)


@app.command()
def despesas_por_categoria():
    """Exibe as despesas agrupadas por categoria."""

    orcamento = carregar_dados()

    if orcamento is None:
        console.print("[yellow]Nenhum orçamento cadastrado.[/yellow]")
        raise typer.Exit(code=1)

    RelatorioService.exibir_despesas_por_categoria(orcamento)

@app.command()
def despesas_por_forma_pagamento():
    """Exibe as despesas agrupadas por forma de pagamento."""

    orcamento = carregar_dados()

    if orcamento is None:
        console.print("[yellow]Nenhum orçamento cadastrado.[/yellow]")
        raise typer.Exit(code=1)

    RelatorioService.exibir_despesas_por_forma_pagamento(orcamento)

def exibir_menu():
    print("\n" + "=" * 42)
    print(" SISTEMA DE CONTROLE DE DESPESAS")
    print("=" * 42)
    print("1 - Adicionar receita")
    print("2 - Adicionar despesa")
    print("3 - Listar lançamentos")
    print("4 - Consultar saldo")
    print("5 - Relatório mensal")
    print("6 - Despesas por categoria")
    print("7 - Consultar alertas")
    print("8 - Salvar dados")
    print("9 - Salvar e sair")
    print("0 - Encerrar sem salvar")
    print("10 - Despesas por forma de pagamento")
    print("=" * 42)



def main():
    print("Bem-vinda ao Sistema de Controle de Despesas!")

    orcamento = carregar_dados()

    if orcamento is not None:
        print(
            f"Orçamento {orcamento.mes:02d}/{orcamento.ano} "
            "carregado do arquivo."
        )
    else:
        orcamento = criar_orcamento()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            adicionar_lancamento(orcamento, "RECEITA")

        elif opcao == "2":
            adicionar_lancamento(orcamento, "DESPESA")

        elif opcao == "3":
            listar_lancamentos(orcamento)

        elif opcao == "4":
            exibir_saldo(orcamento)

        elif opcao == "5":
            RelatorioService.exibir_relatorio_mensal(orcamento)

        elif opcao == "6":
            RelatorioService.exibir_despesas_por_categoria(orcamento)

        elif opcao == "7":
            exibir_alertas(orcamento)

        elif opcao == "8":
            salvar_dados(orcamento)

        elif opcao == "9":
            salvar_dados(orcamento)
            print("Programa encerrado.")
            break

        elif opcao == "0":
            print("Programa encerrado sem salvar.")
            break
        elif opcao == "10":
            RelatorioService.exibir_despesas_por_forma_pagamento(orcamento)

        else:
            print("Opção inválida. Escolha uma opção do menu.")


if __name__ == "__main__":
    app()
