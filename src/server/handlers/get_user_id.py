from flask import request, redirect, url_for
from config import logger_config
from dotenv import load_dotenv
import jwt
import os

import logging
import logging.config


logger = logging.getLogger('server')
logging.config.dictConfig(logger_config)

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def get_user_id():
    token = request.cookies.get('auth_token')
    if not token:
        return redirect(url_for('login'))

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('user_id')
        return user_id
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login'))
    except jwt.InvalidTokenError:
        return redirect(url_for('login'))