from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from app.services.user_service import UserService
from app.model import TaiKhoan



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Thiếu tên đăng nhập hoặc mật khẩu'}), 400
    
    user = UserService.authenticate_user(username, password)
    
    if user:
        session.permanent = True  # Thoi gian session ton tai
        login_user(user, remember=True)

        return redirect(url_for('auth.home'))
    else:
        return jsonify({'error': 'Tài khoản hoặc mật khẩu không đúng'}), 401

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/home', methods=['GET'])
@login_required
def home():
    return render_template('home.html', current_user=current_user) 