from config import logger_config
from werkzeug.security import generate_password_hash, check_password_hash
from server.database.db_connection import execute_query
from typing import List, Optional

import logging
import logging.config

log = logging.getLogger('server')
logging.config.dictConfig(logger_config)

class User:
    @staticmethod
    def create(name: str, email: str, password: str) -> int:
        """
        Создаёт нового пользователя в БД.
            Параметры:
                name: Имя пользователя
                email: Email пользователя, 
                       обязательно в формате example@mail.ru
                password: Пароль пользователя

            Возвращает:
                int: ID созданного пользователя
        """
        log.debug("Создаю нового пользователя")
        password_hash = generate_password_hash(password)
        query = """
        INSERT INTO users (name, email, password_hash)
        VALUES (%s, %s, %s) RETURNING id;
        """
        return execute_query(query, (name, email, password_hash), fetch=True)[0]['id']

    @staticmethod
    def check_password(user_id: int, password: str) -> bool:
        """
        Проверяет, верен ли пароль пользователя, сравнивая хэши.
            Параметры:
                user_id: ID пользователя
                password: Пароль пользователя

            Возвращает:
                bool: Правильный ли пароль?
        """
        log.debug(f"Проверяю пароль пользователя c id: {user_id}")
        query = "SELECT password_hash FROM users WHERE id = %s;"
        result = execute_query(query, (user_id,), fetch=True)
        if not result:
            log.warning("Пароля у этого пользователя НЕТ")
            return False
        else:
            return check_password_hash(result[0]['password_hash'], password)

    @staticmethod
    def check_user_existence(email_or_name: str) -> int | bool:
        """
        Проверяет, существует ли пользователь с такой почтой или именем в БД.
            Параметры:
                email_or_name: Почта или имя

            Возвращает:
                Существует ли пользователь в БД? 
                Если да, то возвращает user_id: int
                Иначе False
        """
        log.debug("Проверяю существование пользователя по почте или имени")
        query = "SELECT id FROM users WHERE email = %s OR name = %s;"
        result = execute_query(query, (email_or_name, email_or_name), fetch=True)
        if result:
            log.debug("Пользователь существует.")
            return result[0]['id']
        else:
            log.debug("Пользователя НЕ существует")
            return False

    @staticmethod
    def get_name(file_id: int) -> str:
        """
        Возвращает имя пользователя через его ID.
            Параметры:
                file_id (int): ID файла

            Возвращает:
                str: Имя пользователя.
        """
        log.debug("Получаю имя пользователя")
        query = """
        SELECT name FROM users WHERE id = %s;
        """
        return execute_query(query, (file_id,), fetch=True)[0]['name']


class Feedback:
    @staticmethod
    def create(user_id: int, feedback_type: str, message: str, files_id: int) -> int:
        """
        Добавляет новый фидбэк в БД.
            Параметры:
                user_id (int): ID пользователя, оставляющего фидбэк
                feedback_type (str): Тип фидбэка (например, review, bug_report)
                message (str): Сообщение фидбэка
                files_id (int): ID прикрепленного файла

            Возвращает:
                int: ID созданного фидбэка
        """
        log.debug("Добавляю feedback")
        query = """
        INSERT INTO feedback (user_id, type, message, files_id)
        VALUES (%s, %s, %s, %s) RETURNING id;
        """
        return execute_query(query, (user_id, feedback_type, message, files_id), fetch=True)[0]['id']

    @staticmethod
    def get_feedback(feedback_type: str = '') -> List[dict()]:
        """
        Получает список всех фидбэков из БД.
            Параметры:
                feedback_type (str): Тип фидбэка для фильтрации.

            Возвращает:
                list: Список фидбэков.
        """
        log.debug("Получаю все фидбэки из БД")
        if feedback_type != '':
            where_type = f"WHERE type = '{feedback_type}'"
        else:
            where_type = ''

        query = "SELECT * FROM feedback " + where_type + " ORDER BY time desc;"
        return execute_query(query, fetch=True)


class File:
    @staticmethod
    def create(file_type: str, file_name: str, file_info: str, file_path: str) -> int:
        """
        Добавляет файл в БД.
            Параметры:
                file_type (str): Тип файла (например, изображение, текстовый документ)
                file_name (str): Название файла
                file_info (str): Описание файла
                file_path (str): Путь к файлу

            Возвращает:
                int: ID созданного файла
        """
        log.debug("Добавляю файл")
        query = """
        INSERT INTO files (type, file_name, file_info, file_path)
        VALUES (%s, %s, %s, %s) RETURNING id;
        """
        return execute_query(query, (file_type, file_name, file_info, file_path), fetch=True)[0]['id']

    @staticmethod
    def link(file_id: int, feedback_id: int) -> int:
        """
        Линкует файл с фидбэком в БД.
            Параметры:
                file_id (int): ID файла
                feedback_id (int): ID фидбэка

            Возвращает:
                int: ID созданной записи линковки
        """
        log.debug("Линкую файл с одним из фидбэков")
        query = """
        INSERT INTO feedback_files (feedback_id, file_id)
        VALUES (%s, %s) RETURNING id;
        """
        return execute_query(query, (feedback_id, file_id), fetch=True)[0]['id']

    @staticmethod
    def get_path(file_id: int) -> str:
        """
        Возвращает путь к файлу через его ID.
            Параметры:
                file_id (int): ID файла

            Возвращает:
                str: Путь до файла.
        """
        log.debug("Получаю путь до файла")
        query = """
        SELECT file_path FROM files WHERE id = %s;
        """
        return execute_query(query, (file_id,), fetch=True)[0]['file_path']

