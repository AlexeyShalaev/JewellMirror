import logging
from dataclasses import dataclass

from pymongo import MongoClient

from MusicPlayer.config import load_config

config = load_config()  # config
logger = logging.getLogger(__name__)  # logging

db = MongoClient(config.db.conn).jewell_mirror  # jewell_mirror - название БД

logger.info('Database engine inited')


@dataclass
class MongoDBResult:
    # Класс для возврата данных
    success: bool
    data: ...
