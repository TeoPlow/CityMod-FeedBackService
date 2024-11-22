from config import logger_config
from server.database.db_connection import get_db
from server.database.db_create import User
from server.handlers.get_user_id import get_user_id
from functools import wraps
from flask import request, redirect, url_for, jsonify, make_response
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

    email_or_name = data.get('email_or_name')
    logger.info(f"Получил на вход email or name: {email_or_name}")

    password = data.get('password')
    logger.info(f"Получил на вход password: {password}")

    remember_me = data.get('remember_me', False)
    logger.info(f"Запоминалка: {remember_me}")

    user = db.query(User).filter(User.email == email_or_name).first()
    if not user:
        user = db.query(User).filter(User.name == email_or_name).first()

    if not user or not user.check_password(password):
        logger.warning(f"Пользователя нет в БД!")
        response = make_response({'error': 'Invalid email, name or password'}, 401)
        return response

    # Устанавливаем срок действия токена
    expiration = datetime.timedelta(days=30 if remember_me else 1)
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + expiration
    }, SECRET_KEY, algorithm='HS256')

    # Создаем ответ с токеном в куке
    response = make_response({'token': token}, 200)
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
        request.user_id = get_user_id()
        return f(*args, **kwargs)
    return decorated_function