from http import client
import json
import requests
from flask import Blueprint, render_template 

# Third-party libraries
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
# Oauth2 client setup
client = WebApplicationClient(Config.GOOGLE_CLIENT_ID)
# Client_ID from google is used to initialize our oauthlib client in the 
# WebAppClient


# Flask-Login helper to retrieve a user from the db.



# Login 
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Find out what URL to fit for Google Login, 
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    
    # Use library to construct the request for google login
    # and provide scopes that you retrieeves user's profile from google
    request_uri = client.prepare_request_uri(
        authorization_endpoint, 
        redirect_uri=request.base_url + "/callback",
        scope=['openid', 'email', 'profile'] 
    )
    return redirect(request_uri)


@auth.route('/login/callback')
def callback():
    # Get authorization code Google back to you
    code = request.args.get("code")
    # google's token endpoint.
    # Find out what URL to hit to get tokens that allows you to ask for things 
    # on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Construct a token request.
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_reponse=request.url,
        redirect_url=request.base_url,
        code=code
    )
    # use request to actually send it out
    token_reponse = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(Config.GOOGLE_CLIENT_ID, Config.GOOGLE_CLIENT_SECRET),
    )
    # Parse the tokens!
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
    #create user in the db with infor provided by google 
    user = User(
        email=users_email, username=users_name, unique_id=unique_id, profile_pic=picture
    )
    # Doesn't exist? Add it to the DB
    if not User.query.filter_by(unique_id=unique_id).first():
        db.session.add(user)
        db.session.commit()
    
    # Begin session by logging the user in
    login_user(user, force=True)
    
    # send user bacj to home page
    return redirect(url_for('auth.index'))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))


@auth.route('/account', methods=['GET', 'POST'])
def index():
    return render_template('auth/account.html')





@login_manager.user_loader
def load_user(unique_id):
    return User.query.filter_by(unique_id=unique_id).first()
    # return User.get_id(user_id)
    