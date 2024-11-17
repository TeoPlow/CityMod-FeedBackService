from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL, logger_config
import logging
import logging.config


logger = logging.getLogger('server')
logging.config.dictConfig(logger_config)

engine = create_engine(DATABASE_URL)
logger.info(f"Создал движок по адресу: {DATABASE_URL}")

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

def get_db():
    logging.info(f"Запрос к БД")
    db = Session()
    try:
        yield db
    finally:
        db.close()
