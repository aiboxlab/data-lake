"""CLI da biblioteca."""

import typer

from .bucket import cli as bucket
from .config import cli as config
from .metadata import cli as metadata

cli = typer.Typer(no_args_is_help=True, add_completion=False, help="CLI do AiBox Data Lake.")


cli.add_typer(config, name="config")
cli.add_typer(bucket, name="bucket")
cli.add_typer(metadata, name="metadata")


if __name__ == "__main__":
    cli()
