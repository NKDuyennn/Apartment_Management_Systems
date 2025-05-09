from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.services.thuphi_service import *
from datetime import datetime

tp = Blueprint('tp', __name__)

@tp.route('/khoanthu', methods=['GET'])
@login_required
def khoanthu():
    khoanthus = KhoanThuService.get_all_khoanthus()
    return render_template('khoanthu.html', khoanthus=khoanthus)

