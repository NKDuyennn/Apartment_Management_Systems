from app.model import *
from app import db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

class KhoanThuService:
    @staticmethod
    def create_khoanthu(tenKhoanThu, loaiKhoanThu, soTien, loaiSoTien, ghiChu, idNguoiTao):
        try:
            new_khoanthu = KhoanThu(
                tenKhoanThu=tenKhoanThu,
                loaiKhoanThu=loaiKhoanThu,
                soTien=soTien,
                loaiSoTien=loaiSoTien,
                ghiChu=ghiChu,
                idNguoiTao=idNguoiTao
            )
            db.session.add(new_khoanthu)
            db.session.commit()
            return new_khoanthu
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at create_khoanthu: {str(e)}")
            db.session.rollback()
            return None

    @staticmethod
    def get_khoanthu_by_id(maKhoanThu):
        return KhoanThu.query.get(maKhoanThu)

    @staticmethod
    def get_all_khoanthus():
        return KhoanThu.query.all()
    
    @staticmethod
    def get_khoanthus_by_loai(loaiKhoanThu):
        return KhoanThu.query.filter_by(loaiKhoanThu=loaiKhoanThu).all()
    
    @staticmethod
    def get_khoanthus_by_nguoitao(idNguoiTao):
        return KhoanThu.query.filter_by(idNguoiTao=idNguoiTao).all()

    @staticmethod
    def update_khoanthu(maKhoanThu, tenKhoanThu=None, loaiKhoanThu=None, soTien=None, loaiSoTien=None, ghiChu=None):
        try:
            khoanthu = KhoanThu.query.get(maKhoanThu)
            if not khoanthu:
                return False
            
            khoanthu.tenKhoanThu = tenKhoanThu or khoanthu.tenKhoanThu
            khoanthu.loaiKhoanThu = loaiKhoanThu or khoanthu.loaiKhoanThu
            khoanthu.soTien = soTien if soTien is not None else khoanthu.soTien
            khoanthu.loaiSoTien = loaiSoTien or khoanthu.loaiSoTien
            khoanthu.ghiChu = ghiChu or khoanthu.ghiChu
            
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at update_khoanthu: {str(e)}")
            db.session.rollback()
            return False

    @staticmethod
    def delete_khoanthu(maKhoanThu):
        try:
            khoanthu = KhoanThu.query.get(maKhoanThu)
            if not khoanthu:
                return False
            
            db.session.delete(khoanthu)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at delete_khoanthu: {str(e)}")
            db.session.rollback()
            return False

class DotThuService:
    @staticmethod
    def create_dotthu(tenDotThu, ngayBatDau, ngayKetThuc, trangThai="Đang thực hiện"):
        try:
            if DotThu.query.filter_by(tenDotThu=tenDotThu).first():
                return None
                
            new_dotthu = DotThu(
                tenDotThu=tenDotThu,
                ngayBatDau=ngayBatDau,
                ngayKetThuc=ngayKetThuc,
                trangThai=trangThai
            )
            db.session.add(new_dotthu)
            db.session.commit()
            return new_dotthu
            
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at commit: {str(e)}")
            db.session.rollback()
            return None
    
    @staticmethod
    def get_dotthu_by_name(tenDotThu):
        return DotThu.query.filter_by(tenDotThu=tenDotThu).first()
    
    @staticmethod
    def get_dotthu_by_id(maDotThu):
        return DotThu.query.get(maDotThu)
        
    @staticmethod
    def get_all_dotthus():
        return DotThu.query.all()
        
    @staticmethod
    def update_dotthu(maDotThu, tenDotThu, ngayBatDau, ngayKetThuc, trangThai):
        try:
            dotthu = DotThu.query.get(maDotThu)
            if not dotthu:
                return False
                
            dotthu.tenDotThu = tenDotThu
            dotthu.ngayBatDau = ngayBatDau
            dotthu.ngayKetThuc = ngayKetThuc
            dotthu.trangThai = trangThai
            
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False
    
    @staticmethod
    def delete_dotthu(maDotThu):
        try:
            dotthu = DotThu.query.get(maDotThu)
            if not dotthu:
                return False
                
            db.session.delete(dotthu)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False
    
    @staticmethod
    def get_active_dotthus():
        return DotThu.query.filter_by(trangThai="Đang thực hiện").all()
    
    @staticmethod
    def get_dotthus_by_status(trangThai):
        return DotThu.query.filter_by(trangThai=trangThai).all()
    
    @staticmethod
    def update_status(maDotThu, trangThai):
        try:
            dotthu = DotThu.query.get(maDotThu)
            if not dotthu:
                return False
                
            dotthu.trangThai = trangThai
            
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

