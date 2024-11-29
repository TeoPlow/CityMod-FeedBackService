from config import logger_config
from server.database.tables import BugReport, Review, Offer, File
from server.handlers.get_user_id import get_user_id
from flask import url_for, make_response, Response
from http import HTTPStatus
from typing import Any

import logging
import logging.config


log = logging.getLogger('server')
logging.config.dictConfig(logger_config)

def send_review_handler(data: dict[str, Any]) -> Response:
    """
    Добавляет отзыв пользователя в БД
    """
    log.info(f"Добавляю отзыв в БД")
    try:
        review_data = data.get('review')
        user_id = get_user_id()
        log.debug(f"Получил на вход review: '{review_data}' от пользователя c id: {user_id}")

        review_id = Review.create(user_id, review_data)
        log.debug(f"Отзыв {review_id} успешно добавлен")

        return make_response({'message': 'The review has been add successfully!'}, HTTPStatus.CREATED)
    except Exception as e:
        return make_response({'message': 'Something went wrong...'}, HTTPStatus.BAD_REQUEST)
     

def send_bug_report_handler(request, file_id: int) -> Response:
    """
    Добавляет баг репорт от пользователя в БД
    """
    log.info(f"Добавляю баг репорт в БД")
    try:
        user_id = get_user_id()
        bug_report_data = request.form.get('bugReport')
        log.debug(f"Получил на вход bug_report: '{bug_report_data}' и файлы: '{file_id}' от пользователя c id: {user_id}")

        bug_report_id = BugReport.create(user_id, bug_report_data, files_id=file_id)
        log.debug(f"Баг репорт {bug_report_id} успешно добавлен")

        # feedback_files_id = File.link(file_id, bug_report_id)
        # log.debug(f"Баг репорт {bug_report_id} и файл {file_id} слинкованы в id: {feedback_files_id}")

        return make_response({'message': 'The bug_report has been add successfully!'}, HTTPStatus.CREATED)
    except Exception as e:
        return make_response({'message': 'Something went wrong...'}, HTTPStatus.BAD_REQUEST)
     


def send_offer_handler(data: dict[str, Any]) -> Response:
    """
    Добавляет предложение от пользователя в БД
    """
    log.info(f"Добавляю предложение в БД")
    try:
        offer_data = data.get('offer')
        user_id = get_user_id()
        log.debug(f"Получил на вход offer: '{offer_data}' от пользователя c id: {user_id}")

        offer_id = Offer.create(user_id, offer_data)
        log.debug(f"Предложение {offer_id} успешно добавлено")

        return make_response({'message': 'The offer has been add successfully!'}, HTTPStatus.CREATED)
    except Exception as e:
        return make_response({'message': 'Something went wrong...'}, HTTPStatus.BAD_REQUEST)
     