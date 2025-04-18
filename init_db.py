from app import app, db
from models import User, Device
import os

def init_db():
    with app.app_context():
        # Delete existing database file if it exists
        db_file = 'instance/smart_home.db'
        if os.path.exists(db_file):
            os.remove(db_file)
            print("Existing database removed")
        
        # Create all tables
        db.create_all()
        print("Database tables created")
        
        # Create admin user
        admin = User(
            name='Admin',
            email='admin@smart.house',
            is_admin=True
        )
        admin.set_password('admin123')  # Change this password in production
        db.session.add(admin)
        
        # Create some sample devices
        devices = [
            Device(name='Living Room Temp', type='temperature', user_id=1),
            Device(name='Front Door Motion', type='motion', user_id=1),
            Device(name='Kitchen Light', type='light', user_id=1)
        ]
        db.session.add_all(devices)
        
        db.session.commit()
        print("Database initialized with admin user and sample devices")

if __name__ == '__main__':
    init_db() 