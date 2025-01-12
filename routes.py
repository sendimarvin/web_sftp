from flask import Blueprint, jsonify, send_file, render_template, current_app
from models import User
import os
from extensions import db

# Create a Blueprint
main = Blueprint("main", __name__)

@main.route("/users", methods=["GET"])
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


@main.route('/')
def hello_world():
   return 'Login'


@main.route('/files/', defaults={'path': ''})
@main.route('/files/<path:path>')
def list_files(path):
   base_dir = current_app.config['BASE_DIR']
   current_app.logger.info("base_dir: "+base_dir)
   
   # Normalize the path to use forward slashes
   path = path.replace('\\', '/')
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