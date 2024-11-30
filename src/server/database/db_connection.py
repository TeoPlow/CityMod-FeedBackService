from config import DATABASE_URL, logger_config
from psycopg2.extras import RealDictCursor
import psycopg2
from typing import List, Union, Optional, Tuple

import logging
import logging.config


log = logging.getLogger('server')
logging.config.dictConfig(logger_config)


def execute_query(query: str, params: Optional[Tuple[str, ...]] = None, fetch: bool = False) -> List[dict]:
    """
    Выполняет SQL-запрос и возвращает результат как список словарей.
        Параметры:
            query: SQL код для запроса к БД
            params: Параметры для использования в запросе
            fetch: Получить ли ответ от базы данных?

        Возвращает:
            Ответ от базы данных
    """
    log.info("Работаю с БД")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        log.debug("Подключился к БД")
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        log.debug("Создал курсор")

        cursor.execute(query, params)

        if fetch:
            result = cursor.fetchall()
            log.debug(f"Получил ответ от БД: {result}")
        else:
            result = None
            log.debug("Ответа от БД нет: fetch = false")

        conn.commit()
        return result

    except psycopg2.Error as e:
        log.error(f"Ошибка в БД: {e}")
        conn.rollback()
    finally:
        if cursor:
            log.debug("Выключаю курсор")
            cursor.close()
        if conn:
            log.debug("Отключаю соединение")
            conn.close()

