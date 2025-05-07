from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import os
from .model import TaiKhoan, KhoanThu, DotThu, KhoanThu_Has_DotThu, NopPhi
from .extension import db
from flask_login import LoginManager
from datetime import timedelta


def create_db(app):
    db_path = "instance/apartment.db"
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
            print("Database created successfully")

            admin_exists = db.session.query(TaiKhoan).filter_by(vaiTro='admin').first()
            if not admin_exists:
                # Danh sách tài khoản mặc định cần tạo
                default_users = [
                    {
                        'username': 'admin',
                        'password': 'admin123',
                        'vaiTro': 'admin',
                        'hoTen': 'Quản trị viên'
                    },
                    {
                        'username': 'topho',
                        'password': 'topho123',
                        'vaiTro': 'Tổ phó',
                        'hoTen': 'Tổ phó mặc định'
                    },
                    {
                        'username': 'ketoan',
                        'password': 'ketoan123',
                        'vaiTro': 'Kế toán',
                        'hoTen': 'Kế toán mặc định'
                    }
                ]

                for user in default_users:
                    tai_khoan = TaiKhoan(
                        username=user['username'],
                        password=user['password'],
                        vaiTro=user['vaiTro'],
                        hoTen=user['hoTen']
                    )
                    tai_khoan.set_password(user['password'])
                    db.session.add(tai_khoan)
                    print(f"Default {user['vaiTro']} account created")
                
                db.session.commit() 
                print("Tao tai khoan thanh cong") 
    else:
        print("Database already exists")


def create_app(config_file="config.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)

    create_db(app)

     # Them current_user vào tất cả template
    @app.context_processor
    def inject_current_user():
        current_user = {
            'id': session.get('user_id'),
            'username': session.get('username'),
            'role': session.get('vaiTro'),
            'name': session.get('hoTen')
        }
        return dict(current_user=current_user)
    
    # Import và đăng ký Blueprint
    from app.routes import auth_routes, user_routes, hokhau_routes, thuphi_routes
    app.register_blueprint(auth_routes.auth)
    # app.register_blueprint(user_routes.auth)
    # app.register_blueprint(hokhau_routes.auth)
    # app.register_blueprint(thuphi_routes.auth)

    # Khoi tao login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"  # Chuyen den trang login neu chua dang nhap
    login_manager.init_app(app)  # Khoi tao login manager voi app
    app.permanent_session_lifetime = timedelta(hours=1)  # Thoi gian session ton tai
    
    @login_manager.user_loader
    def load_user(id):
        return TaiKhoan.query.get(int(id))  # Lay user tu db theo id

    return app
