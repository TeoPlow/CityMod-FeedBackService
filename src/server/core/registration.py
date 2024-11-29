from config import logger_config
from server.database.tables import User
from flask import make_response, Response
from http import HTTPStatus
from typing import Any

import logging
import logging.config


logger = logging.getLogger('server')
logging.config.dictConfig(logger_config)


def user_register(data: dict[str, Any]) -> Response:
    """
    Выполняет регистрацию пользователя, добавляя его данные в БД.
        Параметры:
            data: Словарь в формате response.json с инфой
                  о name, email и password.

        Возвращает:
            Ответ от сервера: {message, code}
    """
    name = data.get('name')
    logger.info(f"Получил на вход name: {name}")
    
    email: str = data.get('email').lower()
    logger.info(f"Получил на вход email: {email}")

    password = data.get('password')
    logger.info(f"Получил на вход password: {password}")

    if User.check_user_existence(email):
        response = make_response({'error': 'Email already registered'}, HTTPStatus.CONFLICT)
        return response

    if User.check_user_existence(name):
        response = make_response({'error': 'Username already registered'}, HTTPStatus.CONFLICT)
        return response

    try:
        user_id = User.create(name, email, password)
        logger.info(f"Пользователь c id: {user_id} зарегистрирован")
        return make_response({'message': 'User registered successfully'}, HTTPStatus.CREATED)
    except Exception as e:
        logger.error(f"Не удалось создать нового пользователя!")
        return make_response({'message': 'User not registered...'}, HTTPStatus.BAD_REQUEST)
    

