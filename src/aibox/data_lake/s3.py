"""Implementações das interfaces
básicas para o S3.
"""

import fnmatch
from functools import cached_property
from io import BytesIO
from pathlib import Path

import boto3

from .core import Blob, Bucket

_S3_RESOURCE = boto3.resource("s3")


class S3Blob(Blob):
    def __init__(self, bucket_name: str, key: str):
        self._bucket_name = bucket_name
        self._key = key
        self._object = _S3_RESOURCE.Object(self._bucket_name, self._key)
        self._object.load()

    @property
    def bucket(self) -> Bucket:
        return S3Bucket(self._bucket_name)

    @cached_property
    def name(self) -> str:
        return super().name

    @cached_property
    def path(self) -> str:
        return self._key

    @cached_property
    def size(self) -> int:
        return self._object.content_length or 0

    def download_to_local(self, file_path: Path | str, overwrite: bool = False):
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if file_path.exists() and not overwrite:
            raise ValueError(f"File already exists: {file_path}.")

        self._object.download_file(str(file_path))

    def as_stream(self) -> BytesIO:
        buf = BytesIO()
        self._object.download_fileobj(buf)
        buf.seek(0)
        return buf

    def delete(self) -> bool:
        try:
            self._object.delete()
            return True
        except:
            return False


class S3Bucket(Bucket):
    def __init__(self, bucket_name: str):
        super().__init__(bucket_name)
        self._bucket_name = bucket_name
        self._bucket = _S3_RESOURCE.Bucket(bucket_name)
        self._bucket.load()

    @property
    def uri(self) -> str:
        return f"s3://{self._bucket_name}"

    def list(self, prefix: str | None = None, glob: str | None = None) -> list[Blob]:
        objects = self._bucket.objects.filter(Prefix=prefix or "")
        if glob is not None:
            objects = [obj for obj in objects if fnmatch.fnmatch(obj.key, glob)]

        return [S3Blob(self._bucket_name, obj.key) for obj in objects]

    def get(self, name: str) -> Blob | None:
        try:
            return S3Blob(self._bucket_name, name)
        except:
            return None
