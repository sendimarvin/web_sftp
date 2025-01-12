from flask import Flask
import os
from config import Config
from extensions import db
from routes import main

def create_app():
   app = Flask(__name__)

   # Load configuration
   app.config.from_object(Config)

   # Initialize database
   db.init_app(app)

   # Register the blueprint
   app.register_blueprint(main)
   
   return app


if __name__ == '__main__':
   app = create_app()
   app.run(host='0.0.0.0', port = 5000, debug=True)