"""CLI para configuração
da biblioteca.
"""

import typer
from rich.prompt import Confirm

from aibox.data_lake.config import Config
from aibox.data_lake.factory import get_bucket

from .utils import console, get_config

cli = typer.Typer(
    no_args_is_help=True, add_completion=False, help="Configuração de buckets & acesso."
)


@cli.command(name="setup", help="Configura a biblioteca para primeiro uso.")
def setup(
    bronze_bucket: str = typer.Option(
        help="URL do bucket nível bronze (e.g., gs://<bucket>)."
    ),
    silver_bucket: str = typer.Option(
        help="URL do bucket nível prata (e.g., gs://<bucket>)."
    ),
    gold_bucket: str = typer.Option(
        help="URL do bucket nível ouro (e.g., gs://<bucket>)."
    ),
):
    if Config.local_file_path().exists():
        config = get_config()
        console.print("[info]Configuração encontrada:[/]")
        console.print_json(config.model_dump_json(indent=2))
        if not Confirm.ask(
            "[warning]Deseja sobrescrever?[/]", console=console, default=True
        ):
            console.print("[info]Configuração atual mantida.[/]")
            return

    # Garantindo que os buckets são válidos
    for bucket in [bronze_bucket, silver_bucket, gold_bucket]:
        try:
            get_bucket(bucket)
        except Exception as e:
            console.print(
                f"[error]Não foi possível accesar o bucket '{bucket}': {e}[/]"
            )
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
        config = get_config()
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

    config = get_config()
    for bucket_url in [config.bronze_bucket, config.silver_bucket, config.gold_bucket]:
        bucket = str(bucket_url)
        try:
            get_bucket(bucket)
        except Exception as e:
            console.print(
                f"[error]Não foi possível accesar o bucket '{bucket}': {e}[/]"
            )
            console.print(
                "[warning]Confirme que possui acesso ao bucket ou "
                "atualize as configurações.[/]"
            )
            return -1

    console.print("[info]Configurações válidas![/]")
