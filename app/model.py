from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.extension import db
from flask_login import UserMixin

class TaiKhoan(db.Model, UserMixin):
    __tablename__ = 'taikhoan'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    vaiTro = db.Column(db.String(50))
    hoTen = db.Column(db.String(100))
    
    # Relationships
    nopphis = db.relationship('NopPhi', backref='taikhoan', lazy=True)
    
    def __init__(self, username, password, vaiTro, hoTen):
        self.username = username
        self.password = password
        self.vaiTro = vaiTro
        self.hoTen = hoTen
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<TaiKhoan {self.username}>'


class KhoanThu(db.Model):
    __tablename__ = 'khoanthu'
    
    maKhoanThu = db.Column(db.Integer, primary_key=True)
    tenKhoanThu = db.Column(db.String(100), nullable=False)
    loaiKhoanThu = db.Column(db.String(50))
    soTien = db.Column(db.Float)
    loaiSoTien = db.Column(db.String(50))  # "Tiền mặt" or "Chuyển khoản"
    idNguoiTao = db.Column(db.Integer, db.ForeignKey('taikhoan.id'))
    
    # Relationships
    khoanthu_has_dotthus = db.relationship('KhoanThu_Has_DotThu', backref='khoanthu', lazy=True)
    
    def __init__(self, tenKhoanThu, loaiKhoanThu, soTien, loaiSoTien, idNguoiTao):
        self.tenKhoanThu = tenKhoanThu
        self.loaiKhoanThu = loaiKhoanThu
        self.soTien = soTien
        self.loaiSoTien = loaiSoTien
        self.idNguoiTao = idNguoiTao
    
    def __repr__(self):
        return f'<KhoanThu {self.tenKhoanThu}>'

class DotThu(db.Model):
    __tablename__ = 'dotthu'
    
    maDotThu = db.Column(db.Integer, primary_key=True)
    tenDotThu = db.Column(db.String(100), nullable=False)
    ngayBatDau = db.Column(db.Date)
    ngayKetThuc = db.Column(db.Date)
    trangThai = db.Column(db.String(50))
    
    # Relationships
    khoanthu_has_dotthus = db.relationship('KhoanThu_Has_DotThu', backref='dotthu', lazy=True)
    
    def __init__(self, tenDotThu, ngayBatDau, ngayKetThuc, trangThai="Đang thực hiện"):
        self.tenDotThu = tenDotThu
        self.ngayBatDau = ngayBatDau
        self.ngayKetThuc = ngayKetThuc
        self.trangThai = trangThai
    
    def __repr__(self):
        return f'<DotThu {self.tenDotThu}>'


class KhoanThu_Has_DotThu(db.Model):
    __tablename__ = 'khoanthu_has_dotthu'
    
    idKhoanThuDotThu = db.Column(db.Integer, primary_key=True)
    maKhoanThu = db.Column(db.Integer, db.ForeignKey('khoanthu.maKhoanThu'))
    maDotThu = db.Column(db.Integer, db.ForeignKey('dotthu.maDotThu'))
    
    # Relationships
    nopphis = db.relationship('NopPhi', backref='khoanthu_has_dotthu', lazy=True)
    
    def __init__(self, maKhoanThu, maDotThu):
        self.maKhoanThu = maKhoanThu
        self.maDotThu = maDotThu
    
    def __repr__(self):
        return f'<KhoanThu_Has_DotThu {self.idKhoanThuDotThu}>'


class NopPhi(db.Model):
    __tablename__ = 'nopphi'
    
    IDNopTien = db.Column(db.Integer, primary_key=True)
    ngayThu = db.Column(db.Date)
    soTien = db.Column(db.Float)
    nguoiNop = db.Column(db.String(100))
    idNguoiThu = db.Column(db.Integer, db.ForeignKey('taikhoan.id'))
    maHoKhau = db.Column(db.Integer, db.ForeignKey('hokhau.maHoKhau'))
    idKhoanThuDotThu = db.Column(db.Integer, db.ForeignKey('khoanthu_has_dotthu.idKhoanThuDotThu'))
    
    def __init__(self, soTien, nguoiNop, idKhoanThuDotThu, maHoKhau, idNguoiThu, ngayThu):
        self.soTien = soTien
        self.nguoiNop = nguoiNop
        self.idKhoanThuDotThu = idKhoanThuDotThu
        self.maHoKhau = maHoKhau
        self.idNguoiThu = idNguoiThu
        self.ngayThu = ngayThu if ngayThu else datetime.now().date()
    
    def __repr__(self):
        return f'<NopPhi {self.IDNopTien}>'
    

