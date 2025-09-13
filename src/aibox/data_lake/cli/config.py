"""CLI para configuração
da biblioteca.
"""

import typer
from rich.prompt import Confirm, Prompt

from aibox.data_lake.config import Config
from aibox.data_lake.factory import get_bucket

from .utils import console, get_config

cli = typer.Typer(
    no_args_is_help=True, add_completion=False, help="Configuração de buckets & acesso."
)


@cli.command(name="setup", help="Configura a biblioteca para primeiro uso.")
def setup():
    if Config.local_file_path().exists():
        try:
            config = get_config()
        except:
            return -1

        console.print("[info]Configuração encontrada:[/]")
        console.print_json(config.model_dump_json(indent=2))
        if not Confirm.ask("[warning]Deseja sobrescrever?[/]", console=console, default=True):
            console.print("[info]Configuração atual mantida.[/]")
            return

    # Obtendo dados
    bronze_bucket = Prompt.ask("[info]URL do bucket nível bronze[/]", console=console)
    silver_bucket = Prompt.ask("[info]URL do bucket nível prata[/]", console=console)
    gold_bucket = Prompt.ask("[info]URL do bucket nível ouro[/]", console=console)

    # Garantindo que os buckets são válidos
    for bucket in [bronze_bucket, silver_bucket, gold_bucket]:
        try:
            get_bucket(bucket)
        except Exception as e:
            console.print(f"[error]Não foi possível accesar o bucket '{bucket}': {e}[/]")
            return -1

    # Criando nova configuração
    config = Config(
        bronze_bucket=bronze_bucket,
        silver_bucket=silver_bucket,
        gold_bucket=gold_bucket,
    )

    # Persistência
    config.save_to_file()
    console.print("[success]Configuração atualizada:[/]")
    console.print_json(config.model_dump_json(indent=2))


@cli.command(name="show", help="Exibe a configuração atual da biblioteca.")
def show():
    # Tenta carregar configurações
    if Config.local_file_path().exists():
        try:
            config = get_config()
        except:
            return -1

        console.print_json(config.model_dump_json(indent=2))
        return

    console.print("[warning]Nenhuma configuração encontrada.[/]")


@cli.command(name="validate", help="Valida as configurações atuais.")
def validate():
    if not Config.local_file_path().exists():
        console.print(
            "[warning]Configuração não encontrada. "
            "Use `aibox-dl config setup` para inicializar.[/]"
        )
        return

    try:
        config = get_config()
    except:
        return -1

    for bucket_url in [config.bronze_bucket, config.silver_bucket, config.gold_bucket]:
        bucket = str(bucket_url)
        try:
            get_bucket(bucket)
        except Exception as e:
            console.print(f"[error]Não foi possível accesar o bucket '{bucket}': {e}[/]")
            console.print(
                "[warning]Confirme que possui acesso ao bucket ou " "atualize as configurações.[/]"
            )
            return -1

    console.print("[info]Configurações válidas![/]")
