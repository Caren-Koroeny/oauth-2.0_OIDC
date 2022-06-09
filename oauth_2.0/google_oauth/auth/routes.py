from flask import Blueprint, render_template 


auth = Blueprint('auth', __name__)

@auth.route('/account', methods=['GET', 'POST'])
def index():
    return render_template('auth/account.html')