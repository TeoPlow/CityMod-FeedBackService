from config import logger_config, FILEBASE_PATH, ALLOWED_EXTENSIONS, UnauthorizedError
from flask import make_response, Response
from http import HTTPStatus
from typing import Any, Optional
from server.database.tables import File
import os

import logging
import logging.config


log = logging.getLogger('server')
logging.config.dictConfig(logger_config)


def get_file_type(filename: str) -> Optional[str]:
    """
    Возвращает тип переданного файла, если он есть в ALLOWED_EXTENSIONS
        Параметры:
            filename (str): Название файла

        Возвращает:
            Optional[str]: Расширение файла, если есть.
    """
    file_type = '.' in filename and filename.rsplit('.', 1)[1].lower()
    if file_type in ALLOWED_EXTENSIONS:
        return file_type
    else:
        return None

def upload_file_handler(request, file_key: str, relative_path: str = '') -> int:
    """
    Загружает файл на сервер и в БД
        Параметры:
            request: Запрос
            file_key (str): Ключ, по которому передаётся файл внутри request.files
            relative_path (str): относительный путь между внутри папки /filebase/, в котором будет лежать добавленный файл.

        Возвращает:
            int: ID загруженного файла 
    """
    log.info("Загружаю файл на сервер и в БД")
    if file_key not in request.files:
        log.error(f"Файл не добавлен: Его нет в запросе - {file_key}")
        raise UnauthorizedError("The file was not added: It is not in the request")
    
    file = request.files[file_key]
    file_name = request.form.get('fileName')
    file_info = request.form.get('fileInfo')

    if file.filename == '' or not file_name:
        log.warning("Файл не добавлен: Имя файла пустое")
        raise UnauthorizedError("The file was not added: File name is empty")

    file_type = get_file_type(file.filename)

    if file and file_type != None:
        file_path = os.path.join(FILEBASE_PATH, relative_path, file.filename)
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)

        file_path_relative = os.path.join('filebase', relative_path, file.filename)
        log.debug(f"Файл сохранён на сервере по пути: {file_path_relative}")

        file_id = File.create(file_type, file_name, file_info, file_path_relative)
        return file_id
    else:
        log.error("Файл не добавлен: Расширение не поддерживается.")
        raise UnauthorizedError("The file was not added: The extension is not supported.")
