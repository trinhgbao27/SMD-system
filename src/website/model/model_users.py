from data.supa import supabase
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, username, email, phone=None, status='active', faculty_id=None,created_at=None, updated_at=None,role='user'):
        self.id = user_id
        self.username = username
        self.email = email
        self.phone = phone
        self.status = status
        self.faculty_id = faculty_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.role = role

    @staticmethod
    def get(user_id):
        response = supabase.from_('user').select('*').eq('id', user_id).execute()
        data = response.data
        if data:
            user_data = data[0]
            return User(
                user_id=user_data['id'], 
                username=user_data['username'], 
                email=user_data['email'],
                phone=user_data['phone'], 
                status=user_data['status'], 
                faculty_id=user_data['faculty_id'],
                created_at=user_data['created_at'], 
                updated_at=user_data['updated_at'], 
                role=user_data['role'])
        return None
    
    # Các method bắt buộc
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.status == 'active'

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
