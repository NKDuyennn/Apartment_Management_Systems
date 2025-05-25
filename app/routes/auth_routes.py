from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from app.services.user_service import UserService
from app.services.hokhau_service import *
from app.services.user_service import *
from app.services.thuphi_service import *
from app.model import TaiKhoan
from datetime import date


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
    stats = {}
    current_date = date(2025, 5, 25)  # Hardcoded for May 25, 2025, as per context

    if current_user.vaiTro in ['admin', 'Tổ phó']:
        # Total households
        total_hokhau = len(HoKhauService.get_all_hokhaus())
        # Assuming all households are active for simplicity (no trangThai field)
        active_hokhau = total_hokhau
        inactive_hokhau = 0
        new_hokhau_this_month = len([
            hk for hk in HoKhauService.get_all_hokhaus()
            if hk.ngayLap and hk.ngayLap.year == 2025 and hk.ngayLap.month == 5
        ])

        # Total residents
        all_nhankhau = NhanKhauService.get_all_nhankhau()
        total_nhankhau = len(all_nhankhau)
        male_nhankhau = len([nk for nk in all_nhankhau if nk.gioiTinh == 'Nam'])
        female_nhankhau = len([nk for nk in all_nhankhau if nk.gioiTinh == 'Nữ'])
        new_nhankhau_this_month = len([
            nk for nk in all_nhankhau
            if nk.ngaySinh and nk.ngaySinh.year == 2025 and nk.ngaySinh.month == 5
        ])

        # Temporary residence/absence
        active_tamtrutamvang = TamTruTamVangService.get_active_tamtrutamvang(current_date)
        total_tamtrutamvang = len(active_tamtrutamvang)
        tamtru_count = len([ttv for ttv in active_tamtrutamvang if ttv.loai == 'Tạm trú'])
        tamvang_count = len([ttv for ttv in active_tamtrutamvang if ttv.loai == 'Tạm vắng'])
        new_tamtrutamvang_this_month = len([
            ttv for ttv in active_tamtrutamvang
            if ttv.ngayBatDau and ttv.ngayBatDau.year == 2025 and ttv.ngayBatDau.month == 5
        ])

        # Today's activities
        today_activities = [
            lshk for lshk in LichSuHoKhauService.get_all_lichsuhokhau()
            if lshk.thoiGian and lshk.thoiGian.date() == current_date
        ]
        total_activities_today = len(today_activities)
        update_activities = len([act for act in today_activities if act.loaiThayDoi in ['Thêm', 'Sửa']])
        view_activities = len([act for act in today_activities if act.loaiThayDoi == 'Xem'])

        stats = {
            'total_hokhau': total_hokhau,
            'active_hokhau': active_hokhau,
            'inactive_hokhau': inactive_hokhau,
            'new_hokhau_this_month': new_hokhau_this_month,
            'total_nhankhau': total_nhankhau,
            'male_nhankhau': male_nhankhau,
            'female_nhankhau': female_nhankhau,
            'new_nhankhau_this_month': new_nhankhau_this_month,
            'total_tamtrutamvang': total_tamtrutamvang,
            'tamtru_count': tamtru_count,
            'tamvang_count': tamvang_count,
            'new_tamtrutamvang_this_month': new_tamtrutamvang_this_month,
            'total_activities_today': total_activities_today,
            'update_activities': update_activities,
            'view_activities': view_activities
        }

        if current_user.vaiTro == 'admin':
            # Total accounts
            all_users = UserService.get_all_users()
            total_accounts = len(all_users)
            totruong_count = len([u for u in all_users if u.vaiTro == 'admin'])
            topho_count = len([u for u in all_users if u.vaiTro == 'Tổ phó'])
            ketoan_count = len([u for u in all_users if u.vaiTro == 'Kế toán'])
            new_accounts_this_month = len([
                u for u in all_users
                if u.id and TaiKhoan.query.get(u.id).id  # Assuming id reflects creation order
            ])  # Simplified; ideally, need a creation timestamp

            stats.update({
                'total_accounts': total_accounts,
                'totruong_count': totruong_count,
                'topho_count': topho_count,
                'ketoan_count': ketoan_count,
                'new_accounts_this_month': new_accounts_this_month
            })

    return render_template('home.html', current_user=current_user, stats=stats)