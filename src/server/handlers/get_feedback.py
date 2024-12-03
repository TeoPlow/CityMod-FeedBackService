from config import logger_config, UnauthorizedError
from server.database.tables import Feedback, File, User
from flask import request
from typing import List
import os

import logging
import logging.config


log = logging.getLogger('server')
logging.config.dictConfig(logger_config)


def get_feedback_handler(feedback_type: str = '') -> List[dict()]:
    """
    Получает фидбэки из БД и редактирует список фидбэков для корректного вывода.
        Параметры:
            feedback_type (str): Тип фидбэка для фильтрации.

        Возвращает:
            List[dict()]: Список словарей, где каждый словарь это фидбэк.
    """
    feedback_list = Feedback.get_feedback(feedback_type=feedback_type)

    for feedback in feedback_list:
        feedback_time = feedback['time'].strftime('%d-%m-%Y %H:%M')
        feedback['time'] = feedback_time

        # Превращаем ID файла в путь до файла
        files_id = feedback['files_id']
        if files_id:
            file_path = File.get_path(feedback['files_id'])
        else:
            file_path = None

        # Превращаем ID пользователя в его имя
        user_id = feedback['user_id']
        if user_id:
            user_name = User.get_name(feedback['user_id'])
        else:
            user_name = None

        # Редактируем тип пользователя в нормальный вид
        feedback_type = feedback['type']
        if feedback_type == 'review':
            feedback_type = 'Review'
        elif feedback_type == 'bug_report':
            feedback_type = 'Bug Report'
        elif feedback_type == 'offer':
            feedback_type = 'Offer'
        else:
            raise UnauthorizedError("Тип не поддерживается!")

        feedback['type'] = feedback_type
        feedback['name'] = user_name
        feedback['file_path'] = file_path

    log.debug(f"Передаю список: {feedback_list}")
    return feedback_list



