import logging
import logging.config
from config import logger_config
from server.database.db_create import update_database, User

from server.database.db_connection import get_db


logger = logging.getLogger('server')
logging.config.dictConfig(logger_config)

update_database()


db = next(get_db())  # Получаем сессию

new_user = User(name="Egor", email="egor@example.com")
db.add(new_user)
db.commit()  # Фиксируем изменения
db.refresh(new_user)  # Обновляем объект с ID из БД
logger.info(f"Добавил пользователя: {new_user}")