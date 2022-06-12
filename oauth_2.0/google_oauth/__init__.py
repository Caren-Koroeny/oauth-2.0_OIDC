from distutils.log import Log
from flask import Flask
from google_oauth import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app=Flask(__name__)
    app.config['FLASK_ENV'] = 'development'
    app.config.from_object(config.Config)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    db.init_app(app)
    login_manager.init_app(app)
    
    with app.app_context():
        
        from google_oauth.routes import views
        from google_oauth.auth.routes import auth
        app.register_blueprint(views)
        app.register_blueprint(auth)
    # where the routes and blue prints will be initialized and called. 
    
        db.create_all() 
        migrate.init_app(app, db)
        
        
        
        
        
    return app
    
