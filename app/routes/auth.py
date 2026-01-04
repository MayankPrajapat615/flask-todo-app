from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)

# REGISTER
@auth_bp.route('/')
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists", "danger")
            return redirect(url_for('auth.register'))

        password_hash = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# LOGIN
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            flash("Login successful", "success")
            return redirect(url_for('tasks.view_tasks'))

        flash("Invalid username or password", "danger")

    return render_template('login.html')


# LOGOUT
@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully", "info")
    return redirect(url_for('auth.login'))
