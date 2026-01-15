from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from data.supa import supabase
from functools import wraps

user_controller = Blueprint('user_controller', __name__, url_prefix='/users')

# Decorator check role admin
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if current_user.role != 'admin':
            return jsonify({"error": "Không có quyền admin"}), 403
        return f(*args, **kwargs)
    return decorated

# Route list users (admin only)
@user_controller.route('/', methods=['GET'])
@admin_required
def list_users():
    response = supabase.from_('user').select('*').execute()
    users = response.data or []
    return render_template('admin/users.html', users=users)  # Template list users (tạo sau)

# Route update role (admin only)
@user_controller.route('/update-role/<user_id>', methods=['POST'])
@admin_required
def update_role(user_id):
    data = request.json
    new_role = data.get('role')
    allowed_roles = ['user', 'teacher', 'faculty_manager', 'admin']
    if new_role not in allowed_roles:
        return jsonify({"error": "Role không hợp lệ"}), 400

    response = supabase.from_('user').update({'role': new_role}).eq('user_id', user_id).execute()
    if response.data:
        return jsonify({"message": f"Cập nhật role thành công cho user {user_id}"}), 200
    return jsonify({"error": "Update thất bại"}), 400