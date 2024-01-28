# app.py
from flask import Flask
from database import Database
import routes


def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes.bp)
    return app

app = create_app()
