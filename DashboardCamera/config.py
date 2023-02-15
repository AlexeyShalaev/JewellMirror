from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    conn: str  # connection string to database


@dataclass
class Config:  # class config
    db: DbConfig


def load_config(path: str = ".env"):
    env = Env()
    env.read_env(path)

    return Config(
        db=DbConfig(
            conn=env.str('DB_CONN')
        )
    )
