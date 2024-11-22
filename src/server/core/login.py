from config import logger_config
from server.database.db_connection import get_db
from server.database.db_create import User
from dotenv import load_dotenv
import logging
import logging.config
import jwt
import datetime
import os


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

logger = logging.getLogger('server')
logging.config.dictConfig(logger_config)



def user_login(data):
    db = next(get_db())
    name = data.get('name')
    logger.info(f"Получил на вход name: {name}")

    email = data.get('email')
    logger.info(f"Получил на вход email: {email}")

    password = data.get('password')
    logger.info(f"Получил на вход password: {password}")

    remember_me = data.get('remember_me', False)
    logger.info(f"Запоминалка: {remember_me}")

    user = db.query(User).filter(User.email == email).first()

    if not user or not user.check_password(password):
        logger.warning(f"Пользователя нет в БД!")
        return {'error': 'Invalid email or password'}, 401

    # Устанавливаем срок действия токена
    expiration = datetime.timedelta(days=30 if remember_me else 1)
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + expiration
    }, SECRET_KEY, algorithm='HS256')

    return {'token': token}, 200