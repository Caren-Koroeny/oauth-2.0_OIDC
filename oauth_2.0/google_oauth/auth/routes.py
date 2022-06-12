import json
import requests
from flask import Blueprint, render_template 

from flask import redirect, request, url_for
from flask_login import (
    current_user, 
    login_required, 
    login_user,
    logout_user
)
from google_oauth.models import User
from google_oauth.config import Config
from oauthlib.oauth2 import WebApplicationClient
from google_oauth import login_manager
from google_oauth.auth.utils import get_google_provider_cfg
from google_oauth import db

auth = Blueprint('auth', __name__)
client = WebApplicationClient(Config.GOOGLE_CLIENT_ID)




@login_manager.user_loader
def load_user(unique_id):
    return User.query.filter_by(unique_id=unique_id).first()


# Login 
@auth.route('/login', methods=['GET', 'POST'])
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']
    
    request_uri = client.prepare_request_uri(
        authorization_endpoint, 
        redirect_uri=request.base_url + "/callback",
        scope=['openid', 'email', 'profile'] 
    )
    return redirect(request_uri)


@auth.route('/login/callback')
def callback():
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg['token_endpoint']
    
    token_url, headers, body = client.prepare_refresh_token_request(
        token_endpoint,
        authorization_reponse=request.url,
        redirect_url=request.base_url,
        code=code
    )
    
    token_reponse = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(Config.GOOGLE_CLIENT_ID, Config.GOOGLE_CLIENT_SECRET),
    )
    
    client.parse_request_body_response(json.dumps(token_reponse.json()))
    
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google"
    
    user = User(
        email=users_email, username=users_name, unique_id=unique_id, picture=picture
    )
    
    if not User.get_id(unique_id):
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    
    return redirect(url_for('auth.index'))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))


@auth.route('/account', methods=['GET', 'POST'])
def index():
    return render_template('auth/account.html')