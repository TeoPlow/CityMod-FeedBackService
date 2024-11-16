import os
import logging
import logging.config
from flask import Flask, render_template
from server import main
from config import root_dir, logger_config

logger = logging.getLogger('app')
logging.config.dictConfig(logger_config)


template_folder = os.path.join(root_dir, "templates")
app = Flask(__name__, template_folder=template_folder)

@app.route("/")
def index():
    logger.info(f"Перехожу по app.route('/')")
    return render_template("index.html")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.config["WTF_CSRF_ENABLED"] = False
    app.run()