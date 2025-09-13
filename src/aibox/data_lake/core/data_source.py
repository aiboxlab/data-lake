"""Fontes de dados."""

import pandas as pd

from .bucket import Blob, Bucket
from .openmetadata import MetadataEntry


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

        self._metadata = metadata
        self._bucket = bucket
        self._blobs = self._bucket.list(
            prefix=self._metadata.dataPath,
            glob=f"**/*.{self._metadata.structureFormat}",
        )

        if not self._blobs:
            raise ValueError(f"Data source not found on bucket {self._bucket.name}.")

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
