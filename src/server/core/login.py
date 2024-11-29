from config import logger_config
from server.database.tables import User
from server.handlers.get_user_id import get_user_id
from functools import wraps
from flask import request, make_response, Response, redirect, url_for
from http import HTTPStatus
from dotenv import load_dotenv
from typing import Any
import jwt
import datetime
import os

import logging
import logging.config


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

log = logging.getLogger('server')
logging.config.dictConfig(logger_config)


def user_login(data: dict[str, Any]) -> Response:
    """
    Выполняет авторизацию пользователя,
    проверяя наличие вводимых данных в БД
    и устанавливая токен в куке для сохранения авторизации.
        Параметры:
            data: Словарь в формате response.json с инфой
                  о email_or_name, password и remember_me.

        Возвращает:
            Ответ от сервера : {message, code}
    """
    email_or_name = data.get('email_or_name')
    log.debug(f"Получил на вход email or name: {email_or_name}")

    password = data.get('password')
    log.debug(f"Получил на вход password: {password}")

    remember_me = data.get('remember_me', False)
    log.debug(f"Запоминалка: {remember_me}")

    user_id = User.check_user_existence(email_or_name)[0]['id']
    log.debug(f"Получил user_id: {user_id}")

    if not user_id or not User.check_password(user_id, password):
        log.warning(f"Пользователя нет в БД!")
        return make_response({'error': 'Invalid email, name or password'}, HTTPStatus.NOT_FOUND)

    # Устанавливаем срок действия токена
    expiration = datetime.timedelta(days=30 if remember_me else 1)
    token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + expiration
    }, SECRET_KEY, algorithm='HS256')

    # Создаем ответ с токеном в куке
    response = make_response({'token': token}, HTTPStatus.OK)
    response.set_cookie(
        'auth_token', token, 
        httponly=True, 
        secure=True, 
        max_age=expiration.total_seconds()
    )

    return response


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            request.user_id = get_user_id()
        except:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function