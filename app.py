from flask import Flask
import os
from config import Config
from extensions import db, login_manager
from routes import main
from flask_wtf.csrf import CSRFProtect
from models import User

def create_app():
   app = Flask(__name__)

   # Load configuration
   app.config.from_object(Config)

   # Initialize database
   db.init_app(app)
   login_manager.init_app(app)
    
    # Configure login manager
   login_manager.login_view = 'main.login'

   @login_manager.user_loader
   def load_user(user_id):
      return User.query.get(int(user_id))

   # In your create_app function:
   csrf = CSRFProtect()
   csrf.init_app(app)

   # Register the blueprint
   app.register_blueprint(main)
   
   
   return app


if __name__ == '__main__':
   app = create_app()
   app.run(host='0.0.0.0', port = 5000, debug=True)