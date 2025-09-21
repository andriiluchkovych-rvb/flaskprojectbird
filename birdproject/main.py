from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
import os
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

@main.route('/create-directory')
@login_required
def create_directory_page():
    """Display the directory creation page"""
    return render_template('create_directory.html')

@main.route('/api/create-directory', methods=['POST'])
@login_required
def create_directory_api():
    """API endpoint to create directories"""
    try:
        data = request.get_json()
        directory_name = data.get('directory_name', '').strip()
        
        if not directory_name:
            return jsonify({'success': False, 'message': 'Directory name is required'}), 400
            
        # Create user-specific directory path
        base_path = os.path.join('user_directories', str(current_user.id))
        full_path = os.path.join(base_path, directory_name)
        
        # Ensure the path is safe (no traversal attacks)
        if '..' in directory_name or '/' in directory_name or '\\' in directory_name:
            return jsonify({'success': False, 'message': 'Invalid directory name'}), 400
            
        # Create the directory structure
        os.makedirs(full_path, exist_ok=True)
        
        # Create a simple info file in the directory
        info_file = os.path.join(full_path, 'directory_info.txt')
        with open(info_file, 'w') as f:
            f.write(f"Directory created by: {current_user.username}\n")
            f.write(f"Directory name: {directory_name}\n")
            f.write(f"Created at: {os.path.dirname(os.path.abspath(full_path))}\n")
        
        return jsonify({
            'success': True, 
            'message': f'Directory "{directory_name}" created successfully',
            'path': full_path
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error creating directory: {str(e)}'}), 500

@main.route('/api/list-directories', methods=['GET'])
@login_required
def list_directories_api():
    """API endpoint to list user's directories"""
    try:
        base_path = os.path.join('user_directories', str(current_user.id))
        
        if not os.path.exists(base_path):
            return jsonify({'success': True, 'directories': []})
            
        directories = []
        for item in os.listdir(base_path):
            item_path = os.path.join(base_path, item)
            if os.path.isdir(item_path):
                directories.append({
                    'name': item,
                    'path': item_path,
                    'created': os.path.getctime(item_path)
                })
                
        return jsonify({'success': True, 'directories': directories})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error listing directories: {str(e)}'}), 500

if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(main)
    app.run(debug=True)