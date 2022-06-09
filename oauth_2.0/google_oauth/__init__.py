from flask import Flask
from google_oauth import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app=Flask(__name__)
    app.config['FLASK_ENV'] = 'development'
    app.config.from_object(config.Config)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        
        from google_oauth.routes import views
        app.register_blueprint(views)
    # where the routes and blue prints will be initialized and called. 
    
        db.create_all() 
        
        
        
        
        
    return app
    
