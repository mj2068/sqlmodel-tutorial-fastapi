from pydantic import BaseSettings


class Settings(BaseSettings):
    username: str
    password: str
    address: str
    dbname: str
    dbname_test:str
    
    class Config:
        env_prefix = "db_"
        env_file = ".env"


# (https://github.com/pydantic/pydantic/issues/3753)
settings = Settings()  # type: ignore