class Mod:
    @staticmethod
    def create(name: str, release_channel: str, version: str, game_versions: str, changelog: str, files_id: int, images_id: int) -> int:
        """
        Добавляет новый мод в БД.
            Параметры:
                name (str): Название мода
                release_channel (str): Канал релиза (например, beta, release)
                version (str): Версия мода
                game_versions (str): Поддерживаемые версии игры
                changelog (str): Описание изменений
                files_id (int): ID связанного файла
                images_id (int): ID связанного изображения

            Возвращает:
                int: ID созданного мода
        """
        log.debug("Добавляю мод")
        query = """
        INSERT INTO mods (name, release_channel, version, game_versions, changelog, files_id, images_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """
        return execute_query(query, (name, release_channel, version, game_versions, changelog, files_id, images_id), fetch=True)[0]['id']

    @staticmethod
    def get_mods(mod_type: str = '') -> List[dict()]:
        """
        Получает список всех модов из БД.   
            Параметры:
                mod_type (str): Тип (версия) мода для фильтрации.    

            Возвращает:
                list: Список модов.
        """
        log.debug("Получаю все моды из БД")
        if mod_type != '':
            where_type = f"WHERE game_versions = '{mod_type}'"
        else:
            where_type = ''

        query = "SELECT * FROM mods " + where_type + " ORDER BY version desc;"
        return execute_query(query, fetch=True)


class Map:
    @staticmethod
    def create(name: str, game_versions: str, mod_version: str, info: str, files_id: int, images_id: int) -> int:
        """
        Добавляет новую карту в БД.
            Параметры:
                name (str): Название карты
                info (str): Описание карты
                game_versions (str): Версии игры
                mod_version (str): Версия мода
                files_id (int): ID связанного файла
                images_id (int): ID связанного изображения

            Возвращает:
                int: ID созданной карты
        """
        log.debug("Добавляю карту")
        query = """
        INSERT INTO maps (name, game_versions, mod_version, info, files_id, images_id)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
        """
        return execute_query(query, (name, game_versions, mod_version, info, files_id, images_id), fetch=True)[0]['id']

    @staticmethod
    def get_maps() -> List[dict()]:
        """
        Получает список всех карт из БД.        
            Возвращает:
                list: Список карт.
        """
        log.debug("Получаю все карты из БД")
        query = """
        SELECT * FROM maps ORDER BY id desc;
        """
        return execute_query(query, fetch=True)


class ModElements:
    @staticmethod
    def create(name: str, element_type: str, status: str, mod_id: str, path: str, info: str, version_added: str, images_id: int, files_id: int) -> int:
        """
        Добавляет элемент мода в БД.
            Параметры:
                name (str): Название элемента
                element_type (str): Тип элемента
                status (str): Статус разработки
                mod_id (str): ID мода
                path (str): Путь до файла
                info (str): Описание карты
                version_added (str): Версия игры, в которой добавили элемент
                files_id (int): ID связанного файла
                images_id (int): ID связанного изображения
            Возвращает:
                int: ID созданного элемента
        """
        log.debug("Добавляю элемент мода")
        query = """
        INSERT INTO mod_elements (name, type, status, mod_id, path, info, version_added, images_id, files_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """
        return execute_query(query, (name, element_type, status, mod_id, path, info, version_added, images_id, files_id), fetch=True)[0]['id']

    @staticmethod
    def get_mod_elements(name: str, element_type: str, status: str, version_added: str) -> List[dict]:
        """
        Получает список всех элементов мода из БД, с учётом входных переменных для поиска.
            Параметры:
                name (str): Название элемента
                element_type (str): Тип элемента
                status (str): Статус разработки
                version_added (str): Версия игры, в которой добавили элемент
            Возвращает:
                list: Список элементов мода.
        """
        log.debug("Получаю все элементы мода из БД")
        
        base_query = """
        SELECT * FROM mod_elements
        """

        filters = []
        params = []
        
        if name:
            filters.append("name = %s")
            params.append(name)
        if element_type:
            filters.append("element_type = %s")
            params.append(element_type)
        if status:
            filters.append("status = %s")
            params.append(status)
        if version_added:
            filters.append("version_added = %s")
            params.append(version_added)
        
        if filters:
            base_query += " WHERE " + " AND ".join(filters)
        
        base_query += " ORDER BY id desc;"
        
        log.debug(f"Создан запрос с учётом фильтров: {base_query}, параметры: {params}")
        return execute_query(base_query, tuple(params), fetch=True)


class OtherContent:
    @staticmethod
    def create(name: str, info: str, files_id: int, images_id: int) -> int:
        """
        Добавляет другой тип контента в БД.
            Параметры:
                name (str): Название контента
                info (str): Описание контента
                files_id (int): ID связанного файла
                images_id (int): ID связанного изображения

            Возвращает:
                int: ID созданного контента
        """
        log.debug("Добавляю другой контент")
        query = """
        INSERT INTO other_content (name, info, files_id, images_id)
        VALUES (%s, %s, %s, %s) RETURNING id;
        """
        return execute_query(query, (name, info, files_id, images_id), fetch=True)[0]['id']

    @staticmethod
    def get_other_contents() -> List[dict()]:
        """
        Получает список всякого другого контента из БД.        
            Возвращает:
                list: Список другого контента.
        """
        log.debug("Получаю весь другой контент из БД")
        query = """
        SELECT * FROM other_content ORDER BY id desc;
        """
        return execute_query(query, fetch=True)