from app.model import TaiKhoan
from app import db

class UserService:
    @staticmethod
    def authenticate_user(username, password):
        """
        Xác thực người dùng bằng tên đăng nhập và mật khẩu.
        Trả về đối tượng người dùng nếu xác thực thành công, ngược lại trả về None.
        """
        user = TaiKhoan.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def create_user(username, password, vaiTro, hoTen):
        """
        Tạo người dùng mới.
        Trả về đối tượng người dùng đã tạo hoặc None nếu người dùng đã tồn tại.
        """
        if TaiKhoan.query.filter_by(username=username).first():
            return None  # Người dùng đã tồn tại
        
        new_user = TaiKhoan(
            username=username,
            vaiTro=vaiTro,
            hoTen=hoTen
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def get_user_by_username(username):
        """
        Lấy thông tin người dùng bằng tên đăng nhập.
        """
        return TaiKhoan.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_id(user_id):
        """
        Lấy thông tin người dùng bằng ID.
        """
        return TaiKhoan.query.get(user_id)
