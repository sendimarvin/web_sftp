from flask import Flask
import os
from flask import send_file, render_template


app = Flask(__name__)

@app.route('/')
def hello_world():
   return 'Hello World'


@app.route('/files/', defaults={'path': ''})
@app.route('/files/<path:path>')
def list_files(path):
    base_dir = 'D:\logs'  # Change this to your desired directory
    abs_path = os.path.join(base_dir, path)
    
    # Security check to prevent directory traversal
    if not os.path.abspath(abs_path).startswith(os.path.abspath(base_dir)):
        return "Access denied", 403
        
    # If path is a file, send it as download
    if os.path.isfile(abs_path):
        return send_file(abs_path, as_attachment=True)
        
    # If path is a directory, list contents
    if os.path.isdir(abs_path):
        files = []
        for item in os.listdir(abs_path):
            full_path = os.path.join(abs_path, item)
            item_type = 'dir' if os.path.isdir(full_path) else 'file'
            files.append({'name': item, 'type': item_type})
            
       
        return render_template('directory_listing.html', files=files, path=path)
        
    return "Not found", 404


if __name__ == '__main__':
   app.run(host='0.0.0.0', port = 5000, debug=True)