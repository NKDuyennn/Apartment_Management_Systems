from app.model import HoKhau, NhanKhau, LichSuHoKhau, TamTruTamVang
from app import db
from sqlalchemy.exc import SQLAlchemyError

class HoKhauService:
    @staticmethod
    def create_hokhau(chuHo, diaChi, ngayLap):
        
        try:

            if HoKhau.query.filter_by(diaChi=diaChi).first():
                return None
            
            new_hokhau = HoKhau(
                diaChi=diaChi,
                chuHo=chuHo,
                ngayLap=ngayLap
            )
            db.session.add(new_hokhau)
            db.session.commit()
            return new_hokhau
        
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at commit: {str(e)}")
            db.session.rollback()
            return None

    @staticmethod
    def get_hokhau_by_diaChi(diaChi):
        
        return HoKhau.query.filter_by(diaChi=diaChi).first()

    @staticmethod
    def get_hokhau_by_id(id):
        
        return HoKhau.query.get(id)
    
    @staticmethod
    def get_all_hokhaus():
        
        return HoKhau.query.all()
    
    @staticmethod
    def update_HoKhau(maHoKhau, chuHo, diaChi, ngayLap):
        
        try:
            hokhau = HoKhau.query.get(maHoKhau)
            if not hokhau:
                return False
            
            hokhau.chuHo = chuHo
            hokhau.diaChi = diaChi
            hokhau.ngayLap = ngayLap

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