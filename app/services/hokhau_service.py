from app.model import HoKhau, NhanKhau, LichSuHoKhau, TamTruTamVang
from app import db
from sqlalchemy.exc import SQLAlchemyError

class HoKhauService:
    @staticmethod
    def create_hokhau(chuHo, soNha, ngayLap, ngayCapNhat):
        
        try:

            if HoKhau.query.filter_by(soNha=soNha).first():
                return None
            
            new_hokhau = HoKhau(
                soNha=soNha,
                chuHo=chuHo,
                ngayLap=ngayLap,
                ngayCapNhat=ngayCapNhat
            )
            db.session.add(new_hokhau)
            db.session.commit()
            return new_hokhau
        
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at commit: {str(e)}")
            db.session.rollback()
            return None

    @staticmethod
    def get_hokhau_by_soNha(soNha):
        
        return HoKhau.query.filter_by(soNha=soNha).first()

    @staticmethod
    def get_hokhau_by_id(id):
        
        return HoKhau.query.get(id)
    
    @staticmethod
    def get_all_hokhaus():
        
        return HoKhau.query.all()
    
    @staticmethod
    def update_HoKhau(maHoKhau, chuHo, soNha, ngayLap, ngayCapNhat):
        
        try:
            hokhau = HoKhau.query.get(maHoKhau)
            if not hokhau:
                return False
            
            hokhau.chuHo = chuHo
            hokhau.soNha = soNha
            hokhau.ngayLap = ngayLap
            hokhau.ngayCapNhat = ngayCapNhat

            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    @staticmethod
    def delete_hokhau(maHoKhau):
        
        try:
            hokhau = HoKhau.query.get(maHoKhau)
            if not hokhau:
                return False
            
            db.session.delete(hokhau)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False
        
class NhanKhauService:
    @staticmethod
    def create_nhankhau(hoTen, ngaySinh, gioiTinh, maHoKhau=None, quocTich=None, noiSinh=None, cmnd=None, qhVoiChuHo=None, trangThai=None):
        try:
            new_nhankhau = NhanKhau(
                hoTen=hoTen,
                ngaySinh=ngaySinh,
                gioiTinh=gioiTinh,
                maHoKhau=maHoKhau
            )
            
            # Các trường bổ sung
            new_nhankhau.quocTich = quocTich
            new_nhankhau.noiSinh = noiSinh
            new_nhankhau.cmnd = cmnd
            new_nhankhau.qhVoiChuHo = qhVoiChuHo
            new_nhankhau.trangThai = trangThai

            db.session.add(new_nhankhau)
            db.session.commit()
            return new_nhankhau
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at create_nhankhau: {str(e)}")
            db.session.rollback()
            return None

    @staticmethod
    def get_nhankhau_by_id(maNhanKhau):
        return NhanKhau.query.get(maNhanKhau)

    @staticmethod
    def get_all_nhankhau():
        return NhanKhau.query.all()

    @staticmethod
    def get_nhankhau_by_hoKhau(maHoKhau):
        return NhanKhau.query.filter_by(maHoKhau=maHoKhau).all()

    @staticmethod
    def update_nhankhau(maNhanKhau, hoTen=None, ngaySinh=None, gioiTinh=None, maHoKhau=None, quocTich=None, noiSinh=None, cmnd=None, qhVoiChuHo=None, trangThai=None):
        try:
            nhankhau = NhanKhau.query.get(maNhanKhau)
            if not nhankhau:
                return False

            nhankhau.hoTen = hoTen or nhankhau.hoTen
            nhankhau.ngaySinh = ngaySinh or nhankhau.ngaySinh
            nhankhau.gioiTinh = gioiTinh or nhankhau.gioiTinh
            nhankhau.maHoKhau = maHoKhau if maHoKhau is not None else nhankhau.maHoKhau
            nhankhau.quocTich = quocTich or nhankhau.quocTich
            nhankhau.noiSinh = noiSinh or nhankhau.noiSinh
            nhankhau.cmnd = cmnd or nhankhau.cmnd
            nhankhau.qhVoiChuHo = qhVoiChuHo or nhankhau.qhVoiChuHo
            nhankhau.trangThai = trangThai or nhankhau.trangThai

            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at update_nhankhau: {str(e)}")
            db.session.rollback()
            return False

    @staticmethod
    def delete_nhankhau(maNhanKhau):
        try:
            nhankhau = NhanKhau.query.get(maNhanKhau)
            if not nhankhau:
                return False

            db.session.delete(nhankhau)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at delete_nhankhau: {str(e)}")
            db.session.rollback()
            return False