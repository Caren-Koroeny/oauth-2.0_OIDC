from flask import Flask
# from google_oauth.routes import views
from google_oauth import config

def create_app():
    app=Flask(__name__)
    app.config['FLASK_ENV'] = 'development'
    app.config.from_object(config.Config)

    
    with app.app_context():
        
        from google_oauth.routes import views
        from google_oauth.auth.routes import auth
        app.register_blueprint(views)
        app.register_blueprint(auth)
    # where the routes and blue prints will be initialized and called. 
    
        
        
        
        
        
        
    return app
    
