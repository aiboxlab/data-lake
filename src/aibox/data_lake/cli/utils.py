"""Utilidades para o CLI."""

from pydantic import ValidationError
from rich.console import Console
from rich.theme import Theme

from aibox.data_lake.client import Client
from aibox.data_lake.config import Config

console = Console(
    theme=Theme(
        {
            "success": "green bold",
            "error": "red bold",
            "warning": "yellow",
            "info": "cyan",
        }
    )
)


def get_config() -> Config:
    try:
        return Config()
    except (ValidationError, Exception) as e:
        console.print(f"[error]Não foi possível carregar as configurações: {e}[/]")
        raise


def get_client() -> Client:
    return Client(config=get_config())
