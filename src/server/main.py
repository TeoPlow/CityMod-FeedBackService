import logging
import logging.config
from config import logger_config
from server.database.db_create import update_database

from server.database.db_connection import get_db


logger = logging.getLogger('server')
logging.config.dictConfig(logger_config)

