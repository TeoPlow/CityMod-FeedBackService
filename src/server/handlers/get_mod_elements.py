from config import logger_config
from server.database.tables import ModElements, File
from flask import request
from typing import List
import os

import logging
import logging.config


log = logging.getLogger('server')
logging.config.dictConfig(logger_config)


def get_mod_elements_handler(name: str, element_type: str, status: str, version_added: str) -> List[dict()]:
    """
    Получает элементы мода из БД и редактирует список элементов для корректного вывода.

        Возвращает:
            List[dict()]: Список словарей, где каждый словарь это Элемент Мода.
    """
    mod_elements_list = ModElements.get_mod_elements(name, element_type, status, version_added)

    for mod_element in mod_elements_list:
        mod_element_time = mod_element['time'].strftime('%d-%m-%Y %H:%M')
        mod_element['time'] = mod_element_time

        images_id = mod_element['images_id']
        if images_id:
            image_path = File.get_path(mod_element['images_id'])
        else:
            image_path = None

        files_id = mod_element['files_id']
        if files_id:
            file_path = File.get_path(mod_element['files_id'])
        else:
            file_path = None

        mod_element['images_path'] = image_path
        mod_element['files_path'] = file_path

    return mod_elements_list



