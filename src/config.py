import os
import sys

root_dir = os.path.dirname(os.path.abspath(__file__))

DATABASE_URL = "postgresql://postgres@127.0.0.1:5432/citymod_feedback"

FILEBASE_PATH = "/home/teoblow/Programs/CityMod-FeedBackService/filebase"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

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