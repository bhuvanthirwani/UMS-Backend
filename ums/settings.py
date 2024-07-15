import enum
import os
from pathlib import Path
from tempfile import gettempdir
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Environment(str, enum.Enum):
    DEV = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    base_path: str = str(Path(__file__).parent.absolute())
    hot_reload: bool = False

    session_secret: str = "Update .env"
    jwt_secret: str = "Update .env"
    jwt_expiry_hours: int = 24
    jwt_algorithm: str = "HS256"

    # period in hours.
    expiration_period: int = 12
    max_file_size_allowed: int = 5 * 1000 * 1000  # 5 MB

    host: str = "0.0.0.0"
    port: int = 5000
    workers_count: int = 1
    reload: bool = False

    # Current environment
    environment: Environment = os.getenv("env") or Environment.DEV

    log_level: LogLevel = LogLevel.DEBUG

    # Variables for the database
    # db_host: str = "10.10.11.120"
    db_host: str = "127.0.0.1"
    db_port: int = 7000
    db_user: str = "ums"
    db_pass: str = "ums"
    db_base: str = "ums"
    db_echo: bool = False

    # Variables for Redis
    redis_host: str = "ums-redis"
    redis_port: int = 6379
    redis_user: Optional[str] = None
    redis_pass: Optional[str] = None
    redis_base: Optional[int] = None

    # This variable is used to define
    # multiproc_dir. It's required for [uvi|guni]corn projects.
    prometheus_dir: Path = TEMP_DIR / "prom"

    # Sentry's configuration.
    sentry_dsn: Optional[str] = None
    sentry_sample_rate: float = 1.0

    auto_generate_tables: bool = False

    admin_enabled: bool = False
    admin_swatch: str = "cerulean"
    admin_name: str = "Ums"
    admin_template: str = "bootstrap4"
    admin_endpoint: str = "/admin"

    # S3 Configs
    s3_access_key: str = "your-s3-access-key"
    s3_secret_key: str = "your-s3-secret-key"
    s3_url_prefix: str = "https://ums-assets.s3.ap-south-1.amazonaws.com/"

    app5_user_url: str = "http://127.0.0.1:8080/api/v1/app5"
    app2_user_url: str = "http://127.0.0.1:8080/api/v1/user"

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+psycopg2",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    @property
    def redis_url(self) -> URL:
        """
        Assemble REDIS URL from settings.

        :return: redis URL.
        """
        path = f"/{self.redis_base}" if self.redis_base is not None else ""
        return URL.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
            user=self.redis_user,
            password=self.redis_pass,
            path=path,
        )

    # TODO: os.getenv("environment") and select secret file accordingly.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="UMS_",
        env_file_encoding="utf-8",
    )


settings = Settings()
