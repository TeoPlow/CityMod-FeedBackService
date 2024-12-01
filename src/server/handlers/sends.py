from config import logger_config, UnauthorizedError
from server.database.tables import Feedback, File
from server.handlers.get_user_id import get_user_id
from flask import url_for, make_response, Response
from http import HTTPStatus
from typing import Any

import logging
import logging.config


log = logging.getLogger('server')
logging.config.dictConfig(logger_config)


def send_feedback_handler(request, file_id: int) -> Response:
    """
    Добавляет feedback от пользователя в БД
        Параметры:
            request: запрос в виде form
            file_id (int): ID файла
        Возвращает:
            Responce об успешном добавлении фидбэка.
    """
    log.debug(f"Добавляю feedback в БД")
    user_id: int = get_user_id()
    feedback_message = request.form.get('feedback')
    feedback_type = request.form.get('feedbackType')
    log.debug(f"Получил на вход {feedback_type}: '{feedback_message}' и файлы c id: {file_id} от пользователя c id: {user_id}")

    feedback_id = Feedback.create(user_id, feedback_type, feedback_message, file_id)

    log.debug(f"Фидбэк c id: {feedback_id} успешно добавлен")
    return make_response({'message': 'The feedback has been add successfully!'}, HTTPStatus.CREATED)