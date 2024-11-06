from pydantic import Field

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class RedisConfig(BaseConfig):
    redis_host: str = Field(env="REDIS_HOST")
    redis_port: int = Field(env="REDIS_PORT")


class KafkaConfig(BaseConfig):
    bootstrap_servers: str = Field(field="BOOTSTRAP_SERVERS")


class ServerConfig(BaseConfig):
    redis: RedisConfig = RedisConfig()
    kafka: KafkaConfig = KafkaConfig()


class Settings:
    conf: ServerConfig = ServerConfig()

    def setup(self):
        return self


server = Settings().setup()