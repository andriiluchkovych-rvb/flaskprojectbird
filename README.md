# flaskprojectbird

A Flask web application with user authentication and directory creation functionality.

## Features

- User registration and authentication
- Profile management
- Directory creation and management for authenticated users
- Secure directory operations with user isolation

## How to Create Directories

### Prerequisites
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python wsgi.py
   ```

### Using the Web Interface

1. **Register/Login**: Create an account or login to access directory creation features
2. **Navigate to Directory Creation**: Click "Create Directory" in the navigation menu
3. **Create Directory**: 
   - Enter a directory name (letters, numbers, and underscores only)
   - Click "Create Directory" button
   - Directory will be created in your user-specific folder

### Using the API

You can also create directories programmatically using the REST API:

#### Create Directory
```bash
POST /api/create-directory
Content-Type: application/json

{
    "directory_name": "my_new_directory"
}
```

#### List Directories
```bash
GET /api/list-directories
```

### Directory Structure

- Each user has their own isolated directory space
- Directories are created under `user_directories/{user_id}/`
- Each created directory includes a `directory_info.txt` file with metadata

### Security Features

- Directory names are validated to prevent path traversal attacks
- Users can only access their own directories
- Authentication required for all directory operations

## Project Structure

```
flaskprojectbird/
├── birdproject/           # Main Flask application
│   ├── __init__.py       # App factory
│   ├── main.py           # Main routes and directory functionality
│   ├── auth.py           # Authentication routes
│   ├── models.py         # Database models
│   ├── templates/        # HTML templates
│   └── static/           # Static files
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Running the Application

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python wsgi.py`
4. Visit: `http://localhost:5000`