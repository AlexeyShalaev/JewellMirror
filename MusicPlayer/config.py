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
class DbConfig:
    conn: str  # connection string to database


@dataclass
class Config:  # class config
    flask: FlaskConfig
    db: DbConfig
    api_key: str
    songs_path: str


def load_config(path: str = ".env"):
    env = Env()
    env.read_env(path)

    return Config(
        flask=FlaskConfig(
            secret_key=env.str('SECRET_KEY'),
            app_name=env.str('APP_NAME'),
        ),
        db=DbConfig(
            conn=env.str('DB_CONN')
        ),
        songs_path=env.str('SONGS_PATH'),
        api_key=env.str('API_KEY')
    )
