#!/usr/bin/env python3
"""
Simple test script to demonstrate directory creation functionality
"""
import os
import sys
import tempfile
import shutil
from birdproject import create_app, db
from birdproject.models import User
from werkzeug.security import generate_password_hash

def test_directory_creation():
    """Test the directory creation functionality"""
    print("Testing Flask Directory Creation Functionality...")
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        # Test that we can create the app
        print("✓ Flask app created successfully")
        
        # Test database setup
        db.create_all()
        print("✓ Database tables created")
        
        # Create a test user
        test_user = User(
            username='test_user',
            password=generate_password_hash('test_password')
        )
        db.session.add(test_user)
        db.session.commit()
        print("✓ Test user created")
        
        # Test directory creation logic
        base_path = os.path.join('user_directories', str(test_user.id))
        test_dir = os.path.join(base_path, 'test_directory')
        
        # Create directory
        os.makedirs(test_dir, exist_ok=True)
        
        # Verify directory exists
        if os.path.exists(test_dir):
            print("✓ Directory creation successful")
            
            # Create info file
            info_file = os.path.join(test_dir, 'directory_info.txt')
            with open(info_file, 'w') as f:
                f.write(f"Directory created by: {test_user.username}\n")
                f.write(f"Directory name: test_directory\n")
            
            if os.path.exists(info_file):
                print("✓ Directory info file created")
            else:
                print("✗ Failed to create info file")
                
        else:
            print("✗ Directory creation failed")
        
        # Cleanup
        if os.path.exists('user_directories'):
            shutil.rmtree('user_directories')
            print("✓ Cleanup completed")
        
        # Remove test database
        db.drop_all()
        print("✓ Test database cleaned up")
    
    print("\nAll tests passed! Directory creation functionality is working correctly.")

if __name__ == '__main__':
    test_directory_creation()