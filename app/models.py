import datetime
import hashlib
import json
from datetime import date, datetime

from flask_login import UserMixin
from sqlalchemy import (Boolean, Column, Date, DateTime, Float, ForeignKey,
                        Integer, String, Text, UniqueConstraint)
from sqlalchemy.orm import backref, relationship

from app import PayingMethod, Role, Rule, Status
from app import app as my_app
from app import db


class VaiTro(db.Model):
    __tablename__ = "vai_tro"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_vai_tro = Column(String(50), nullable=True)
    user = relationship("User", backref="vai_tro", lazy=True)

    # def __int__(self):
    #     return int(self.id)


class QuyDinh(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_quy_dinh = Column(String(50), nullable=False, unique=True)
    noi_dung = Column(Text, nullable=False)
    gia_tri = Column(Integer, nullable=False, default=0)
    ngay_tao = Column(DateTime, nullable=False, default=datetime.now())
    is_active = Column(Boolean, nullable=False, default=True)


class TacGia(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_tac_gia = Column(String(225), nullable=False)
    sach = relationship("Sach", backref="tac_gia", lazy=True)

    def __str__(self):
        return self.ten_tac_gia


class TheLoai(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_the_loai = Column(String(225), nullable=False, unique=True)
    sach = relationship("Sach", backref="the_loai", lazy=True)

    def __str__(self):
        return self.ten_the_loai


class TrangThaiDonHang(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_trang_thai = Column(String(50), nullable=False)

    don_hang = relationship("DonHang", backref="trang_thai_don_hang", lazy=True)


class PhuongThucThanhToan(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_phuong_thuc = Column(String(50), nullable=False)

    don_hang = relationship("DonHang", backref="phuong_thuc_thanh_toan", lazy=True)


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ho = Column(String(50), nullable=False)
    ten = Column(String(50), nullable=False)
    username = Column(String(225), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    ngay_tao = Column(DateTime, nullable=False, default=datetime.now())
    avatar = Column(String(225))
    vai_tro_id = Column(Integer, ForeignKey(VaiTro.id), nullable=False)

    phieu_nhap_sach = relationship("PhieuNhapSach", backref="user", lazy=True)
    don_hang_kh = relationship(
        "DonHang", backref="khach_hang", foreign_keys="DonHang.khach_hang_id", lazy=True
    )
    don_hang_nv = relationship(
        "DonHang", backref="nhan_vien", foreign_keys="DonHang.nhan_vien_id", lazy=True
    )
    comments = relationship("Comment", backref="user", lazy=True)

    # hoa_don_ban_sach=relationship('HoaDonBanSach',backref='user',lazy=True)
    def __str__(self):
        return self.ten


# class HoaDonBanSach(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     ngay_tao_hoa_don = Column(DateTime, nullable=False, default=datetime.now())
#
#     nhan_vien = Column(Integer, ForeignKey(User.id), nullable=True)
#     sach = relationship('ChiTietHoaDon', backref='hoa_don_ban_sach')


class Sach(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_sach = Column(String(100), nullable=False)
    don_gia = Column(Float, nullable=False)
    bia_sach = Column(String(225))
    noi_dung = Column(Text, nullable=True)
    nam_phat_hanh = Column(Integer, nullable=True)
    so_luong = Column(Integer, default=0)

    the_loai_id = Column(Integer, ForeignKey(TheLoai.id), nullable=False)
    tac_gia_id = Column(Integer, ForeignKey(TacGia.id), nullable=False)

    # hoa_don_ban_sach = relationship('ChiTietHoaDon', backref='sach')
    phieu_nhap_sach = relationship("ChiTietPhieuNhapSach", backref="sach", lazy=True)
    don_hang = relationship("ChiTietDonHang", backref="sach", lazy=True)
    comments = relationship("Comment", backref="sach", lazy=True)

    def __str__(self):
        return self.ten_sach


class PhieuNhapSach(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngay_nhap = Column(DateTime, nullable=False, default=datetime.now())

    quan_ly_kho_id = Column(Integer, ForeignKey(User.id), nullable=False)
    sach = relationship("ChiTietPhieuNhapSach", backref="phieu_nhap_sach")

    def __int__(self):
        return self.id


class ChiTietPhieuNhapSach(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    phieu_nhap_sach_id = Column(
        Integer,
        ForeignKey(PhieuNhapSach.id, ondelete="CASCADE"),
    )
    sach_id = Column(Integer, ForeignKey(Sach.id))

    so_luong = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("sach_id", "phieu_nhap_sach_id", name="uix_sach_phieunhap"),
    )


class DonHang(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngay_tao_don = Column(DateTime, nullable=False, default=datetime.now())

    phuong_thuc_id = Column(Integer, ForeignKey(PhuongThucThanhToan.id), nullable=False)
    trang_thai_id = Column(Integer, ForeignKey(TrangThaiDonHang.id), nullable=False)
    khach_hang_id = Column(Integer, ForeignKey(User.id), nullable=True)
    nhan_vien_id = Column(Integer, ForeignKey(User.id), nullable=True)
    thong_tin_nhan_hang = relationship(
        "ThongTinNhanHang", uselist=False, backref="don_hang"
    )
    sach = relationship("ChiTietDonHang", backref="don_hang")

    # def __class__(self):
    #      return self


# class NhanVien_DonHang(db.Model):
#     donhang_id=Column(Integer,ForeignKey(DonHang.id, ondelete='CASCADE'),primary_key=True,nullable=False)
#     nhanvien_id=Column(Integer,ForeignKey(User.id),primary_key=False,nullable=False)
#
#     ngay_than_toan=Column(DateTime, nullable=False, default=datetime.now())


class ThongTinNhanHang(db.Model):
    id = Column(Integer, ForeignKey(DonHang.id, ondelete="CASCADE"), primary_key=True)
    dien_thoai_nhan_hang = Column(String(50), nullable=False)
    dia_chi_nhan_hang = Column(String(225), nullable=False)


class ChiTietDonHang(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)

    don_hang_id = Column(
        Integer,
        ForeignKey(DonHang.id),
    )
    sach_id = Column(Integer, ForeignKey(Sach.id))

    so_luong = Column(Integer, nullable=False, default=0)
    tong_tien = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint("sach_id", "don_hang_id", name="uix_sach_donhang"),
    )


class Comment(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    sach_id = Column(Integer, ForeignKey(Sach.id, ondelete="CASCADE"), nullable=False)
    ngay_tao = Column(DateTime, default=datetime.now())


if __name__ == "__main__":
    with my_app.app_context():

        # db.drop_all()
        db.create_all()

        db.session.commit()
        # vt1 = VaiTro(ten_vai_tro=Role.QUANLY.value)
        # vt2 = VaiTro(ten_vai_tro=Role.NHAN_VIEN.value)
        # vt3 = VaiTro(ten_vai_tro=Role.QUAN_LY_KHO.value)
        # vt4 = VaiTro(ten_vai_tro=Role.KHACH_HANG.value)
        #
        # db.session.add_all([vt1,vt2,vt3,vt4])
        # db.session.commit()
        # db.session.query(User).delete()
        #

        pt1 = PhuongThucThanhToan(ten_phuong_thuc=PayingMethod.ONLINE_PAY.value)
        pt2 = PhuongThucThanhToan(ten_phuong_thuc=PayingMethod.OFFLINE_PAY.value)
        db.session.add_all([pt1, pt2])

        tt1 = TrangThaiDonHang(ten_trang_thai=Status.PAID.value)
        tt2 = TrangThaiDonHang(ten_trang_thai=Status.WAITING.value)
        tt3 = TrangThaiDonHang(ten_trang_thai=Status.FAIL.value)
        db.session.add_all([tt1, tt2, tt3])

        r1 = VaiTro(ten_vai_tro=Role.QUANLY.value)
        r2 = VaiTro(ten_vai_tro=Role.QUAN_LY_KHO.value)
        r3 = VaiTro(ten_vai_tro=Role.NHAN_VIEN.value)
        r4 = VaiTro(ten_vai_tro=Role.KHACH_HANG.value)
        db.session.add_all([r1, r2, r3, r4])
        db.drop_all()
        db.create_all()
        db.session.commit()
        db.session.query(User).delete()

        pw = str(hashlib.md5("123".encode("utf-8")).hexdigest())
        qlk = User(ho="Le", ten="Huy", username="quanlykho", password=pw, vai_tro_id=3)
        db.session.add(qlk)

        ten_qd1 = Rule.SL_NHAP_MIN.value
        ten_qd2 = Rule.SL_MIN_TO_NHAP.value
        ten_qd3 = Rule.OUT_OF_TIME_TO_PAY.value
        qd1 = QuyDinh(
            ten_quy_dinh=ten_qd1,
            noi_dung="Số lượng tối thiểu khi nhập sách",
            gia_tri=150,
        )
        qd2 = QuyDinh(
            ten_quy_dinh=ten_qd2,
            noi_dung="Số lượng tối thiểu của đầu sách để được nhập",
            gia_tri=300,
        )
        qd3 = QuyDinh(
            ten_quy_dinh=ten_qd3,
            noi_dung="Số giờ tối đa kể từ khi đặt hàng đến lúc thanh toán",
            gia_tri=48,
        )

        db.session.add_all([qd1, qd2, qd3])
        pw = str(hashlib.md5("123".encode("utf-8")).hexdigest())

        qlk = User(ho="Le", ten="Huy", username="quanlykho", password=pw, vai_tro_id=3)
        db.session.add(qlk)

        pt1 = PhuongThucThanhToan(ten_phuong_thuc=PayingMethod.ONLINE_PAY.value)
        pt2 = PhuongThucThanhToan(ten_phuong_thuc=PayingMethod.OFFLINE_PAY.value)
        db.session.add_all([pt1, pt2])
        #
        tt1 = TrangThaiDonHang(ten_trang_thai=Status.PAID.value)
        tt2 = TrangThaiDonHang(ten_trang_thai=Status.WAITING.value)
        tt3 = TrangThaiDonHang(ten_trang_thai=Status.FAIL.value)
        db.session.add_all([tt1, tt2, tt3])
        #
        r1 = VaiTro(ten_vai_tro=Role.QUANLY.value)
        r2 = VaiTro(ten_vai_tro=Role.QUAN_LY_KHO.value)
        r3 = VaiTro(ten_vai_tro=Role.NHAN_VIEN.value)
        r4 = VaiTro(ten_vai_tro=Role.KHACH_HANG.value)
        db.session.add_all([r1, r2, r3, r4])

        ten_qd1 = Rule.SL_NHAP_MIN.value
        ten_qd2 = Rule.SL_MIN_TO_NHAP.value
        ten_qd3 = Rule.OUT_OF_TIME_TO_PAY.value
        qd1 = QuyDinh(
            ten_quy_dinh=ten_qd1,
            noi_dung="Số lượng tối thiểu khi nhập sách",
            gia_tri=150,
        )
        qd2 = QuyDinh(
            ten_quy_dinh=ten_qd2,
            noi_dung="Số lượng tối thiểu của đầu sách để được nhập",
            gia_tri=300,
        )
        qd3 = QuyDinh(
            ten_quy_dinh=ten_qd3,
            noi_dung="Số giờ tối đa kể từ khi đặt hàng đến lúc thanh toán",
            gia_tri=48,
        )

        db.session.add_all([qd1, qd2, qd3])

        admin = User(ho="Hứa", ten="Hứa", username="admin", password=pw, vai_tro_id=1)
        nhan_vien = User(
            ho="Trump", ten="Donald", username="nhanvien", password=pw, vai_tro_id=3
        )
        qlk = User(ho="Trump", ten="Donald", username="qlk", password=pw, vai_tro_id=2)
        u = User(ho="Trump", ten="Donald", username="client", password=pw, vai_tro_id=4)

        db.session.add_all([admin, nhan_vien, qlk, u])
        db.session.commit()

        with open("virtual_data/the_loai.json", "r", encoding="utf-8") as f:
            the_loai_data = json.load(f)

        # Lặp qua từng mục trong dữ liệu the_loai_data và tạo đối tượng TheLoai
        for item in the_loai_data:
            the_loai = TheLoai(ten_the_loai=item["ten_the_loai"])
            db.session.add(the_loai)

        # Lưu tất cả các đối tượng vào cơ sở dữ liệu
        db.session.commit()

        with open("virtual_data/tac_gia.json", "r", encoding="utf-8") as f:
            tac_gia_data = json.load(f)

        # Lặp qua từng mục trong dữ liệu tac_gia_data và tạo đối tượng TacGia
        for item in tac_gia_data:
            tac_gia = TacGia(ten_tac_gia=item["ten_tac_gia"])
            db.session.add(tac_gia)

        # Lưu tất cả các đối tượng vào cơ sở dữ liệu
        db.session.commit()

        with open("virtual_data/sach.json", "r", encoding="utf-8") as f:
            sach_data = json.load(f)

        # Lặp qua từng mục trong dữ liệu sach_data và tạo đối tượng Sach
        for item in sach_data:
            sach = Sach(
                ten_sach=item["ten_sach"],
                don_gia=item["don_gia"],
                bia_sach=item["bia_sach"],
                noi_dung=item["noi_dung"],
                so_luong=item["so_luong"],
                nam_phat_hanh=item["nam_phat_hanh"],
                the_loai_id=item["the_loai_id"],
                tac_gia_id=item["tac_gia_id"],
            )
            db.session.add(sach)

        # Lưu tất cả các đối tượng vào cơ sở dữ liệu
        admin = User(ho="Hứa", ten="Hứa", username="admin1", password=pw, vai_tro_id=1)
        nhan_vien = User(
            ho="Trump", ten="Donald", username="nhanvien", password=pw, vai_tro_id=3
        )
        qlk = User(ho="Trump", ten="Donald", username="qlk", password=pw, vai_tro_id=2)
        u = User(ho="Trump", ten="Donald", username="client", password=pw, vai_tro_id=4)
        db.session.add_all([admin, nhan_vien, qlk, u])

        db.session.commit()
