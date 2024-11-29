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
    def create(name: str, email: str, password: str) -> List[dict]:
        """
        Создаёт нового пользователя в БД.
            Параметры:
                name: Имя пользователя
                email: Email пользователя, 
                       обязательно в формате example@mail.ru
                password: Пароль пользователя

            Возвращает:
                ID созданного пользователя
        """
        log.debug("Создаю нового пользователя")
        password_hash = generate_password_hash(password)
        query = """
        INSERT INTO users (name, email, password_hash)
        VALUES (%s, %s, %s) RETURNING id;
        """
        return execute_query(query, (name, email, password_hash), fetch=True)[0]['id']

    @staticmethod
    def check_password(user_id: str, password: str) -> bool:
        """
        Проверяет, верен ли пароль пользователя, сравнивая хэши.
            Параметры:
                user_id: ID пользователя
                password: Пароль пользователя

            Возвращает:
                Правильный ли пароль?
        """
        log.debug("Проверяю пароль пользователя")
        query = "SELECT password_hash FROM users WHERE id = %s;"
        result = execute_query(query, (user_id,), fetch=True)
        if not result:
            return False
        return check_password_hash(result[0]['password_hash'], password)

    @staticmethod
    def check_user_existence(email_or_name):
        """
        Проверяет, существует ли пользователь с такой почтой или именем в БД.
            Параметры:
                email_or_name: Почта или имя

            Возвращает:
                Существует ли пользователь в БД?
        """
        log.debug("Проверяю существование пользователя по почте или имени")
        query = "SELECT id FROM users WHERE email = %s OR name = %s;"
        result = execute_query(query, (email_or_name, email_or_name), fetch=True)
        if result:
            return result
        else:
            return False



class Review:
    @staticmethod
    def create(user_id: int, message: str) -> int:
        log.debug("Добавляю отзыв")
        query = """
        INSERT INTO reviews (user_id, message)
        VALUES (%s, %s) RETURNING id;
        """
        return execute_query(query, (user_id, message), fetch=True)[0]['id']


class BugReport:
    @staticmethod
    def create(user_id: int, message: str, files_id: int = None) -> int:
        log.debug("Добавляю баг репорт")
        query = """
        INSERT INTO bug_reports (user_id, message, files_id)
        VALUES (%s, %s, %s) RETURNING id;
        """
        return execute_query(query, (user_id, message, files_id), fetch=True)[0]['id']


class Offer:
    @staticmethod
    def create(user_id, message, files_id=None) -> int:
        log.debug("Добавляю предложение")
        query = """
        INSERT INTO offers (user_id, message, files_id)
        VALUES (%s, %s, %s) RETURNING id;
        """
        return execute_query(query, (user_id, message), fetch=True)[0]['id']


class File:
    @staticmethod
    def create(file_type, file_name, file_info, file_path):
        log.debug("Добавляю файл")
        query = """
        INSERT INTO files (type, file_name, file_info, file_path)
        VALUES (%s, %s, %s, %s) RETURNING id;
        """
        return execute_query(query, (file_type, file_name, file_info, file_path), fetch=True)[0]['id']

    @staticmethod
    def link(file_id, feedback_id):
        log.debug("Линкую файл с одним из фидбэков")
        query = """
        INSERT INTO feedback_files (feedback_id, file_id)
        VALUES (%s, %s) RETURNING id;
        """
        return execute_query(query, (feedback_id, file_id), fetch=True)[0]['id']

class Mod:
    @staticmethod
    def create(name, release_channel, version, game_versions, changelog, files_id):
        log.debug("Добавляю мод")
        query = """
        INSERT INTO mods (name, release_channel, version, game_versions, changelog, files_id)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
        """
        return execute_query(query, (name, release_channel, version, game_versions, changelog, files_id), fetch=True)[0]['id']

    @staticmethod
    def get_mods():
        log.debug("Получаю все моды из БД")
        query = """
        SELECT * FROM mods;
        """
        return execute_query(query, fetch=True)


class Map:
    @staticmethod
    def create(name, info, files_id):
        log.debug("Добавляю карту")
        query = """
        INSERT INTO maps (name, info, files_id)
        VALUES (%s, %s, %s) RETURNING id;
        """
        return execute_query(query, (name, info, files_id), fetch=True)[0]['id']


class OtherContent:
    @staticmethod
    def create(name, info, files_id):
        log.debug("Добавляю другой контент")
        query = """
        INSERT INTO maps (name, info, files_id)
        VALUES (%s, %s, %s) RETURNING id;
        """
        return execute_query(query, (name, info, files_id), fetch=True)[0]['id']