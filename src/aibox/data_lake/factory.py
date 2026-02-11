"""Métodos factory da
biblioteca.
"""

from .core import Bucket


def get_bucket(bucket_url: str) -> Bucket:
    """Obtém um objeto bucket a
    partir de uma URL com schema
    (e.g., `gs://`, `s3://`).

    Args:
        bucket_url: URL para o
            bucket.

    Returns:
        Bucket: bucket.

    Raises:
        ValueError: se a URL não
            é suportada.
    """
    prefix = "gs://"
    if bucket_url.startswith(prefix):
        from .gcp import GCSBucket

        return GCSBucket(bucket_url.lstrip(prefix))

    prefix = "s3://"
    if bucket_url.startswith(prefix):
        from .s3 import S3Bucket

        return S3Bucket(bucket_url.lstrip(prefix))

    raise ValueError(f"Unsupported bucket URL: '{bucket_url}'")
