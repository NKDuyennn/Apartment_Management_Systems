from flask import Blueprint, request, jsonify, render_template
from app.services.user_service import UserService
from app.model import TaiKhoan

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth.route('/login', methods=['GET','POST'])
def login():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
        
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Thiếu tên đăng nhập hoặc mật khẩu'}), 400
    
    user = UserService.authenticate_user(username, password)
    
    if user:
        return jsonify({
            'message': f'Đăng nhập thành công ({user.username})',
            'username': user.username,
            'vaiTro': user.vaiTro,
            'hoTen': user.hoTen
        }), 200
    else:
        return jsonify({'error': 'Tài khoản hoặc mật khẩu không đúng'}), 401
    
