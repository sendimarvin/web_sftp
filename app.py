from flask import Flask
import os
from flask import send_file, render_template_string


app = Flask(__name__)

@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name

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
            
        html_template = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Directory Listing</title>
            <style>
                .folder { font-weight: bold; }
                a { text-decoration: none; }
            </style>
        </head>
        <body>
            <h2>Directory: {{ path if path else '/' }}</h2>
            {% if path %}
            <p><a href="{{ '../' }}">..</a></p>
            {% endif %}
            <ul>
            {% for file in files %}
                <li>
                    <a href="{{ file.name }}" {{ 'class="folder"' if file.type == 'dir' }}>
                        {{ file.name }}{{ '/' if file.type == 'dir' }}
                    </a>
                </li>
            {% endfor %}
            </ul>
        </body>
        </html>
        '''
        return render_template_string(html_template, files=files, path=path)
        
    return "Not found", 404


if __name__ == '__main__':
   app.run(host='0.0.0.0', port = 5000, debug=True)