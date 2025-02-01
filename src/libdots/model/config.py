from pydantic import SecretStr
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class ServiceConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=[".env", ".env.docker"])
    simulation_id: str
    model_id: str
    mqtt_host: str = "localhost"
    mqtt_port: int = 1883
    mqtt_qos: int = 0
    mqtt_username: str = ""
    mqtt_password: SecretStr = SecretStr("")
    influxdb_host: str = ""
    influxdb_port: int = 8086
    influxdb_user: str = ""
    influxdb_password: SecretStr = SecretStr("")
    influxdb_name: str = ""
