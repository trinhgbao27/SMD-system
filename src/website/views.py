from flask import Blueprint, render_template, redirect, url_for,request, flash
from flask_login import login_required, current_user
from data.supa import supabase
from middleware.role_required import role_required

views = Blueprint('views', __name__)

#HOME
@views.route('/')
def home():
    return render_template('home.html')



#STUDENT
@views.route('/student')
@login_required
def student():
    response = supabase.from_('user').select('*').execute()
    users = response.data or []
    return render_template('student.html', users=users)




#ADMIN
@views.route('/admin')
@login_required
def admin():
    users = supabase.table('user')\
        .select('user_id', 'username', 'email', 'role', 'status', 'created_at')\
        .neq('role', 'admin')\
        .execute().data
    return render_template('admin.html', users=users, current_user=current_user)

@views.route('/admin/updated_role', methods = ['POST'])
@login_required
@role_required('admin')

def update_role():
    user_id = request.form.get('user_id')
    new_role = request.form.get('role')
    
    if not user_id or not new_role:
        flash('Thiếu thông tin user hoặc role mới!', category='error')
        return redirect(url_for('views.admin'))
    
    # Cập nhật role
    response = supabase.table('user')\
        .update({'role': new_role})\
        .eq('user_id', user_id)\
        .execute()
    
    if response.data:
        flash(f'Cập nhật role cho user thành công: {new_role}', category='success')
    else:
        flash('Cập nhật thất bại. Vui lòng thử lại.', category='error')
    
    return redirect(url_for('views.admin'))













#LECTURER
@views.route('/lecturer')
@login_required
def lecturer():
    response = supabase.from_('user').select('*').execute()
    users = response.data or []
    return render_template('lecturer.html', users=users)





#ACADEMIC AFFAIRS
@views.route('/academic')
@login_required
def academic():
    response = supabase.from_('user').select('*').execute()
    users = response.data or []
    return render_template('academic.html', users=users)








#RECTOR AND HOD
@views.route('/approval')
@login_required
def approval():
    response = supabase.from_('user').select('*').execute()
    users = response.data or []
    return render_template('approval.html', users=users)