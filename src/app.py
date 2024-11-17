import os
import logging
import logging.config
import server.database.db_create as db
from server.database.db_connection import session


from flask import Flask, render_template, render_template_string, request, jsonify
from server import main
from config import root_dir, logger_config


logger = logging.getLogger('app')
logging.config.dictConfig(logger_config)


template_folder = os.path.join(root_dir, "templates")
app = Flask(__name__, template_folder=template_folder)


@app.route("/")
def index():
    logger.info(f"Перехожу на главную страницу")
    return render_template("main_page/index.html")


@app.route('/send_review', methods=['GET', 'POST'])
def send_review():
    if request.method == 'POST':
        return("Отправка отзыва")

    elif request.method == 'GET':
        return("Менюшка с добавлением отзыва")


@app.route('/send_bug_report', methods=['GET', 'POST'])
def send_bug_report():
    if request.method == 'POST':
        return("Отправка баг репорта")

    elif request.method == 'GET':
        return("Менюшка с добавлением баг репорта")


@app.route('/send_offer', methods=['GET', 'POST'])
def send_offer():
    if request.method == 'POST':
        return("Отправка предложения")

    elif request.method == 'GET':
        return("Менюшка с добавлением предложения")


@app.route('/mods', methods=['GET'])
def mods():
    return("Список модификаций")


@app.route('/maps', methods=['GET'])
def maps():
    return("Список карт")


@app.route('/other_content', methods=['GET'])
def other_content():
    return("Список другого контента")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.config["WTF_CSRF_ENABLED"] = False
    app.run()