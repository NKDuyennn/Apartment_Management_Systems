from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.services.hokhau_service import *
from datetime import datetime

hk = Blueprint('hk', __name__)

@hk.route('/hokhau', methods=['GET'])
@login_required
def hokhau():
    hokhaus = HoKhauService.get_all_hokhaus()
    nhankhaus = NhanKhauService.get_all_nhankhau()
    return render_template('hokhau.html', hokhaus=hokhaus, nhankhaus=nhankhaus)

@hk.route('/hokhau/add', methods=['POST'])
@login_required
def add_new_hokhau():
    if current_user.vaiTro != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    data = request.form
    soNha = data.get('soNha')
    ngayLap = data.get('ngayLap')
    ngayCapNhat = data.get('ngayCapNhat')
    
    
    chuHo_val = data.get('chuHo')
    chuHo = int(chuHo_val) if chuHo_val else 0
    
    # Debug information
    print(f"Form data received: soNha={soNha}, ngayLap={ngayLap}, ngayCapNhat={ngayCapNhat}, chuHo={chuHo}")

    ngayCapNhat = datetime.strptime(ngayCapNhat, '%Y-%m-%d').date() if ngayCapNhat else datetime.now().date()
    ngayLap = datetime.strptime(ngayLap, '%Y-%m-%d').date() if ngayLap else datetime.now().date()
    
    if not all([soNha, ngayLap, ngayCapNhat]):         
        return jsonify({'success': False, 'message': 'Vui lòng điền đầy đủ thông tin'}), 400 
    
    # Tạo tài khoản mới
    new_hokhau = HoKhauService.create_hokhau(chuHo, soNha, ngayLap, ngayCapNhat)
    
    if new_hokhau:
        return jsonify({'success': True, 'message': 'Tạo hộ khẩu thành công'}), 201
    else:
        return jsonify({'success': False, 'message': 'Hộ khẩu đã tồn tại'}), 400

@hk.route('/hokhau/<int:maHoKhau>/update', methods=['PUT'])
@login_required
def update_hokhau(maHoKhau):
    if current_user.vaiTro != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403

    data = request.form

    chuHo_val = data.get('chuHo')
    chuHo = int(chuHo_val) if chuHo_val and chuHo_val.isdigit() else 0

    soNha = data.get('soNha')
    ngayLap_str = data.get('ngayLap')
    ngayCapNhat_str = data.get('ngayCapNhat')

    # Parse ngày lập và ngày cập nhật
    try:
        ngayLap = datetime.strptime(ngayLap_str, '%Y-%m-%d').date()
        ngayCapNhat = datetime.strptime(ngayCapNhat_str, '%Y-%m-%d').date()
    except Exception as e:
        return jsonify({'success': False, 'message': 'Ngày không hợp lệ'}), 400

    if not all([soNha, ngayLap, ngayCapNhat]):
        return jsonify({'success': False, 'message': 'Vui lòng điền đầy đủ thông tin'}), 400

    success = HoKhauService.update_HoKhau(maHoKhau, chuHo, soNha, ngayLap, ngayCapNhat)
    if success:
        return jsonify({'success': True, 'message': 'Cập nhật hộ khẩu thành công'}), 200
    else:
        return jsonify({'success': False, 'message': 'Cập nhật thất bại hoặc không tìm thấy hộ khẩu'}), 400


@hk.route('/hokhau/<int:maHoKhau>/delete', methods=['DELETE'])
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

    return render_template('hokhau_chitiet.html', hokhau=hokhau, nhankhaus=nhankhaus, chu_ho=chu_ho)

