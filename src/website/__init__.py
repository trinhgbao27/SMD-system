from urllib import response
from flask import Flask
from flask_login import LoginManager


from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjhjhjhj'
    app.config['SUPABASE_URL'] = os.getenv('SUPABASE_URL')
    app.config['SUPABASE_KEY'] = os.getenv('SUPABASE_KEY')
#Init - login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from website.model.model_users import User
        return User.get(user_id)
    
#ket noi supabase va debug ket noi
    from data.supa import supabase
    try:
        response = supabase.from_('user').select('*', count=True).execute()
        print("Supabase test query:", response)
    except Exception as e:
        print("Supabase connect error:", str(e))

    from .auth import auth
    from .views import views
    from controllers.user_controller import user_controller
    #dang ky blueprint
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(user_controller, url_prefix='/')

    return app