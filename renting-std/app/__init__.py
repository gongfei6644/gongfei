# -*- coding: utf-8 -*-


from flask import Flask
from flask_apscheduler import APScheduler

from app import config


def create_app():
    app = Flask(__name__, template_folder="../templates")
    app.config.from_object(config)

    from app.webapi import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    return app
