from config import logger_config
from server.database.tables import Map, File
from flask import request
from typing import List
import os

import logging
import logging.config


log = logging.getLogger('server')
logging.config.dictConfig(logger_config)


def get_maps_handler() -> List[dict()]:
    """
    Получает карты из БД и редактирует список карт для корректного вывода.

        Возвращает:
            List[dict()]: Список словарей, где каждый словарь это Карта.
    """
    maps_list = Map.get_maps()

    for map in maps_list:
        map_time = map['time'].strftime('%d-%m-%Y %H:%M')
        map['time'] = map_time

        images_id = map['images_id']
        if images_id:
            image_path = File.get_path(map['images_id'])
        else:
            image_path = None

        files_id = map['files_id']
        if files_id:
            file_path = File.get_path(map['files_id'])
        else:
            file_path = None

        map['images_path'] = image_path
        map['files_path'] = file_path

    return maps_list



