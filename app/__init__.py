from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from .model import TaiKhoan, KhoanThu, DotThu, KhoanThu_Has_DotThu, NopPhi
from .extension import db

def create_db(app):
    db_path = "instance/apartment.db"
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
            print("Database created successfully")

            admin_exists = db.session.query(TaiKhoan).filter_by(vaiTro='admin').first()
            if not admin_exists:
                    admin = TaiKhoan(
                        username='admin',
                        password='admin123',  # Nên mã hóa password trong thực tế
                        vaiTro='admin',
                        hoTen='Quản trị viên'
                    )
                    admin.set_password('admin123')  # Mã hóa mật khẩu trước khi lưu
                    db.session.add(admin)
                    db.session.commit()
                    print("Default admin account created")    
    else:
        print("Database already exists")


def create_app(config_file="config.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)

    create_db(app)

    # Import và đăng ký Blueprint
    from app.routes import auth_routes, user_routes, hokhau_routes, thuphi_routes
    app.register_blueprint(auth_routes.auth)
    # app.register_blueprint(user_routes.auth)
    # app.register_blueprint(hokhau_routes.auth)
    # app.register_blueprint(thuphi_routes.auth)

    return app
