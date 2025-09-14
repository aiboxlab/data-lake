"""Fontes de dados."""

import logging
from typing import Literal

import pandas as pd
from pydantic import BaseModel

from .bucket import Blob, Bucket
from .openmetadata import MetadataEntry

LOGGER = logging.getLogger(__name__)


class SourceInfo(BaseModel):
    name: str
    partioned: bool
    kind: Literal["structured", "unstructured"]

    @classmethod
    def from_metadata(cls, value: MetadataEntry) -> "SourceInfo":
        return cls(
            name=value.dataPath,
            partioned=value.isPartitioned,
            kind="structured" if value.structureFormat is not None else "unstructured",
        )


class StructuredDataSource:
    """Fonte de dados estruturados
    sem particionamento.

    Essa classe representa um dataset
    logicamente: conjunto de arquivos
    em um bucket associados com metadados.
    """

    def __init__(self, metadata: MetadataEntry, bucket: Bucket):
        if metadata.structureFormat not in {"parquet", "csv"}:
            raise ValueError("Data source not supported.")

        if metadata.isPartitioned:
            raise ValueError("Partitioned data sources aren't supported.")

        if metadata.depth != 0:
            LOGGER.warning(
                "Depth is currently ignored. All strucuted files "
                "matching the expected type are loaded."
            )

        self._metadata = metadata
        self._bucket = bucket
        self._blobs = self._bucket.list(
            prefix=f"{self._metadata.dataPath}/",
            glob=f"**/*.{self._metadata.structureFormat}",
        )

        if not self._blobs:
            raise ValueError(f"Data source not found on bucket {self._bucket.name}.")

    @property
    def info(self) -> SourceInfo:
        return SourceInfo.from_metadata(self.metadata)

    @property
    def metadata(self) -> MetadataEntry:
        return self._metadata

    @property
    def bucket(self) -> Bucket:
        return self._bucket

    @property
    def blobs(self) -> list[Blob]:
        return self._blobs

    def load(self) -> pd.DataFrame:
        """Realiza o carregamento da
        fonte dados em um DataFrame.

        Returns:
            pd.DataFrame: DataFrame.
        """
        # Seleciona o método de carregamento
        load = (
            pd.read_parquet if self.metadata.structureFormat.lower() == "parquet" else pd.read_csv
        )

        # Carregamento de todos os blobs
        dfs = []
        for blob in self.blobs:
            dfs.append(load(blob.as_stream()))
        return pd.concat(dfs, ignore_index=True)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(dataPath="
            f"'{self.metadata.dataPath}', bucket='{self.bucket.name}')"
        )
