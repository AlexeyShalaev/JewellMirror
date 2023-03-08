from dataclasses import dataclass

from environs import Env


@dataclass
class FlaskConfig:
    """
    import secrets
    print(secrets.token_hex(16))
    """
    secret_key: str  # app secret key
    app_name: str  # flask app name


@dataclass
class Authentication:
    login: str
    password: str


@dataclass
class DbConfig:
    conn: str  # connection string to database


@dataclass
class API:
    jewell: str


@dataclass
class Links:
    jewell: str


@dataclass
class Config:  # class config
    flask: FlaskConfig
    auth: Authentication
    db: DbConfig
    api: API
    links: Links


def load_config(path: str = ".env"):
    env = Env()
    env.read_env(path)

    return Config(
        flask=FlaskConfig(
            secret_key=env.str('SECRET_KEY'),
            app_name=env.str('APP_NAME'),
        ),
        auth=Authentication(
            login=env.str('AUTH_LOGIN'),
            password=env.str('AUTH_PASSWORD'),
        ),
        db=DbConfig(
            conn=env.str('DB_CONN')
        ), api=API(
            jewell=env.str('JEWELL_TOKEN')
        ),
        links=Links(
            jewell=env.str('URL_JEWELL')
        )
    )
