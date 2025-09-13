"""Interface para interação com
buckets.
"""

from abc import ABC, abstractmethod
from io import BytesIO
from pathlib import Path


class Blob(ABC):
    """Interface para objetos
    armazenados em buckets.

    Essa classe não armazena o
    conteúdo de um objeto diretamente,
    apenas uma referência para o objeto
    dentro do bucket.

    Para acessar o conteúdo, algum dos
    métodos de leitura deve ser utilizado.
    """

    @property
    @abstractmethod
    def bucket(self) -> "Bucket":
        return self._bucket

    @property
    @abstractmethod
    def name(self) -> str:
        return self._name

    @abstractmethod
    def download_to_local(self, directory: Path, overwrite: bool = False) -> Path:
        """Realiza a transferência do objeto
        remoto para um arquivo local.

        Args:
            directory: caminho para o
                diretório onde o objeto
                deve ser armazenado.
            overwrite: se o arquivo deve
                ser sobrescrito casa exista.

        Returns:
            Path: caminho para o objeto
                localmente.
        """

    @abstractmethod
    def as_stream(self) -> BytesIO:
        """Retorna o objeto como
        uma stream de bytes.

        Returns:
            BytesIO: conteúdo do
                objeto.
        """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}" f"(name='{self.name}', bucket" f"='{self.bucket.name}')"


class Bucket(ABC):
    """Interface para buckets.

    Um bucket é um container para
    diferentes objetos, com tipos
    e formatos variados.
    """

    def __init__(self, bucket_name: str):
        self._name = bucket_name

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def list(self, prefix: str | None = None, glob: str | None = None) -> list[Blob]:
        """Realiza uma listagem de todos os
        objetos presentes no bucket.

        Args:
            prefix: prefixo para filtragem
                dos blobs. Padrão é sem
                filtros.
            glob: GLOB para filtragem dos
                blobs. Padrão é sem filtros.

        Returns:
            list[Blob]: objetos presentes
                no bucket.
        """

    @abstractmethod
    def get(self, name: str) -> Blob:
        """Obtém um objeto no bucket
        com o nome passado.

        Args:
            name: nome do objeto.

        Returns:
            Blob: objeto.
        """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