@hk.route('/nhankhau/add', methods=['POST'])
@login_required
def create_nhankhau():
    if current_user.vaiTro != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    # Lấy dữ liệu từ request JSON
    data = request.json
    
    # Trích xuất các trường bắt buộc
    hoTen = data.get('hoTen')
    ngaySinh = data.get('ngaySinh')
    gioiTinh = data.get('gioiTinh')
    maHoKhau = data.get('maHoKhau')
    
    # Trích xuất các trường không bắt buộc
    quocTich = data.get('quocTich', 'Việt Nam')
    noiSinh = data.get('noiSinh')
    cmnd = data.get('cmnd')
    qhVoiChuHo = data.get('qhVoiChuHo')
    trangThai = data.get('trangThai', 'Thường trú')
    
    # Kiểm tra các trường bắt buộc
    if not all([hoTen, ngaySinh, gioiTinh, maHoKhau]):
        return jsonify({
            'success': False, 
            'message': 'Vui lòng điền đầy đủ các thông tin bắt buộc (họ tên, ngày sinh, giới tính)'
        }), 400
    
    # Chuyển đổi ngày sinh từ chuỗi sang đối tượng date
    try:
        ngaySinh = datetime.strptime(ngaySinh, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({
            'success': False, 
            'message': 'Định dạng ngày sinh không hợp lệ. Sử dụng định dạng YYYY-MM-DD'
        }), 400
    
    # Kiểm tra xem hộ khẩu có tồn tại không
    ho_khau = HoKhauService.get_hokhau_by_id(int(maHoKhau))
    if not ho_khau:
        return jsonify({
            'success': False, 
            'message': 'Không tìm thấy hộ khẩu với mã đã cung cấp'
        }), 404
    
    # Tạo nhân khẩu mới
    try:
        new_nhankhau = NhanKhauService.create_nhankhau(
            hoTen=hoTen,
            ngaySinh=ngaySinh,
            gioiTinh=gioiTinh,
            maHoKhau=int(maHoKhau),
            quocTich=quocTich,
            noiSinh=noiSinh,
            cmnd=cmnd,
            qhVoiChuHo=qhVoiChuHo,
            trangThai=trangThai
        )
        
        # Kiểm tra xem có phải là chủ hộ không và cập nhật hộ khẩu nếu cần
        if qhVoiChuHo == 'Chủ hộ':
            HoKhauService.update_HoKhau(
                maHoKhau=int(maHoKhau),
                chuHo=new_nhankhau.maNhanKhau,
                soNha=ho_khau.soNha,
                ngayLap=ho_khau.ngayLap,
                ngayCapNhat=datetime.now().date()
            )
        
        return jsonify({
            'success': True, 
            'message': 'Tạo nhân khẩu mới thành công',
            'maNhanKhau': new_nhankhau.maNhanKhau
        }), 201
        
    except Exception as e:
        print(f"Lỗi khi tạo nhân khẩu: {str(e)}")
        return jsonify({
            'success': False, 
            'message': f'Lỗi khi tạo nhân khẩu: {str(e)}'
        }), 500
    
# Route to get NhanKhau details
@hk.route('/nhankhau/<int:maNhanKhau>', methods=['GET'])
@login_required
def get_nhankhau(maNhanKhau):
    try:
        nhankhau = NhanKhauService.get_nhankhau_by_id(maNhanKhau)
        if not nhankhau:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy nhân khẩu'
            }), 404
        
        return jsonify({
            'success': True,
            'maNhanKhau': nhankhau.maNhanKhau,
            'hoTen': nhankhau.hoTen,
            'ngaySinh': nhankhau.ngaySinh.strftime('%Y-%m-%d'),
            'gioiTinh': nhankhau.gioiTinh,
            'cmnd': nhankhau.cmnd or '',
            'queQuan': nhankhau.noiSinh or '',
            'maHoKhau': nhankhau.maHoKhau,
            'quanHeChuHo': nhankhau.qhVoiChuHo or '',
            'quocTich': nhankhau.quocTich or 'Việt Nam',
            'trangThai': nhankhau.trangThai or 'Thường trú'
        }), 200
    
    except Exception as e:
        print(f"Lỗi khi lấy thông tin nhân khẩu: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Lỗi khi lấy thông tin nhân khẩu: {str(e)}'
        }), 500
    
