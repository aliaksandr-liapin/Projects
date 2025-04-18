from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Device
import os
from sqlalchemy import func

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_home.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('dashboard'))
    return render_template('index.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html', title='Pricing')

@app.route('/blog')
def blog():
    return render_template('blog.html', title='Blog')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
        user = User(email=email, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        
        flash('Invalid email or password')
    
    return render_template('login.html', title='Login')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html', title='Privacy Policy')

@app.route('/faq')
def faq():
    return render_template('faq.html', title='FAQ')

@app.route('/sensor-guide')
def sensor_guide():
    return render_template('sensor_guide.html', title='Sensor Setup Guide')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html', title='Settings')

# Admin route - only accessible through direct link
@app.route('/admin-dashboard-7x9k2p')
@login_required
def admin_dashboard():
    # Check if user is admin (you should add an is_admin field to your User model)
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('index'))
    
    # Get statistics
    total_users = User.query.count()
    total_devices = Device.query.count()
    active_devices = Device.query.filter_by(status='active').count()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    device_types = db.session.query(
        Device.type,
        func.count(Device.id).label('count')
    ).group_by(Device.type).all()
    
    return render_template('admin.html',
                         total_users=total_users,
                         total_devices=total_devices,
                         active_devices=active_devices,
                         recent_users=recent_users,
                         device_types=device_types)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 