from dotenv import find_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    def __init__(self, env_file):
        super().__init__(_env_file=env_file, _case_sensitive=True, )
    STORAGE_SECRET: str = Field()
    API_SERVER_ADDRESS: str = Field()
    API_SERVER_PORT: int = Field()
    API_VERSION: str = Field()
    HTTP_PROTOCOL: str = Field()
    LOG_DIR: str = Field()
    ENVIRONMENT: str = Field()

    class Config:
        validate_assignment = True


envs = find_dotenv('.env', raise_error_if_not_found=True)
settings = Settings(env_file=envs)
