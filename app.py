from flask import Flask, render_template
from flask_restx import Api

from project.config import config
from project.setup.db import db
from project.views.main import directors_ns

api = Api(title="Flask Course Project 3", doc="/docs")


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    @app.route('/')
    def index():
        return render_template('index.html')

    db.init_app(app)
    api.init_app(app)

    api.add_namespace(directors_ns)

    return app