"""CLI para interação
com metadados.
"""

import typer

from aibox.data_lake.client import BucketKind

from .utils import console, get_client

cli = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    help="Interação com metadados dos buckets.",
)


@cli.command(name="get-metadata", help="Obtém os metadados de um bucket.")
def get_metadata(
    bucket: BucketKind = typer.Option(
        help="Nível do bucket a ser utilizado (bronze, silver, gold)."
    ),
):
    client = get_client()
    metadata = client.metadata[bucket]
    bucket = client.buckets[bucket]
    console.print(f"[info]{bucket.name}[/]:")
    console.print_json(metadata.model_dump_json(indent=2))
