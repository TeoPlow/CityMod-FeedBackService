import os
import sys
from colorama import Fore, Style
import logging

# Корневая папка
root_dir = os.path.dirname(os.path.abspath(__file__))


# URL базы данных
DATABASE_URL = "postgresql://postgres@127.0.0.1:5432/citymod_feedback"


# Путь к базе с файлами ОТНОСИТЕЛЬНО папки static
FILEBASE_PATH = "/home/teoblow/Programs/CityMod-FeedBackService/src/static/filebase"


# Поддерживаемые расширения
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'jar'}


# Класс ловитель ошибок
class UnauthorizedError(Exception):
    pass


# Логгер и его форматеры
class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.WHITE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, Style.RESET_ALL)
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        record.msg = f"{log_color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

logger_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "()": ColorFormatter,
            "format": "%(levelname)s | %(name)s | %(filename)s | %(asctime)s | %(lineno)s | %(message)s",
            "datefmt": "%H:%M:%S"
        }
    },
    "handlers": {
        "screen_handler": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
            "stream": sys.stdout
        },
    },
    "loggers": {
        'server': {
            'level': 'DEBUG',
            'handlers': ["screen_handler"],
            'propagate': False
        },
        'app': {
            'level': 'DEBUG',
            'handlers': ["screen_handler"],
            'propagate': False
        },
    }
}