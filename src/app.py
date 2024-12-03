import os
from server.database.tables import Mod
from server.core.registration import user_register
from server.core.login import user_login, login_required, admin_required
from server.handlers.sends import send_feedback_handler
from server.handlers.get_feedback import get_feedback_handler
from server.handlers.upload_file import upload_file_handler
from server.handlers.get_mods import get_mods_handler
from server.handlers.get_maps import get_maps_handler
from server.handlers.get_other_content import get_other_content_handler
from server.handlers.get_mod_elements import get_mod_elements_handler
from server.handlers.add_content import add_content_handler

from flask import Flask, render_template, request, make_response
from config import root_dir, logger_config

import logging
import logging.config
from http import HTTPStatus
from datetime import datetime


log = logging.getLogger('app')
logging.config.dictConfig(logger_config)

template_folder = os.path.join(root_dir, "templates")
app = Flask(__name__, template_folder=template_folder)


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/send_review', methods=['GET'])
@login_required
def send_review():
    return render_template("send_review.html")


@app.route('/send_bug_report', methods=['GET'])
@login_required
def send_bug_report():
    return render_template("send_bug_report.html")


@app.route('/send_offer', methods=['GET'])
@login_required
def send_offer():
    return render_template("send_offer.html")


@app.route('/send_feedback', methods=['POST'])
def send_feedback():
    try:
        uploaded_file = request.files.get("file")
        log.debug(f"Получил uploaded_file = {uploaded_file}")
        if uploaded_file:
            log.info("Отправляю запрос на добавление файла")
            file_id = upload_file_handler(request, 'file')
        else: 
            file_id = None
        
        response = send_feedback_handler(request, file_id)
        log.info("Отправляю фидбэк на сервер")
        return response 
    except Exception as e:
        log.error(f"Ошибка: {e}")
        return make_response({'message': f"{e}"}, HTTPStatus.BAD_REQUEST)


@app.route('/mods', methods=['GET'])
def mods():
    log.info("Вывожу список модов")
    mod_type = request.args.get('mod_type', '')
    mods_list = get_mods_handler(mod_type=mod_type)

    return render_template('mods.html', mods=mods_list)


@app.route('/maps', methods=['GET'])
def maps():
    log.info("Вывожу список модов")
    maps_list = get_maps_handler()

    return render_template("maps.html", maps=maps_list)


@app.route('/mod_elements', methods=['GET'])
def mod_elements():
    log.info("Вывожу список другого контента")
    name = ''
    element_type = ''
    status = ''
    version_added = ''
    mod_elements_list = get_mod_elements_handler(name, element_type, status, version_added)
    return render_template("mod_elements.html", mod_elements=mod_elements_list)


@app.route('/other_content', methods=['GET'])
def other_content():
    log.info("Вывожу список другого контента")
    other_content_list = get_other_content_handler()

    return render_template("other_content.html", other_contents=other_content_list)


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            log.info("Отправляю запрос на регистрацию")
            data = request.json
            return user_register(data)

        elif request.method == 'GET':
            return render_template("register.html")
    except Exception as e:
        log.error(f"Ошибка: {e}")
        return make_response({'error': f"{e}"}, HTTPStatus.BAD_REQUEST)


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            log.info("Отправляю запрос на логирование")
            data = request.json
            return user_login(data)

        elif request.method == 'GET':
            return render_template("login.html")
    except Exception as e:
        log.error(f"Ошибка: {e}")
        return make_response({'error': f"{e}"}, HTTPStatus.BAD_REQUEST)
    

@app.route('/admin', methods=['GET'])
@admin_required
def admin():
    return render_template("admin/admin.html")


@app.route('/check_feedback', methods=['GET'])
@admin_required
def check_feedback():
    log.info("Вывожу список фидбэка")
    feedback_type = request.args.get('feedback_type', '')
    feedback_list = get_feedback_handler(feedback_type=feedback_type)

    return render_template("admin/check_feedback.html", feedbacks=feedback_list)


@app.route('/admin/add_content', methods=['POST'])
@admin_required
def add_content():
    try:
        uploaded_file = request.files.get("file")
        log.debug(f"Получил uploaded_file = {uploaded_file}")
        log.info("Отправляю запрос на добавление файла")
        file_id = upload_file_handler(request, 'file', relative_path='downloaded')

        uploaded_image = request.files.get("image")
        log.debug(f"Получил uploaded_image = {uploaded_image}")
        log.info("Отправляю запрос на добавление изображения")
        image_id = upload_file_handler(request, 'image', relative_path='images')
        
        response = add_content_handler(request, file_id, image_id)
        log.info("Отправляю контент на сервер")
        return response
    except Exception as e:
        log.error(f"Ошибка: {e}")
        return make_response({'error': f"{e}"}, HTTPStatus.BAD_REQUEST)


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(host='0.0.0.0', port='5000', debug=True)