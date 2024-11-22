from config import logger_config
from server.database.db_connection import get_db
from server.database.db_create import Mod
import logging
import logging.config


logger = logging.getLogger('server')
logging.config.dictConfig(logger_config)

def fetch_all_mods():
    db = next(get_db())
    mods = db.query(Mod).order_by(Mod.version.desc()).all()
    logger.info("Отправил моды на сайт")
    return mods
