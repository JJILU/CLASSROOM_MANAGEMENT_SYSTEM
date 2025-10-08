from flask import Flask
from extensions import db,migrate,JWTManager


def create_app():

    app = Flask(__name__)

    # app configurations


    # init extensions

    # import & register blueprints
    from Blueprints.core.views import core_bp 
    from Blueprints.auth.views import auth_bp 
    from Blueprints.dashboard.views import dashboard_bp 

    app.register_blueprint(core_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/dasboard")


    return app

