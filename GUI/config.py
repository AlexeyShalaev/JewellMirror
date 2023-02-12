from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    conn: str  # connection string to database


@dataclass
class FlaskConfig:
    """
    import secrets
    print(secrets.token_hex(16))
    """
    secret_key: str  # app secret key
    api_token: str  # api secret key
    app_name: str  # flask app name


@dataclass
class Config:  # class config
    db: DbConfig
    flask: FlaskConfig


def load_config(path: str = ".env"):
    env = Env()
    env.read_env(path)

    return Config(
        db=DbConfig(
            conn=env.str('DB_CONN'),
        ),
        flask=FlaskConfig(
            secret_key=env.str('SECRET_KEY'),
            api_token=env.str('API_TOKEN'),
            app_name=env.str('APP_NAME'),
        )
    )
