from flask import Flask
from google_oauth import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app=Flask(__name__)
    app.config['FLASK_ENV'] = 'development'
    app.config.from_object(config.Config)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///user.db'

    db.init_app(app)
    
    with app.app_context():
        
        from google_oauth.routes import views
        app.register_blueprint(views)
    # where the routes and blue prints will be initialized and called. 
    
        db.create_all() 
        
        
        
        
        
    return app
    
