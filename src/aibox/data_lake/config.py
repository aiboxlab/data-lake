"""Configurações da biblioteca."""

from pathlib import Path

import platformdirs
from pydantic import AnyUrl
from pydantic_settings import BaseSettings, JsonConfigSettingsSource


class BucketUrl(AnyUrl):
    """Modelo que aceita URLs
    de buckets.
    """

    allowed_schemes = {"s3", "gs"}


class Config(BaseSettings):
    model_config = {"env_prefix": "AIBOX_DL_"}

    bronze_bucket: BucketUrl
    silver_bucket: BucketUrl
    gold_bucket: BucketUrl

    def save_to_file(self):
        """Save current settings to the default
        settings JSON location.
        """
        path = self.local_file_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.model_dump_json(indent=2), encoding="utf-8")

    @classmethod
    def local_file_path(cls) -> Path:
        """Get the config local path.

        Returns:
            Path: path to configuration file.
        """
        return Path(platformdirs.user_config_dir(appname="data_lake", appauthor="aibox")).joinpath(
            "config.json"
        )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        # Precedence order
        return (
            init_settings,
            JsonConfigSettingsSource(settings_cls, json_file=cls.local_file_path()),
            env_settings,
            file_secret_settings,
        )
