from flask import Blueprint, request, jsonify, render_template
from app.services.user_service import UserService  # Giả sử bạn đã có UserService để tương tác với DB

auth = Blueprint('auth', __name__, url_prefix='/auth')

# Tài khoản admin mặc định
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

# Đảm bảo có một route GET để trả về trang login.html
@auth.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# Route xử lý POST request cho việc login
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Thiếu tên đăng nhập hoặc mật khẩu'}), 400

    # Kiểm tra tài khoản admin mặc định
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return jsonify({
            'message': f'Đăng nhập thành công ({username})',
            'username': username,
            'role': 'admin'  # Giả sử quyền admin
        }), 200
    
    # Nếu không phải admin, kiểm tra trong cơ sở dữ liệu
    user = UserService.authenticate_user(username, password)  # Giả sử UserService có phương thức này
    
    if user:
        # Đăng nhập thành công, trả về thông tin người dùng từ DB
        return jsonify({
            'message': f'Đăng nhập thành công ({user.username})',
            'username': user.username,
            'role': user.role  # Quyền người dùng (admin hoặc người dùng bình thường)
        }), 200
    else:
        return jsonify({'error': 'Tài khoản hoặc mật khẩu không đúng'}), 401
