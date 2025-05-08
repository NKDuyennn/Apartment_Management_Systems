from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.services.hokhau_service import *
from datetime import datetime

hk = Blueprint('hk', __name__)

@hk.route('/hokhau', methods=['GET'])
@login_required
def hokhau():
    hokhaus = HoKhauService.get_all_hokhaus()
    return render_template('hokhau.html', hokhaus=hokhaus)

@hk.route('/hokhau/add', methods=['POST'])
@login_required
def add_new_hokhau():
    if current_user.vaiTro != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    data = request.form
    diaChi = data.get('diaChi')
    ngayLap  = data.get('ngayLap')
    chuHo = data.get('chuHo', type=int)
    ngayLap = datetime.strptime(ngayLap, '%Y-%m-%d').date()

    if not all([diaChi, ngayLap, chuHo]):
        return jsonify({'success': False, 'message': 'Vui lòng điền đầy đủ thông tin'}), 400
    
    # Tạo tài khoản mới
    new_hokhau = HoKhauService.create_hokhau(chuHo, diaChi, ngayLap)

    if new_hokhau:
        return jsonify({'success': True, 'message': 'Tạo hộ khẩu thành công'}), 201
    else:
        return jsonify({'success': False, 'message': 'Hộ khẩu đã tồn tại'}), 400


@hk.route('/hokhau/<int:maHoKhau>', methods=['DELETE'])
@login_required
def delete_hokhau(maHoKhau):
    if current_user.vaiTro != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    result = HoKhauService.delete_hokhau(maHoKhau)

    if result:
         return jsonify({'success': True, 'message': 'Xóa hộ khẩu thành công'}), 200
    else:
        return jsonify({'success': False, 'message': 'Không tìm thấy hộ khẩu hoặc có lỗi xảy ra'}), 400
    

@hk.route('/hokhau/<int:maHoKhau>', methods=['GET'])
@login_required
def hokhau_chitiet(maHoKhau):
    hokhau = HoKhauService.get_hokhau_by_id(maHoKhau)

    if not hokhau:
        flash('Không tìm thấy hộ khẩu', 'danger')
        return redirect(url_for('hk.hokhau'))
    
    return render_template('hokhau_chitiet.html', hokhau=hokhau)