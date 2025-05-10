from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.services.thuphi_service import *
from app.services.hokhau_service import *
from datetime import datetime

tp = Blueprint('tp', __name__)

@tp.route('/khoanthu', methods=['GET'])
@login_required
def khoanthu():
    # Kiểm tra quyền hạn, chỉ admin và kế toán mới có quyền truy cập
    if current_user.vaiTro not in ['Kế toán']:
        flash('Không có quyền truy cập trang', 'danger')
        return redirect(url_for('auth.home'))
    
    khoanthus = KhoanThuService.get_all_khoanthus()
    return render_template('khoanthu.html', khoanthus=khoanthus)

@tp.route('/khoanthu/add', methods=['POST'])
@login_required
def add_khoanthu():
    if current_user.vaiTro not in ['Kế toán']:
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    data = request.form
    ten_khoanthu = data.get('tenKhoanThu')
    loai_khoanthu = data.get('loaiKhoanThu')
    so_tien = data.get('soTien')
    loai_sotien = data.get('loaiSoTien')
    ghi_chu = data.get('ghiChu', '')  # Thêm trường ghiChu, mặc định là rỗng
    
    if not all([ten_khoanthu, loai_khoanthu, so_tien, loai_sotien]):
        return jsonify({'success': False, 'message': 'Vui lòng điền đầy đủ thông tin'}), 400
    
    try:
        so_tien = float(so_tien)
    except ValueError:
        return jsonify({'success': False, 'message': 'Số tiền không hợp lệ'}), 400
    
    # Tạo khoản thu mới
    new_khoanthu = KhoanThuService.create_khoanthu(
        tenKhoanThu=ten_khoanthu,
        loaiKhoanThu=loai_khoanthu,
        soTien=so_tien,
        loaiSoTien=loai_sotien,
        ghiChu=ghi_chu,  # Thêm trường ghiChu
        idNguoiTao=current_user.id
    )
    
    if new_khoanthu:
        return jsonify({'success': True, 'message': 'Tạo khoản thu thành công'}), 201
    else:
        return jsonify({'success': False, 'message': 'Có lỗi xảy ra khi tạo khoản thu'}), 500

@tp.route('/khoanthu/<int:ma_khoanthu>', methods=['GET'])
@login_required
def get_khoanthu(ma_khoanthu):
    if current_user.vaiTro not in ['Kế toán']:
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    khoanthu = KhoanThuService.get_khoanthu_by_id(ma_khoanthu)
    if not khoanthu:
        return jsonify({'success': False, 'message': 'Không tìm thấy khoản thu'}), 404
    
    return jsonify({
        'maKhoanThu': khoanthu.maKhoanThu,
        'tenKhoanThu': khoanthu.tenKhoanThu,
        'loaiKhoanThu': khoanthu.loaiKhoanThu,
        'soTien': khoanthu.soTien,
        'loaiSoTien': khoanthu.loaiSoTien,
        'ghiChu': khoanthu.ghiChu,  # Thêm trường ghiChu
        'idNguoiTao': khoanthu.idNguoiTao
    }), 200

@tp.route('/khoanthu/<int:ma_khoanthu>', methods=['PUT'])
@login_required
def update_khoanthu(ma_khoanthu):
    if current_user.vaiTro not in ['admin', 'Kế toán']:
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    data = request.json
    ten_khoanthu = data.get('tenKhoanThu')
    loai_khoanthu = data.get('loaiKhoanThu')
    so_tien = data.get('soTien')
    loai_sotien = data.get('loaiSoTien')
    ghi_chu = data.get('ghiChu', '')  # Thêm trường ghiChu, mặc định là rỗng
    
    if not all([ten_khoanthu, loai_khoanthu, so_tien, loai_sotien]):
        return jsonify({'success': False, 'message': 'Vui lòng điền đầy đủ thông tin'}), 400
    
    try:
        so_tien = float(so_tien)
    except ValueError:
        return jsonify({'success': False, 'message': 'Số tiền không hợp lệ'}), 400
    
    # Cập nhật khoản thu
    result = KhoanThuService.update_khoanthu(
        maKhoanThu=ma_khoanthu,
        tenKhoanThu=ten_khoanthu,
        loaiKhoanThu=loai_khoanthu,
        soTien=so_tien,
        loaiSoTien=loai_sotien,
        ghiChu=ghi_chu,  # Thêm trường ghiChu
    )
    
    if result:
        return jsonify({'success': True, 'message': 'Cập nhật khoản thu thành công'}), 200
    else:
        return jsonify({'success': False, 'message': 'Không tìm thấy khoản thu hoặc có lỗi xảy ra'}), 404