# Route to update NhanKhau
@hk.route('/nhankhau/<int:maNhanKhau>', methods=['PUT'])
@login_required
def update_nhankhau(maNhanKhau):
    if current_user.vaiTro != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    # Lấy dữ liệu từ request JSON
    data = request.json
    print(data)
    # Trích xuất các trường
    hoTen = data.get('hoTen')
    ngaySinh = data.get('ngaySinh')
    gioiTinh = data.get('gioiTinh')
    maHoKhau = data.get('maHoKhau')
    cmnd = data.get('cmnd')
    queQuan = data.get('queQuan')
    quanHeChuHo = data.get('quanHeChuHo')
    
    # Kiểm tra các trường bắt buộc
    if not all([hoTen, ngaySinh, gioiTinh, maHoKhau]):
        return jsonify({
            'success': False,
            'message': 'Vui lòng điền đầy đủ các thông tin bắt buộc (họ tên, ngày sinh, giới tính)'
        }), 400
    
    # Chuyển đổi ngày sinh
    try:
        ngaySinh = datetime.strptime(ngaySinh, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({
            'success': False,
            'message': 'Định dạng ngày sinh không hợp lệ. Sử dụng định dạng YYYY-MM-DD'
        }), 400
    
    # Kiểm tra hộ khẩu
    ho_khau = HoKhauService.get_hokhau_by_id(int(maHoKhau))
    if not ho_khau:
        return jsonify({
            'success': False,
            'message': 'Không tìm thấy hộ khẩu với mã đã cung cấp'
        }), 404
    
    # Kiểm tra nhân khẩu
    nhankhau = NhanKhauService.get_nhankhau_by_id(maNhanKhau)
    if not nhankhau:
        return jsonify({
            'success': False,
            'message': 'Không tìm thấy nhân khẩu'
        }), 404
    
    try:
        # Kiểm tra nếu mã hộ khẩu thay đổi và nhân khẩu là chủ hộ của hộ khẩu cũ
        if nhankhau.maHoKhau != int(maHoKhau):
            old_ho_khau = HoKhauService.get_hokhau_by_id(nhankhau.maHoKhau)
            if old_ho_khau and old_ho_khau.chuHo == maNhanKhau:
                # Cập nhật chủ hộ của hộ khẩu cũ thành None
                HoKhauService.update_HoKhau(
                    maHoKhau=nhankhau.maHoKhau,
                    chuHo=0,
                    soNha=old_ho_khau.soNha,
                    ngayLap=old_ho_khau.ngayLap,
                    ngayCapNhat=datetime.now().date()
                )

        # Cập nhật nhân khẩu
        NhanKhauService.update_nhankhau(
            maNhanKhau=maNhanKhau,
            hoTen=hoTen,
            ngaySinh=ngaySinh,
            gioiTinh=gioiTinh,
            maHoKhau=int(maHoKhau),
            cmnd=cmnd,
            noiSinh=queQuan,
            qhVoiChuHo=quanHeChuHo
        )
        
        # Cập nhật chủ hộ nếu cần
        if quanHeChuHo == 'Chủ hộ':
            HoKhauService.update_HoKhau(
                maHoKhau=int(maHoKhau),
                chuHo=maNhanKhau,
                soNha=ho_khau.soNha,
                ngayLap=ho_khau.ngayLap,
                ngayCapNhat=datetime.now().date()
            )
        
        return jsonify({
            'success': True,
            'message': 'Cập nhật nhân khẩu thành công'
        }), 200
    
    except Exception as e:
        print(f"Lỗi khi cập nhật nhân khẩu: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Lỗi khi cập nhật nhân khẩu: {str(e)}'
        }), 500

# Route to delete NhanKhau
@hk.route('/nhankhau/<int:maNhanKhau>', methods=['DELETE'])
@login_required
def delete_nhankhau(maNhanKhau):
    if current_user.vaiTro != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    # Kiểm tra nhân khẩu
    nhankhau = NhanKhauService.get_nhankhau_by_id(maNhanKhau)
    if not nhankhau:
        return jsonify({
            'success': False,
            'message': 'Không tìm thấy nhân khẩu'
        }), 404
    
    try:
        # Xóa nhân khẩu
        NhanKhauService.delete_nhankhau(maNhanKhau)
        
        # Nếu là chủ hộ, cập nhật hộ khẩu
        ho_khau = HoKhauService.get_hokhau_by_id(nhankhau.maHoKhau)
        if ho_khau and ho_khau.chuHo == maNhanKhau:
            HoKhauService.update_HoKhau(
                maHoKhau=nhankhau.maHoKhau,
                chuHo=0,
                soNha=ho_khau.soNha,
                ngayLap=ho_khau.ngayLap,
                ngayCapNhat=datetime.now().date()
            )
        
        return jsonify({
            'success': True,
            'message': 'Xóa nhân khẩu thành công'
        }), 200
    
    except Exception as e:
        print(f"Lỗi khi xóa nhân khẩu: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Lỗi khi xóa nhân khẩu: {str(e)}'
        }), 500