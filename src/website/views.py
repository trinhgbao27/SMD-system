from flask import Blueprint, render_template
from flask_login import login_required
from data.supa import supabase

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/student')
@login_required
def student():
    response = supabase.from_('user').select('*').execute()
    users = response.data or []
    return render_template('student.html', users=users)

@views.route('/admin')
@login_required
def admin():
    response = supabase.from_('user').select('*').execute()
    users = response.data or []
    return render_template('admin.html', users=users)