# src/website/services/auth_service.py
from data.supa import supabase
from flask import flash

class Authservice:
    def signup(self, username, email, password1, password2, phone=None):
        if len(username) < 2:
            return flash('Họ tên phải lớn hơn 1 ký tự.', category='error')
        if len(email) < 4:
            return flash('Email phải lớn hơn 3 ký tự.', category='error')
        if password1 != password2:
            return flash('Mật khẩu không khớp.', category='error')
        if len(password1) < 7:
            return flash('Mật khẩu phải ít nhất 7 ký tự.', category='error')
        
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
                else:
                    flash('Đăng ký thất bại. Vui lòng thử lại.', category='error')
        except Exception as e:
                flash(str(e), category='error')

    
    
    def login(self, email, password):
        try:
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if response.user:
                return {"success": True, "user_id": response.user.id}
            else:
                return {"error": "Sai email hoặc mật khẩu."}
        except Exception as e:
            return {"error": str(e)}

    