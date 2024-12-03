from config import logger_config, UnauthorizedError
from flask import request
from dotenv import load_dotenv
import jwt
import os

import logging
import logging.config


log = logging.getLogger('server')
logging.config.dictConfig(logger_config)

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


def get_user_id() -> int:
    """
    Получает ID пользователя через jwt токен.
        Возвращает:
            ID пользователя.
    """
    log.debug("Получаю ID пользователя из браузера")
    token = request.cookies.get('auth_token')
    if not token:
        log.debug(f"ID пользователя НЕ получен")
        raise UnauthorizedError("User not logged in")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id: int = payload.get('user_id')
        log.debug(f"ID пользователя получен успешно: {user_id}")
        return user_id
    except jwt.ExpiredSignatureError as e:
        log.warning(f"ID пользователя НЕ получен: {e}")
        raise UnauthorizedError("Expired token")
    except jwt.InvalidTokenError as e:
        log.warning(f"ID пользователя НЕ получен: {e}")
        raise UnauthorizedError("Invalid token")