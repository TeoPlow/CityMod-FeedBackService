import os
import logging
import logging.config
import server.database.db_create as db
from server.database.db_connection import session
from server.core.registration import user_register
from server.core.login import user_login
from server.handlers.mods import fetch_all_mods

from flask import Flask, render_template, render_template_string, request, jsonify
from server import main
from config import root_dir, logger_config


logger = logging.getLogger('app')
logging.config.dictConfig(logger_config)


template_folder = os.path.join(root_dir, "templates")
app = Flask(__name__, template_folder=template_folder)


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/send_review', methods=['GET', 'POST'])
def send_review():
    if request.method == 'POST':
        return("Отправка отзыва")

    elif request.method == 'GET':
        return render_template("send_review.html")


@app.route('/send_bug_report', methods=['GET', 'POST'])
def send_bug_report():
    if request.method == 'POST':
        return("Отправка баг репорта")

    elif request.method == 'GET':
        return render_template("send_bug_report.html")


@app.route('/send_offer', methods=['GET', 'POST'])
def send_offer():
    if request.method == 'POST':
        return("Отправка предложения")

    elif request.method == 'GET':
        return render_template("send_offer.html")


@app.route('/mods', methods=['GET'])
def mods():
    return render_template('mods.html', mods=fetch_all_mods())


@app.route('/maps', methods=['GET'])
def maps():
    return render_template("maps.html")


@app.route('/other_content', methods=['GET'])
def other_content():
    return render_template("other_content.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        message, request_code = user_register(data)
        return jsonify(message), request_code

    elif request.method == 'GET':
        return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        message, request_code = user_login(data)
        return jsonify(message), request_code

    elif request.method == 'GET':
        return render_template("login.html")
    


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.config["WTF_CSRF_ENABLED"] = False
    app.run()