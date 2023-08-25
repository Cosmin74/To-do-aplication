from flask import Blueprint, jsonify, request, render_template,g
from user import User
import bcrypt

users_bp = Blueprint('users', __name__)

user_id_tasks = 0

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

@users_bp.route('/register', methods=['POST'])
def register_user():
    ok = 0
    last_name = request.form.get('last_name')
    first_name = request.form.get('first_name')
    email = request.form.get('email')
    password = request.form.get('pass')
    secret = hash_password(password)
    new_user = User(
        first_name= first_name,
        last_name= last_name,
        email= email,
        encrypt_pass=secret
    )
    new_user.save()
    ok = 1
    return render_template('register.html', ok= ok)

@users_bp.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')



@users_bp.route('/', methods=['GET', 'POST'])
def login_user():
    global user_id_tasks
    ok = 2  
    if request.method == 'POST':
        users = list(User.select())
        mail = request.form.get('email')
        password = request.form.get('pass_aut')
        for user in users:
            if user.email == mail and bcrypt.checkpw(password.encode('utf-8'), user.encrypt_pass.encode('utf-8')):
                user_id_tasks = user.user_id
                print("Id-ul user la logare este: " + str(user_id_tasks))
                ok = 1
                return render_template('index.html', user=user)
        ok = 0
    
    return render_template('login.html', ok=ok)    

def id_for_task():
    global user_id_tasks
    return user_id_tasks