<h1 align="center">
  <br>
  <a href="https://aiboxlab.org/en/"><img src="https://aiboxlab.org/img/logo-aibox.png" alt="AiBox Lab" width="200"></a>
  <br>
  aibox-data-lake
  <br>
</h1>

<h4 align="center">AiBox Data Lake Toolkit.</h4>


[![Python](https://img.shields.io/pypi/pyversions/aibox-data-lake.svg)](https://badge.fury.io/py/aibox-data-lake)
[![PyPI](https://badge.fury.io/py/aibox-data-lake.svg)](https://badge.fury.io/py/aibox-data-lake)

# Quickstart

The AiBox Data Lake Toolkit is a slim library that provides uniform access to Medallion Data Lakes, with [OpenMetadata](https://docs.open-metadata.org/latest/connectors/storage), on Cloud Providers (e.g., GCP). This library is developed for internal usage, but most of the source code and standards adopted are common for other purposes.

The library can be installed with your favorite package manager:

```sh
uv add aibox-data-lake
uv pip install aibox-data-lake
pip install aibox-data-lake
```

Once installed, the library must be configured by running `aibox-dl config setup`. The CLI will prompt for the buckets URL, and validate that the cloud credentials are available, and the user has sufficient permission to read the buckets' and its contents. The cloud credentials are configured by the cloud client libraries (e.g., `google-cloud-storage`, `boto3`). The CLI provides other features such as listing objects, and reading the bucket metadata.

The library is built on top of the [OpenMetadata JSON Manifest](https://docs.open-metadata.org/latest/connectors/storage), which describes the path and layout of data sources stored on a given bucket.

The main class for programmatic access and manipulation of the Data Lake is the [aibox.data_lake.Client](./src/aibox/data_lake/client.py). This class provides methods for common operations on the Data Lake, such as reading specific files or loading datasets. Example usage:

```python
from aibox.data_lake import Client

# Load the configuration and authenticates
#   to the cloud providers.
client = Client()

# List all objects present on the
#   bronze-tier bucket
client.list_objects("bronze")

# Loads a structured data source (e.g.,
#   .parquet, .csv).
ds = client.load_structured_data_source("<relative-path-to-root>", "bronze")

# A structured data source can be easily
#   loaded to a DataFrame
ds.load()
```
