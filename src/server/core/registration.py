from config import logger_config
from email_validator import validate_email, EmailNotValidError
from server.database.tables import User
from flask import make_response, Response
from http import HTTPStatus
from typing import Any

import logging
import logging.config


log = logging.getLogger('server')
logging.config.dictConfig(logger_config)

def is_valid_email(email: str) -> bool:
    """
    Проверяет, валидная ли введённая почта.
        Параметры:
            email (str): Потенциальный email

        Возвращает:
            bool: Валидная (True) или Невалидная (False)
    """
    try:
        validate_email(email)
        return True
    except EmailNotValidError as e:
        log.warning(f"Невалидная почта: {e}")
        return False

def is_valid_password(password: str) -> bool:
    """
    Проверяет, валидный ли введённый пароль.
        Параметры:
            password (str): Потенциальный пароль

        Возвращает:
            bool: Валидный (True) или Невалидный (False)
    """
    if len(password) >= 4:
        return True
    else:
        log.warning(f"Невалидный пароль")
        return False

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
    log.debug(f"Получил на вход name: {name}")
    
    email = data.get('email')
    log.debug(f"Получил на вход email: {email}")

    password = data.get('password')
    log.debug(f"Получил на вход пароль: {password}")

    log.debug(f"Проверяю, являются ли введённые данные почтой и паролем")
    if not is_valid_email(email):
        response = make_response({'error': 'Invalid email'}, HTTPStatus.CONFLICT)
        return response

    if not is_valid_password(password):
        response = make_response({'error': 'Invalid password: Need at least 4 characters'}, HTTPStatus.CONFLICT)
        return response

    log.debug(f"Проверяю, существует ли почта: {email} в БД")
    if User.check_user_existence(email):
        response = make_response({'error': 'Email already registered'}, HTTPStatus.CONFLICT)
        return response

    log.debug(f"Проверяю, существует ли имя: {name} в БД")
    if User.check_user_existence(name):
        response = make_response({'error': 'Username already registered'}, HTTPStatus.CONFLICT)
        return response

    try:
        user_id = User.create(name, email, password)
        log.info(f"Пользователь c id: {user_id} зарегистрирован")
        return make_response({'message': 'User registered successfully'}, HTTPStatus.CREATED)
    except Exception as e:
        log.error(f"Не удалось создать нового пользователя! {e}")
        return make_response({'error': f"User not registered... {e}"}, HTTPStatus.BAD_REQUEST)
    

