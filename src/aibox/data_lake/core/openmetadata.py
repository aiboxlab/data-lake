"""Metadados sobre organização
dos buckets através do OpenMetadata.
"""

import json
from typing import Optional

from pydantic import BaseModel, Field

from .bucket import Bucket


class PartitionColumn(BaseModel):
    """Configuração mínima de uma
    coluna de partição.
    """

    name: str = Field(description="Local name (not fully qualified) of the column.")
    dataType: str = Field(description="Data type of the column (e.g., INT, STRING, etc.).")
    displayName: Optional[str] = Field(None, description="Display name for the column.")


class MetadataEntry(BaseModel):
    """Entrada de metadados para
    o OpenMetadataJson.
    """

    dataPath: str = Field(
        description="The path where the data resides in the container, "
        "excluding the bucket name.",
    )
    structureFormat: Optional[str] = Field(
        None,
        description="What’s the schema format for the container, e.g. " "avro, parquet, csv.",
    )
    unstructuredFormats: Optional[list[str]] = Field(
        None,
        description="What unstructured formats you want to ingest, " "e.g. png, pdf, jpg.",
    )
    depth: int = Field(0, description="Depth of the data path in the container")
    separator: Optional[str] = Field(
        None,
        description="For delimited files such as CSV, what is the " "separator being used?",
    )
    isPartitioned: bool = Field(
        False,
        description="Flag indicating whether the container's data is partitioned",
    )
    partitionColumns: Optional[list[dict]] = Field(
        None, description="List of partition columns if data is partitioned"
    )


class OpenMetadataJson(BaseModel):
    """OpenMetadata JSON manifest.

    Para mais informações, ver:
    https://docs.open-metadata.org/latest/connectors/storage
    """

    entries: list[MetadataEntry] = Field(
        description="List of metadata entries for the bucket containing "
        "information about where data resides and its structure"
    )

    @classmethod
    def load_from_bucket(cls, bucket: Bucket) -> "OpenMetadataJson":
        """Carrega os metadados a partir
        de um Bucket.

        Deve existir um `openmetadata.json`
        na raiz do bucket.

        Args:
            bucket: bucket para carregamento
                dos metadados.

        Returns:
            OpenMetadataJson: metadados.
        """
        return cls(**json.load(bucket.get("openmetadata.json").as_stream()))
