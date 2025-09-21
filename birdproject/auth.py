from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    
    username = request.form.get('username')
    password = request.form.get('password')
    remember = bool(request.form.get('remember'))

    user = User.query.filter_by(username=username).first()

    
    if not user or not check_password_hash(user.password, password):
        flash('Невірні дані для входу. Спробуйте ще раз.')
        return redirect(url_for('auth.login'))

    
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    
    username = request.form.get('username')
    password = request.form.get('password')

    
    if User.query.filter_by(username=username).first():
        flash('Користувач з таким іменем вже існує')
        return redirect(url_for('auth.signup'))

    
    new_user = User(
        username=username, 
        password=generate_password_hash(password)
    )
    
    
    db.session.add(new_user)
    db.session.commit()
    
    flash('Реєстрація успішна! Тепер можете увійти.')
    return redirect(url_for('auth.login'))

@auth.route('/success', methods=['POST'])  
def success():  
    f = request.files['file']
    import os
    os.makedirs('birdproject/static', exist_ok=True)

    file_path = os.path.join('birdproject/static', f.filename)
    f.save(file_path)
    
    return render_template("profile.html", filename=f.filename, name=current_user.username) 

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
