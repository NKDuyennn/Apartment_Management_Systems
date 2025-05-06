from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    CORS(app)

    # Import và đăng ký Blueprint
    from app.routes import auth_routes, user_routes, hokhau_routes, thuphi_routes
    app.register_blueprint(auth_routes.auth)
    # app.register_blueprint(user_routes.auth)
    # app.register_blueprint(hokhau_routes.auth)
    # app.register_blueprint(thuphi_routes.auth)

    return app
