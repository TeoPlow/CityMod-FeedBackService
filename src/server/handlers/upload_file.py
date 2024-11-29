from config import logger_config, FILEBASE_PATH, ALLOWED_EXTENSIONS
from flask import make_response, Response
from http import HTTPStatus
from typing import Any
from server.database.tables import File
import os

import logging
import logging.config


log = logging.getLogger('server')
logging.config.dictConfig(logger_config)


def get_file_type(filename):
    file_type = '.' in filename and filename.rsplit('.', 1)[1].lower()
    if file_type in ALLOWED_EXTENSIONS:
        return file_type
    else:
        return None

def upload_file_handler(request) -> Response:
    """
    Загружает файл на сервер и в БД
    """
    log.info("Загружаю файл на сервер и в БД")
    if 'file' not in request.files:
        log.error("Файл не добавлен: Его нет в запросе")
        raise
    
    file = request.files['file']
    file_name = request.form.get('fileName')
    file_info = request.form.get('fileInfo')

    if file.filename == '':
        log.error("Файл не добавлен: file.filename == '' ")
        raise

    file_type = get_file_type(file.filename)
    if file and file_type != None:
        file_path = os.path.join(FILEBASE_PATH, file.filename)
        file.save(file_path)
        log.debug(f"Файл сохранён на сервере по пути: {file_path}")

        file_id = File.create(file_type, file_name, file_info, file_path)
        return file_id
    else:
        log.error("Файл не добавлен: Расширение не поддерживается.")
        raise
