from flask import Flask

from app.config import ProdConfig


def create_app(config=ProdConfig):
    """Application factory"""
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    return app


def register_extensions(app: Flask):
    pass


def register_blueprints(app: Flask):
    pass


def register_errorhandlers(app: Flask):
    pass


def register_shellcontext(app: Flask):
    context = {}

    app.shell_context_processor(lambda: context)


def register_commands(app: Flask):
    pass
