import os
import sys

root_dir = os.path.dirname(os.path.abspath(__file__))

DATABASE_URL = "postgresql+psycopg2://postgres@127.0.0.1:5432/citymod_feedback"


logger_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
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