from flask import Blueprint, render_template
from flask_login import login_required
from data.supa import supabase

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/dashboard')
@login_required
def dashboard():
    response = supabase.from_('user').select('*').execute()
    users = response.data or []
    return render_template('dashboard.html', users=users)

