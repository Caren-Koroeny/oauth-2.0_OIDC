from flask_login import UserMixin
from google_oauth import db


class User(UserMixin, db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(80), unique = True, nullable = False)
    unique_id = db.Column(db.String(), unique=True)
    profile_pic = db.Column(db.String())
    
    
    
    def __repr__(self):
        return f'<User > {self.id, self.username,self.email, self.profile_pic}'
    
    
    def get_id(self):
        return self.unique_id