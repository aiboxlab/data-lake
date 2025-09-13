"""Client para interação
com o Data Lake.
"""

from enum import Enum

from .config import Config
from .core import Blob, Bucket, MetadataEntry, OpenMetadataJson, StructuredDataSource
from .factory import get_bucket


class BucketKind(Enum):
    bronze = "bronze"
    silver = "silver"
    gold = "gold"

    @classmethod
    def from_str(cls, value: str) -> "BucketKind":
        return next(k for k in cls if k.value == value or k.name == value)


class Client:
    """Classe para interação com
    o Data Lake.


    Permite acessar todas as funcionalidades
    do Data Lake, incluindo o carregamento
    de datasets, listagem de objetos, gerenciamento
    de metadados, entre outros.
    """

    def __init__(self, config: Config | None = None):
        self._config = config if config is not None else Config()
        self._buckets = {
            k: get_bucket(str(getattr(self.config, f"{k.value}_bucket"))) for k in BucketKind
        }
        self._metadata = {
            k: OpenMetadataJson.load_from_bucket(bucket) for k, bucket in self._buckets.items()
        }

    @property
    def config(self) -> Config:
        return self._config

    @property
    def buckets(self) -> dict[BucketKind, Bucket]:
        return self._buckets

    @property
    def metadata(self) -> dict[BucketKind, OpenMetadataJson]:
        return self._metadata

    def list_objects(
        self,
        bucket: BucketKind | str,
        prefix: str | None = None,
        glob: str | None = None,
    ) -> list[Blob]:
        """Lista todos os objetos em
        um dos buckets do Data Lake
        que satisfaçam os filtros.

        Args:
            bucket: bucket para listagem dos
                objetos. Aceita o tipo do bucket
                como string ou `BucketKind` ou um
                objeto `Bucket`.
            prefix: prefixo dos objetos.
            glob: glob para match de objetos.

        Returns:
            list[Blob]: objetos que satisfazem
                os filtros.
        """
        bucket = self._maybe_convert_to_bucket(bucket)
        return bucket.list(prefix=prefix, glob=glob)

    def load_structured_data_source(
        self, source: MetadataEntry | str, bucket: BucketKind | str
    ) -> StructuredDataSource:
        """Carrega uma fonte de dados estruturada
        através de um identificador da fonte de dados
        e o bucket.

        Args:
            source: identificador da fonte de dados.
                Pode ser o caminho para a fonte de
                dados como string ou um objeto de
                metadados.
            bucket: bucket que contém a fonte de
                dados. Aceita o tipo do bucket
                como string ou `BucketKind`.

        Returns:
            StructuredDataSource: fonte de dados
                estruturado.
        """
        if isinstance(bucket, str):
            bucket = BucketKind.from_str(bucket)

        if isinstance(source, str):
            metadata = self.metadata[bucket]
            target = None

            for entry in metadata.entries:
                if entry.dataPath == source:
                    target = entry
                    break

            if target is None:
                raise ValueError(f"Data source '{source}' not found.")

            source = target

        return StructuredDataSource(metadata=source, bucket=self.buckets[bucket])

    def _maybe_convert_to_bucket(self, value: Bucket | BucketKind | str) -> Bucket:
        if isinstance(value, str):
            value = BucketKind.from_str(value)

        if isinstance(value, BucketKind):
            value = self.buckets[value]

        return value
