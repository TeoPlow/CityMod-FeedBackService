from config import logger_config, UnauthorizedError
from server.database.tables import Mod, Map, ModElements, OtherContent, File
from server.handlers.get_user_id import get_user_id
from flask import url_for, make_response, Response
from http import HTTPStatus
from typing import Any

import logging
import logging.config


log = logging.getLogger('server')
logging.config.dictConfig(logger_config)


def add_content_handler(request, file_id: int, image_id: int) -> Response:
    """
    Добавляет контент от админа в БД
        Параметры:
            request: запрос в виде form
            file_id (int): ID файла
            image_id (int): ID изображения
        Возвращает:
            Response об успешном добавлении контента.
    """
    try:
        log.debug("Добавляю контент от админа в БД")
        user_id: int = get_user_id()
        
        content_type = request.form.get('content-type')
        if not content_type:
            log.error("Тип контента не указан.")
            return make_response({'error': 'Content type not specified'}, HTTPStatus.BAD_REQUEST)

        if content_type == "mod-content":
            name = request.form.get('mod-name')
            release_channel = request.form.get('release-channel')
            version = request.form.get('mod-version')
            game_versions = request.form.get('game-versions')
            changelog = request.form.get('mod-changelog')
            log.debug(f"Обрабатываю мод: {name}, {release_channel}, {version}, {game_versions}, {changelog}")
            
            content_id = Mod.create(name, release_channel, version, game_versions, changelog, file_id, image_id)

        elif content_type == "map-content":
            name = request.form.get('map-name')
            game_version = request.form.get('game-version')
            mod_version = request.form.get('map-mod-version')
            info = request.form.get('map-info')
            log.debug(f"Обрабатываю карту: {name}, {game_version}, {mod_version}, {info}")

            content_id = Map.create(name, game_version, mod_version, info, file_id, image_id)

        elif content_type == "mod-elements-content":
            name = request.form.get('name')
            element_type = request.form.get('type')
            status = request.form.get('status')
            mod_id = request.form.get('mod_id')
            path = request.form.get('path')
            info = request.form.get('info')
            version_added = request.form.get('version_added')
            log.debug(f"Обрабатываю элементы мода: {name}, {element_type}, {status}, {mod_id}, {path}, {info}, {version_added}")

            content_id = ModElements.create(name, element_type, status, mod_id, path, info, version_added, image_id, file_id)

        elif content_type == "other-content":
            name = request.form.get('content-name')
            info = request.form.get('content-info')
            log.debug(f"Обрабатываю прочий контент: {name}, {info}")

            content_id = OtherContent.create(name, info, file_id, image_id)

        else:
            log.error(f"Неизвестный тип контента: {content_type}")
            return make_response({'error': 'Unsupported content type'}, HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

        log.debug(f"{content_type} с id: {content_id} успешно добавлен")
        return make_response({'message': 'The content has been added successfully!'}, HTTPStatus.CREATED)

    except Exception as e:
        log.error(f"Ошибка обработки контента: {e}")
        return make_response({'error': f"{e}"}, HTTPStatus.BAD_REQUEST)