class KhoanThuHasDotThuService:
    @staticmethod
    def create_khoanthu_has_dotthu(maKhoanThu, maDotThu):
        try:
            # Kiểm tra khoản thu và đợt thu tồn tại
            khoanthu = KhoanThu.query.get(maKhoanThu)
            dotthu = DotThu.query.get(maDotThu)
            if not khoanthu or not dotthu:
                return None
            
            # Kiểm tra xem đã tồn tại mapping này chưa
            existing = KhoanThu_Has_DotThu.query.filter_by(
                maKhoanThu=maKhoanThu, 
                maDotThu=maDotThu
            ).first()
            if existing:
                return existing
            
            new_khoanthu_has_dotthu = KhoanThu_Has_DotThu(
                maKhoanThu=maKhoanThu,
                maDotThu=maDotThu
            )
            db.session.add(new_khoanthu_has_dotthu)
            db.session.commit()
            return new_khoanthu_has_dotthu
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at create_khoanthu_has_dotthu: {str(e)}")
            db.session.rollback()
            return None

    @staticmethod
    def get_by_id(idKhoanThuDotThu):
        return KhoanThu_Has_DotThu.query.get(idKhoanThuDotThu)

    @staticmethod
    def get_all():
        return KhoanThu_Has_DotThu.query.all()
    
    @staticmethod
    def get_by_khoanthu(maKhoanThu):
        return KhoanThu_Has_DotThu.query.filter_by(maKhoanThu=maKhoanThu).all()
    
    @staticmethod
    def get_by_dotthu(maDotThu):
        return KhoanThu_Has_DotThu.query.filter_by(maDotThu=maDotThu).all()
    
    @staticmethod
    def get_khoanthu_dotthu_details():
        return db.session.query(
            KhoanThu_Has_DotThu.idKhoanThuDotThu,
            KhoanThu.maKhoanThu,
            KhoanThu.tenKhoanThu,
            KhoanThu.loaiKhoanThu,
            KhoanThu.soTien,
            KhoanThu.loaiSoTien,
            DotThu.maDotThu,
            DotThu.tenDotThu,
            DotThu.ngayBatDau,
            DotThu.ngayKetThuc,
            DotThu.trangThai
        ).join(
            KhoanThu, KhoanThu_Has_DotThu.maKhoanThu == KhoanThu.maKhoanThu
        ).join(
            DotThu, KhoanThu_Has_DotThu.maDotThu == DotThu.maDotThu
        ).all()

    @staticmethod
    def delete(idKhoanThuDotThu):
        try:
            khoanthu_has_dotthu = KhoanThu_Has_DotThu.query.get(idKhoanThuDotThu)
            if not khoanthu_has_dotthu:
                return False
            
            db.session.delete(khoanthu_has_dotthu)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at delete KhoanThu_Has_DotThu: {str(e)}")
            db.session.rollback()
            return False

