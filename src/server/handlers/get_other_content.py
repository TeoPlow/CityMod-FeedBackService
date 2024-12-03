from config import logger_config
from server.database.tables import OtherContent, File
from flask import request
from typing import List
import os

import logging
import logging.config


log = logging.getLogger('server')
logging.config.dictConfig(logger_config)


def get_other_content_handler() -> List[dict()]:
    """
    Получает другой контент из БД и редактирует список другого контента для корректного вывода.

        Возвращает:
            List[dict()]: Список словарей, где каждый словарь это Другой контент.
    """
    other_contents_list = OtherContent.get_other_contents()

    for other_content in other_contents_list:
        other_content_time = other_content['time'].strftime('%d-%m-%Y %H:%M')
        other_content['time'] = other_content_time

        images_id = other_content['images_id']
        if images_id:
            image_path = File.get_path(other_content['images_id'])
        else:
            image_path = None

        files_id = other_content['files_id']
        if files_id:
            file_path = File.get_path(other_content['files_id'])
        else:
            file_path = None

        other_content['images_path'] = image_path
        other_content['files_path'] = file_path

    return other_contents_list



