"""CLI para interação
baixo nível com buckets.
"""

import typer

from aibox.data_lake.client import BucketKind

from .utils import console, get_client

cli = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    help="Leitura de objetos armazenados em buckets.",
)


@cli.command(name="list-objects", help="Lista todos objetos de um bucket.")
def list_objects(
    bucket: BucketKind = typer.Option(
        help="Nível do bucket a ser utilizado (bronze, silver, gold)."
    ),
    prefix: str = typer.Option(None, help="Prefixo para filtragem de objetos."),
    glob: str = typer.Option(None, help="Glob para filtragem de objetos."),
):
    client = get_client()
    bucket = client.buckets[bucket]
    objects = client.list_objects(bucket, prefix, glob)
    console.print(f"[info]{bucket.name}:[/]")
    if objects:
        for obj in objects:
            console.print(obj)
    else:
        console.print("[warning]Nenhum objeto encontrado.[/]")