@tp.route('/khoanthu/<int:ma_khoanthu>', methods=['DELETE'])
@login_required
def delete_khoanthu(ma_khoanthu):
    if current_user.vaiTro not in ['admin', 'Kế toán']:
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    # Xóa khoản thu
    result = KhoanThuService.delete_khoanthu(ma_khoanthu)
    if result:
        return jsonify({'success': True, 'message': 'Xóa khoản thu thành công'}), 200
    else:
        return jsonify({'success': False, 'message': 'Không tìm thấy khoản thu hoặc có lỗi xảy ra'}), 404
    

@tp.route('/dotthu', methods=['GET'])
@login_required
def dotthu():
    dotthus = DotThuService.get_all_dotthus()
    return render_template('dotthu.html', dotthus=dotthus)

@tp.route('/dotthu/add', methods=['POST'])
@login_required
def add_dotthu():
    if request.method == 'POST':
        tenDotThu = request.form.get('tenDotThu')
        ngayBatDau = datetime.strptime(request.form.get('ngayBatDau'), '%Y-%m-%d').date()
        ngayKetThuc = datetime.strptime(request.form.get('ngayKetThuc'), '%Y-%m-%d').date()
        trangThai = request.form.get('trangThai', 'Đang thực hiện')
        
        # Kiểm tra tên đợt thu đã tồn tại chưa
        if DotThuService.get_dotthu_by_name(tenDotThu):
            return jsonify({'success': False, 'message': 'Tên đợt thu đã tồn tại!'})
        
        # Kiểm tra ngày bắt đầu phải sớm hơn ngày kết thúc
        if ngayBatDau > ngayKetThuc:
            return jsonify({'success': False, 'message': 'Ngày bắt đầu phải sớm hơn ngày kết thúc!'})
        
        result = DotThuService.create_dotthu(
            tenDotThu=tenDotThu,
            ngayBatDau=ngayBatDau,
            ngayKetThuc=ngayKetThuc,
            trangThai=trangThai
        )
        
        if result:
            return jsonify({'success': True, 'message': 'Thêm đợt thu thành công!'})
        else:
            return jsonify({'success': False, 'message': 'Thêm đợt thu thất bại!'})
        











@tp.route('/dotthu/<int:maDotThu>', methods=['GET'])
@login_required
def dotthu_chitiet(maDotThu):
    dotthu = DotThuService.get_dotthu_by_id(maDotThu)


    maHoKhau=1
    hokhau = HoKhauService.get_hokhau_by_id(maHoKhau)
    nhankhaus = NhanKhauService.get_nhankhau_by_hoKhau(maHoKhau)
    if not hokhau:
        flash('Không tìm thấy hộ khẩu', 'danger')
        return redirect(url_for('hk.hokhau'))
    
    chu_ho = None
    if hokhau and hokhau.chuHo != 0:
        for nk in nhankhaus:
            if nk.maNhanKhau == hokhau.chuHo:
                chu_ho = nk.hoTen
                break

    return render_template('dotthu_chitiet.html', dotthu=dotthu, hokhau=hokhau, nhankhaus=nhankhaus)
