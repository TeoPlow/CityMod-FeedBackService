from config import logger_config
from server.database.tables import Mod, File
from flask import request
from typing import List
import os

import logging
import logging.config


log = logging.getLogger('server')
logging.config.dictConfig(logger_config)


def get_mods_handler() -> List[dict()]:
    """
    Получает моды из БД и редактирует список модов для корректного вывода.

        Возвращает:
            List[dict()]: Список словарей, где каждый словарь это Мод.
    """
    mods_list = Mod.get_mods()

    for mod in mods_list:
        mod_time = mod['time'].strftime('%d-%m-%Y %H:%M')
        mod['time'] = mod_time

        images_id = mod['images_id']
        if images_id:
            image_path = File.get_path(mod['images_id'])
        else:
            image_path = None

        files_id = mod['files_id']
        if files_id:
            file_path = File.get_path(mod['files_id'])
        else:
            file_path = None

        mod['images_path'] = image_path
        mod['files_path'] = file_path

    return mods_list



