"""Implementações das interfaces
básicas para o GCP.
"""

from io import BytesIO
from pathlib import Path

from google.cloud import storage

from .core import Blob, Bucket

_CLIENT = storage.Client()


class GCSBlob(Blob):
    def __init__(self, blob: storage.Blob):
        self._blob = blob

    @property
    def bucket(self) -> Bucket:
        return GCSBucket(self._blob.bucket.name)

    @property
    def name(self) -> str:
        return self._blob.name

    def filename(self) -> str:
        return self.name.split("/")[-1]

    def download_to_local(self, directory: Path, overwrite: bool = False) -> Path:
        directory.mkdir(parents=True, exist_ok=True)
        fpath = directory.joinpath(self.filename())
        if fpath.exists() and not overwrite:
            raise ValueError("File already exists: {fpath}.")

        self._blob.download_to_filename(str(fpath), client=_CLIENT)
        return fpath

    def as_stream(self) -> BytesIO:
        return BytesIO(self._blob.download_as_bytes(client=_CLIENT))


class GCSBucket(Bucket):
    def __init__(self, bucket_name: str):
        super().__init__(bucket_name)
        self._bucket = _CLIENT.bucket(bucket_name)
        if not self._bucket.exists():
            raise ValueError(f"Bucket '{bucket_name}' not found.")

    def list(self, prefix: str | None = None, glob: str | None = None) -> list[Blob]:
        return [GCSBlob(blob) for blob in self._bucket.list_blobs(prefix=prefix, match_glob=glob)]

    def get(self, name: str) -> Blob:
        return GCSBlob(self._bucket.get_blob(name))
