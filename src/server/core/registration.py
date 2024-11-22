from config import logger_config
from server.database.db_connection import get_db
from server.database.db_create import User
import logging
import logging.config
import jwt
import datetime


logger = logging.getLogger('server')
logging.config.dictConfig(logger_config)


def user_register(data):
    db = next(get_db())
    name = data.get('name')
    logger.info(f"Получил на вход name: {name}")
    
    email = data.get('email')
    logger.info(f"Получил на вход email: {email}")

    password = data.get('password')
    logger.info(f"Получил на вход password: {password}")

    if db.query(User).filter(User.email == email).first():
        return {'error': 'Email already registered'}, 400

    new_user = User(name=name, email=email)
    new_user.set_password(password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info("Пользователь зарегестрирован")

    return {'message': 'User registered successfully'}, 201

