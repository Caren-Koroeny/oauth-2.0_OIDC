from google_oauth import db


class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(80), unique = True, nullable = False)
    profile_pic = db.Column(db.String())
    
    
    
    def __repr__(self):
        return f'<User > {self.id, self.username,self.email, self.profile_pic}'
    
    