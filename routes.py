from flask import Blueprint, jsonify, request, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from models import User
import os
from extensions import db
from flask import current_app, send_file
from models import Path, UserPermission

# Create a Blueprint
main = Blueprint("main", __name__)

@main.route('/')
def root():
    return redirect(url_for('main.list_files', path=''))


@main.route(f'/sharepoint/users', methods=["GET"])
def list_users():
    """List all users in the database."""
    # Query all users
    users = User.query.all()

    # Serialize the data to return as JSON
    user_list = [
        {
            "UserID": user.UserID,
            "Username": user.Username,
            "FullName": user.FullName,
            "Email": user.Email,
            "IsActive": user.IsActive,
            "CreatedAt": user.CreatedAt.strftime("%Y-%m-%d %H:%M:%S") if user.CreatedAt else None,
        }
        for user in users
    ]

    return jsonify(user_list)


@main.route(f'/sharepoint/', defaults={'path': ''})
@main.route(f'/sharepoint/<path:path>')
@login_required
def list_files(path):
    base_dir = current_app.config['BASE_DIR']
    current_app.logger.info("base_dir: "+base_dir)
    
    # Normalize the path to use forward slashes
    path = path.replace('\\', '/')


    # Always allow access to the root directory
    if not path.strip('/'):
        has_permission = True
    else:
        # Check user permissions
        user_paths = db.session.query(Path.Path).join(UserPermission).filter(
            UserPermission.UserID == current_user.UserID
        ).all()
        user_paths = [p[0] for p in user_paths]  # Extract paths from query result
        
        # If user has root access ('/'), grant permission to everything
        if '/' in user_paths:
            has_permission = True
        # Always allow access to the root directory
        elif not path.strip('/'):
            has_permission = True
        else:
            # Check if the requested path is allowed
            has_permission = False
            for allowed_path in user_paths:
                # Convert both paths to normalized form for comparison
                norm_allowed_path = allowed_path.strip('/').lower()
                norm_request_path = path.strip('/').lower()
                
                # Check if the requested path starts with any of the allowed paths
                if norm_request_path == norm_allowed_path or norm_request_path.startswith(norm_allowed_path + '/'):
                    has_permission = True
                    break
        
    if not has_permission:
        flash('You do not have permission to access this location.', 'error')
        return redirect(url_for('main.list_files', path=''))
   

    abs_path = os.path.join(base_dir, path)
    
    # Security check to prevent directory traversal
    if not os.path.abspath(abs_path).startswith(os.path.abspath(base_dir)):
        return "Access denied", 403
        
    if os.path.isfile(abs_path):
        return send_file(abs_path, as_attachment=True)
        
    if os.path.isdir(abs_path):
        files = []
        for item in os.listdir(abs_path):
            full_path = os.path.join(abs_path, item)
            item_type = 'dir' if os.path.isdir(full_path) else 'file'
            
            # Create the URL-safe path for this item
            # Ensure we use the current path as prefix
            if path:
                item_path = f"{path}/{item}"
            else:
                item_path = item
                
            files.append({
                'name': item,
                'type': item_type,
                'path': item_path
            })
            
        # Create breadcrumbs
        breadcrumbs = []
        current_path = ''
        parts = [p for p in path.split('/') if p]  # Filter out empty parts
        
        for part in parts:
            if current_path:
                current_path = f"{current_path}/{part}"
            else:
                current_path = part
            breadcrumbs.append({
                'name': part,
                'path': current_path
            })
        
        return render_template('directory_listing.html', 
                            files=files, 
                            path=path, 
                            breadcrumbs=breadcrumbs)
        
    return "Not found", 404


@main.route(f'/sharepoint/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(Username=username).first()
        if user and user.check_password(password):
            # Get the next page from args or use default
            next_page = request.args.get('next')
            login_user(user)
            
            # Validate that the next_page is safe
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.list_files', path='')
                
            return redirect(next_page)
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@main.route(f'/sharepoint/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route(f'/sharepoint/create-user', methods=['GET', 'POST'])
@login_required  # Optional: restrict user creation to logged-in users only
def create_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        
        # Check if username already exists
        if User.query.filter_by(Username=username).first():
            flash('Username already exists')
            return redirect(url_for('main.create_user'))
        
        try:
            new_user = User(
                Username=username,
                PasswordHash=generate_password_hash(password),
                FullName=fullname,
                Email=email
            )
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('main.list_users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating user: {str(e)}')
            
    return render_template('create_user.html')