from flask import Blueprint, render_template, request, flash, redirect, url_for
from data.supa import supabase
from flask_login import login_user, logout_user, login_required, current_user

from website.model.model_users import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            response = supabase.auth.sign_in_with_password({"username": username, "email": email, "password": password})
            if response.user:
                user = User.get(response.user.id)
                login_user(user)
                flash('Đăng nhập thành công!', category='success')
                return redirect(url_for('views.home'))
        except Exception as e:
            flash('Sai email hoặc mật khẩu.', category='error')
    return render_template('login.html', user=current_user)

@auth.route('/logout')
def logout():
    supabase.auth.sign_out()
    flash('Đăng xuất thành công!', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        phone = request.form.get('phone', None)  # Optional

        if len(username) < 2:
            flash('Họ tên phải lớn hơn 1 ký tự.', category='error')
        elif len(email) < 4:
            flash('Email phải lớn hơn 3 ký tự.', category='error')
        elif password1 != password2:
            flash('Mật khẩu không khớp.', category='error')
        elif len(password1) < 7:
            flash('Mật khẩu phải ít nhất 7 ký tự.', category='error')
        else:
            try:
                auth_response = supabase.auth.sign_up({
                    "email": email,
                    "password": password1
                })
                if auth_response.user:
                    # Lưu vào bảng public.user với role mặc định 'student'
                    supabase.from_('user').insert({
                        "user_id": auth_response.user.id,
                        "username": username,
                        "email": email,
                        "phone": phone,
                        "status": 'active',
                        "role": 'student'  # Mặc định 'student', admin duyệt sau
                    }).execute()
                    flash('Đăng ký thành công! Role mặc định: student.', category='success')
                    return redirect(url_for('auth.login'))
            except Exception as e:
                flash(str(e), category='error')
    return render_template('signup.html', user=current_user)