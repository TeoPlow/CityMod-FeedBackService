from config import logger_config
from server.database.db_connection import get_db
from server.database.db_create import BugReport
from server.handlers.get_user_id import get_user_id
from flask import url_for, make_response

import logging
import logging.config


logger = logging.getLogger('server')
logging.config.dictConfig(logger_config)

def send_review_handler(data):
    db = next(get_db())

    review_data = data.get('review')
    user_id = get_user_id()
    logger.info(f"Получил на вход review: {review_data} от пользователя c id: {user_id}")

    review = Review(user_id=user_id, review=review_data)
    db.add(review)
    db.commit()
    db.refresh(review)
    logger.info("Отзыв успешно добавлен")

    response = make_response({'message': 'The review has been add successfully!'}, 201)
    return response


def send_bug_report_handler(data):
    db = next(get_db())

    bug_report_data = data.get('bug_report')
    user_id = get_user_id()
    logger.info(f"Получил на вход bug_report: {bug_report_data} от пользователя c id: {user_id}")

    files_id = data.get('files_id')

    bug_report = BugReport(user_id=user_id, message=bug_report_data, files_id=files_id)
    db.add(bug_report)
    db.commit()
    db.refresh(bug_report)
    logger.info("Баг репорт успешно добавлен")

    response = make_response({'message': 'The bug report has been add successfully!'}, 201)
    return response


def send_offer_handler(data):
    pass