class HoKhau(db.Model):
    __tablename__ = 'hokhau'
    
    maHoKhau = db.Column(db.Integer, primary_key=True)
    chuHo = db.Column(db.Integer, nullable=False)
    diaChi = db.Column(db.String(255), nullable=False)
    ngayLap = db.Column(db.Date)
    ngayCapNhat = db.Column(db.Date)

    # Relationships
    lichsuhokhau = db.relationship('LichSuHoKhau', backref='hokhau', lazy=True)
    nhankhau = db.relationship('NhanKhau', backref='hokhau', lazy=True)
    
    def __init__(self, chuHo, diaChi, ngayLap, ngayCapNhat):
        self.chuHo = chuHo
        self.diaChi = diaChi
        self.ngayLap = ngayLap
        self.ngayCapNhat = ngayCapNhat

    def __repr__(self):
        return f'<HoKhau {self.maHoKhau}>'


class NhanKhau(db.Model):
    __tablename__ = 'nhankhau'
    
    maNhanKhau = db.Column(db.Integer, primary_key=True)
    hoTen = db.Column(db.String(100), nullable=False)
    ngaySinh = db.Column(db.Date)
    gioiTinh = db.Column(db.String(10))
    maHoKhau = db.Column(db.Integer, db.ForeignKey('hokhau.maHoKhau'))
    
    # Relationships
    lichsuhokhau = db.relationship('LichSuHoKhau', backref='nhankhau', lazy=True)
    tamtrutamvang = db.relationship('TamTruTamVang', backref='nhankhau', lazy=True)
    
    def __init__(self, hoTen, ngaySinh, gioiTinh, maHoKhau):
        self.hoTen = hoTen
        self.ngaySinh = ngaySinh
        self.gioiTinh = gioiTinh
        self.maHoKhau = maHoKhau
    
    def __repr__(self):
        return f'<NhanKhau {self.hoTen}>'


class LichSuHoKhau(db.Model):
    __tablename__ = 'lichsuhokhau'
    
    id = db.Column(db.Integer, primary_key=True)
    loaiThayDoi = db.Column(db.String(45))
    thoiGian = db.Column(db.DateTime)
    maHoKhau = db.Column(db.Integer, db.ForeignKey('hokhau.maHoKhau'))
    maNhanKhau = db.Column(db.Integer, db.ForeignKey('nhankhau.maNhanKhau'))
    
    def __init__(self, loaiThayDoi, maHoKhau, maNhanKhau, thoiGian):
        self.loaiThayDoi = loaiThayDoi
        self.maHoKhau = maHoKhau
        self.maNhanKhau = maNhanKhau
        self.thoiGian = thoiGian if thoiGian else datetime.now()
    
    def __repr__(self):
        return f'<LichSuHoKhau {self.id}>'





class TamTruTamVang(db.Model):
    __tablename__ = 'tamtrutamvang'
    
    id = db.Column(db.Integer, primary_key=True)
    loai = db.Column(db.String(50))  # "Tạm trú" or "Tạm vắng"
    ngayBatDau = db.Column(db.Date)
    ngayKetThuc = db.Column(db.Date)
    lyDo = db.Column(db.String(1000))
    maNhanKhau = db.Column(db.Integer, db.ForeignKey('nhankhau.maNhanKhau'))
    
    def __init__(self, loai, maNhanKhau, ngayBatDau, ngayKetThuc, lyDo):
        self.loai = loai
        self.maNhanKhau = maNhanKhau
        self.ngayBatDau = ngayBatDau if ngayBatDau else datetime.now().date()
        self.ngayKetThuc = ngayKetThuc
        self.lyDo = lyDo
    
    def __repr__(self):
        return f'<TamTruTamVang {self.id}>'