class NopPhiService:
    @staticmethod
    def create_nopphi(soTien, nguoiNop, idKhoanThuDotThu, maHoKhau, idNguoiThu, ngayThu=None):
        try:
            # Kiểm tra khoản thu đợt thu tồn tại
            khoanthu_has_dotthu = KhoanThu_Has_DotThu.query.get(idKhoanThuDotThu)
            if not khoanthu_has_dotthu:
                return None
            
            new_nopphi = NopPhi(
                soTien=soTien,
                nguoiNop=nguoiNop,
                idKhoanThuDotThu=idKhoanThuDotThu,
                maHoKhau=maHoKhau,
                idNguoiThu=idNguoiThu,
                ngayThu=ngayThu
            )
            db.session.add(new_nopphi)
            db.session.commit()
            return new_nopphi
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at create_nopphi: {str(e)}")
            db.session.rollback()
            return None

    @staticmethod
    def get_nopphi_by_id(IDNopTien):
        return NopPhi.query.get(IDNopTien)

    @staticmethod
    def get_all_nopphis():
        return NopPhi.query.all()
    
    @staticmethod
    def get_nopphis_by_hokhau(maHoKhau):
        return NopPhi.query.filter_by(maHoKhau=maHoKhau).all()
    
    @staticmethod
    def get_nopphis_by_khoanthu_dotthu(idKhoanThuDotThu):
        return NopPhi.query.filter_by(idKhoanThuDotThu=idKhoanThuDotThu).all()
    
    @staticmethod
    def get_nopphis_by_nguoithu(idNguoiThu):
        return NopPhi.query.filter_by(idNguoiThu=idNguoiThu).all()
    
    @staticmethod
    def get_nopphis_by_date_range(start_date, end_date):
        return NopPhi.query.filter(
            NopPhi.ngayThu >= start_date,
            NopPhi.ngayThu <= end_date
        ).all()
    
    @staticmethod
    def get_nopphis_with_details():
        return db.session.query(
            NopPhi.IDNopTien,
            NopPhi.ngayThu,
            NopPhi.soTien,
            NopPhi.nguoiNop,
            NopPhi.idNguoiThu,
            NopPhi.maHoKhau,
            KhoanThu.tenKhoanThu,
            KhoanThu.loaiKhoanThu,
            DotThu.tenDotThu
        ).join(
            KhoanThu_Has_DotThu, NopPhi.idKhoanThuDotThu == KhoanThu_Has_DotThu.idKhoanThuDotThu
        ).join(
            KhoanThu, KhoanThu_Has_DotThu.maKhoanThu == KhoanThu.maKhoanThu
        ).join(
            DotThu, KhoanThu_Has_DotThu.maDotThu == DotThu.maDotThu
        ).all()

    @staticmethod
    def update_nopphi(IDNopTien, soTien=None, nguoiNop=None, ngayThu=None):
        try:
            nopphi = NopPhi.query.get(IDNopTien)
            if not nopphi:
                return False
            
            nopphi.soTien = soTien if soTien is not None else nopphi.soTien
            nopphi.nguoiNop = nguoiNop or nopphi.nguoiNop
            nopphi.ngayThu = ngayThu or nopphi.ngayThu
            
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at update_nopphi: {str(e)}")
            db.session.rollback()
            return False

    @staticmethod
    def delete_nopphi(IDNopTien):
        try:
            nopphi = NopPhi.query.get(IDNopTien)
            if not nopphi:
                return False
            
            db.session.delete(nopphi)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at delete_nopphi: {str(e)}")
            db.session.rollback()
            return False
    
    @staticmethod
    def get_total_by_khoanthu(maKhoanThu):
        """Tính tổng số tiền đã thu theo khoản thu"""
        total = db.session.query(db.func.sum(NopPhi.soTien)).join(
            KhoanThu_Has_DotThu, NopPhi.idKhoanThuDotThu == KhoanThu_Has_DotThu.idKhoanThuDotThu
        ).filter(
            KhoanThu_Has_DotThu.maKhoanThu == maKhoanThu
        ).scalar()
        return total or 0
    
    @staticmethod
    def get_total_by_dotthu(maDotThu):
        """Tính tổng số tiền đã thu theo đợt thu"""
        total = db.session.query(db.func.sum(NopPhi.soTien)).join(
            KhoanThu_Has_DotThu, NopPhi.idKhoanThuDotThu == KhoanThu_Has_DotThu.idKhoanThuDotThu
        ).filter(
            KhoanThu_Has_DotThu.maDotThu == maDotThu
        ).scalar()
        return total or 0