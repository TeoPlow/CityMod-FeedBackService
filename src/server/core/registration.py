from config import logger_config
from server.database.tables import User
from flask import make_response, Response
from http import HTTPStatus
from typing import Any

import logging
import logging.config


log = logging.getLogger('server')
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
    log.info(f"Получил на вход name: {name}")
    
    email = data.get('email')
    log.info(f"Получил на вход email: {email}")

    password = data.get('password')
    log.info(f"Получил на вход password: {password}")

    if User.check_user_existence(email):
        response = make_response({'error': 'Email already registered'}, HTTPStatus.CONFLICT)
        return response

    if User.check_user_existence(name):
        response = make_response({'error': 'Username already registered'}, HTTPStatus.CONFLICT)
        return response

    try:
        user_id = User.create(name, email, password)
        log.info(f"Пользователь c id: {user_id} зарегистрирован")
        return make_response({'message': 'User registered successfully'}, HTTPStatus.CREATED)
    except Exception as e:
        log.error(f"Не удалось создать нового пользователя! {e}")
        return make_response({'message': f"User not registered... {e}"}, HTTPStatus.BAD_REQUEST)
    

