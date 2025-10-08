from flask import Flask, jsonify
from dotenv import load_dotenv
from extensions import db, migrate, jwt
import os
from datetime import timedelta
from Blueprints.auth.models import User, TokenBlockList


def create_app():
    app = Flask(__name__)

   

    # 1. Load variables from .env into system environment
    load_dotenv()

     # load all .env variables with prefix FLASK
    app.config.from_prefixed_env()

    # Set JWT config
    app.config["JWT_SECRET_KEY"] = os.getenv("FLASK_JWT_SECRET_KEY")  # load JWT secret key
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]  # where JWT is expected (headers, cookies, etc.) where the token will be sent
    app.config["JWT_HEADER_NAME"] = "Authorization" # default
    app.config["JWT_HEADER_TYPE"] = "Bearer"        # default

    # set access token and refresh token expiration 
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)
    


   
    # print(app.config['SECRET_KEY'])
    # print(app.config['DEBUG'])
    # print(app.config['SQLALCHEMY_DATABASE_URI'])
    # print(app.config['PORT'])

     # init extensions
    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)

   

    # register bluperints
    from Blueprints.auth.views import auth_bp
    from Blueprints.dashboard.views import dashboard_bp
    from Blueprints.screens.routes import screens_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(screens_bp, url_prefix='/home')

    # looking up current user
    @jwt.user_lookup_loader
    def user_lookup_callback(jwt_headers,jwt_data):

        identity = jwt_data['sub']

        return User.query.filter_by(username = identity).one_or_none()

    # adding additional claims to created jwt
    @jwt.additional_claims_loader
    def make_additional_claims(identity):

        if identity == 'jean':
            return {"is_admin": True}
        return {"is_staff":True}

    # Handling token expired,token invalid,token missing senarios

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header,jwt_data):
        return jsonify({"message": "Token  has expired","error": "token_expired"}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Signature verification failed","error": str(error)}), 401


    # handle missing 
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message": "Missing Authorization Header","error": str(error)}), 401
    
    # logout user 
    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header,jwt_data):
         
         jti = jwt_data['jti']

         token = db.session.query(TokenBlockList).filter(TokenBlockList.jti == jti).scalar()

         return token is not None
        


    return app